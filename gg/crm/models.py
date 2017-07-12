from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel
from model_utils import FieldTracker
from django_fsm import ConcurrentTransitionMixin, FSMField, transition
from .utils import slug_generator
from django.utils.text import slugify
from django.conf import settings


class State(object):
    '''
    Constants to represent the `state`s of the CRM Models
    '''
    NEW = 'new'              
    ACCEPTED = 'accepted'
    IN = 'in'
    OUT = 'out'      

    ASSIGNMENT_STATES = (
        (NEW, _('New')),
        (ACCEPTED, _('Accepted')),
    )

    ASSIGNMENT_TYPES=(
    	(IN, _('In')),
    	(OUT, _('Out')), 
    )


@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
    tracker = FieldTracker()
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class Assignment(ConcurrentTransitionMixin, Base):
	slug = models.CharField(max_length=36, null=True, blank=True)

	type = models.CharField(
		max_length=15, 
		choices=State.ASSIGNMENT_TYPES,
		null=True,
	)
	state = FSMField(
		default=State.NEW,
		#verbose_name='Статус',
		choices=State.ASSIGNMENT_STATES,
		protected=True,
	)

	services = models.ManyToManyField('services.Service')

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(slug_generator(), allow_unicode=True)
		super(Assignment, self).save(*args, **kwargs)

	def __str__(self):
		return self.slug

	def get_absolute_url(self):
		return reverse('crm:assignment_detail', kwargs={'slug': self.slug})
