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

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Job, self).save(*args, **kwargs)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    description = models.CharField(max_length=255, null=True)
    bet = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (("job", "user"),)

    def clean(self):
        if self.bet > settings.AUTH_USER_MODEL.objects.get(pk=self.user.user.pk).balane:
            raise ValidationError(_('The bet can not be more than your current balance.'))
        if self.bet < settings.AUTH_USER_MODEL.objects.get(pk=self.user.user.pk).balane:
            raise ValidationError(_('The bet can not be less than your current balance.'))

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
    
    def __str__(self):
        if self.service.name:
            return _('Service: %s') % str(self.service.name)

    def get_absolute_url(self):
        return reverse('service:pricelist_detail', kwargs={'pk': self.pk})
