from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey
from djmoney.models.fields import MoneyField
from annoying.fields import AutoOneToOneField
from model_utils.models import SoftDeletableModel, TimeStampedModel
from model_utils import FieldTracker
from django_fsm import ConcurrentTransitionMixin, FSMField, transition
from geoposition.fields import GeopositionField
from .utils import slug_generator
from django.utils import timezone
from django.utils.functional import cached_property
from django.core import serializers
import ujson as json
from .serializers import ExtJsonSerializer, ExtPythonSerializer


@python_2_unicode_compatible
class State(object):
    '''
    Constants to represent the `state`s of the Servuces Models
    '''
    NEW = 'new'              
    ACCEPTED = 'accepted'
    IN_PROGRESS = 'in_progress'
    SUSPENDED = 'suspended'
    RESUMED = 'resumed'
    COMPLETE = 'complete'
    WITHDRAWN = 'withdrawn'
    REJECTED = 'rejected'
    IN = 'in'
    OUT = 'out'      

    JOB_STATES = (
        (NEW, _('New')),
        (ACCEPTED, _('Accepted')),
        (IN_PROGRESS, _('In progress')),
        (SUSPENDED, _('Suspended')),
        (RESUMED, _('Resumed')),
        (COMPLETE, _('Complete')),
        (WITHDRAWN ,_('Withdrawn')),
    )

    JOB_TYPES = (
        (IN, _('In')),
        (OUT, _('Out')), 
    )

    PROPOSAL_STATES = (
        (NEW, _('New')),
        (ACCEPTED, _('Accepted')),
        (WITHDRAWN ,_('Withdrawn')),
    )

    OFFER_STATES = (
        (NEW, _('New')),
        (ACCEPTED, _('Accepted')),
        (WITHDRAWN ,_('Withdrawn')),
        (REJECTED, _('Rejected')),
    )


@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
    tracker = FieldTracker()
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class ServiceUser(Base):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    balance = models.PositiveSmallIntegerField(default=settings.USER_MOUNTHLY_BALANCE)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'slug': self.user.username})


    @cached_property
    def jobs_list(self):
        return [p.service for p in Job.objects.filter(user=self).all()]

    @cached_property
    def jobs(self):
        return Job.objects.filter(user=self).all()

    @cached_property
    def jobs_json(self):
        return ExtJsonSerializer().serialize(Job.objects.filter(user=self), props=['proposals_json']) 


    @cached_property
    def proposals(self):
        return Proposal.objects.filter(user=self).all()

    @cached_property
    def proposals_list(self):
        return [p.service for p in Proposal.objects.filter(user=self).all()]

    @cached_property
    def proposals_json(self):
        return serializers.serialize("json", self.proposals)


    @cached_property
    def pricelist(self):
        return PriceList.objects.filter(user=self).all()


    @cached_property
    def services_list(self):
        return [p.service for p in PriceList.objects.filter(user=self).all()]

    @cached_property
    def services_json(self):
        return serializers.serialize("json", self.services_list[0])

    @cached_property
    def proposals_jobs(self):
        return [p.job.proposals_json for p in self.proposals]


    def __str__(self):  # pragma: no cover
        return self.user.username


@python_2_unicode_compatible
class Service(MPTTModel, Base):
    slug = models.SlugField(
        verbose_name=_('Slug of service'),
        unique=True, 
        null=True)
    title = models.CharField(
        _('Title of service'),
        max_length=50)
    description = models.CharField(
        _('Description of service'),
        max_length=255, 
        null=True)
    name = models.CharField(
        _('Name of service'),
        max_length=50)

    parent = TreeForeignKey(
        'self',
        verbose_name=_('Parent service'),
        null=True, 
        blank=True, 
        related_name='children', 
        db_index=True)


    class MPTTMeta:
        order_insertion_by = ['name']
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Service, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class Job(ConcurrentTransitionMixin, Base):
    slug = models.SlugField(null=True)

    title = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    
    user = models.ForeignKey(ServiceUser)

    type = models.CharField(
        max_length=15, 
        choices=State.JOB_TYPES,
        null=True,
    )
    state = FSMField(
        default=State.NEW,
        choices=State.JOB_STATES,
        protected=True,
    )
    
    services = models.ManyToManyField('services.Service')
    date = models.DateTimeField(default=timezone.now())
    address = GeopositionField()



    @cached_property
    def proposals(self):
        return Proposal.objects.all()

    @cached_property
    def proposals_json(self):
        new_proposals_json = serializers.serialize("json", Proposal.objects.all())
        return [{'index': index, 'object': obj} for index, obj in enumerate(json.loads(new_proposals_json), 1)] 

    @cached_property
    def users(self):
        pricelists = PriceList.objects.filter(service__in=[s for s in self.services.all()])
        return [p.user for p in pricelists if p.user is not self.user]

    @cached_property
    def state_changes(self):
        state_changes = dict()
        return state_changes


    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__state = self.state


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.state != self.__state:
            print('state')

        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)

        super(Job, self).save(force_insert, force_update, *args, **kwargs)
        self.__state = self.state

    #def save(self, *args, **kwargs):
    #
    #    super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('services:job_detail', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class Offer(ConcurrentTransitionMixin, Base):
    slug = models.SlugField(null=True, blank=True)

    state = FSMField(
        default=State.NEW,
        choices=State.OFFER_STATES,
        protected=True,
    )

    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(ServiceUser, null=True)

    class Meta:
        unique_together = (("job", "user"),)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(slug_generator(), allow_unicode=True)
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('services:offer_detail', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class Proposal(ConcurrentTransitionMixin, Base):
    slug = models.SlugField(null=True, blank=True)
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE)
    state = FSMField(
        default=State.NEW,
        choices=State.PROPOSAL_STATES,
        protected=True,
    )
    user = models.ForeignKey(ServiceUser, null=True)
    description = models.CharField(max_length=255, null=True)
    bet = models.PositiveSmallIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (("job", "user"),)

    def make_bet(self):
        self.user.balance - self.bet

    def clean(self):
        if self.bet > self.user.balance:
            raise ValidationError(_('The bet can not be more than your current balance.'))

        if self.user == self.job.user:
            raise ValidationError(_('You can not create proposal for your own job.'))



    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(slug_generator(), allow_unicode=True)
        super(Proposal, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('services:proposal_detail', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class PriceList(Base):
    user = models.ForeignKey(ServiceUser)
    service = models.ForeignKey(Service, null=True, blank=True, 
        related_name='executant_price')
    from_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        null=True)
    to_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        null=True)
    above_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        null=True)

    class Meta:
        unique_together = (("service", "user"),)

    def __str__(self):
        if self.service.name:
            return _('Service: %s') % str(self.service.name)

    def get_absolute_url(self):
        return reverse('service:pricelist_detail', kwargs={'pk': self.pk})
