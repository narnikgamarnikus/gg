from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from django.conf import settings
from djmoney.models.fields import MoneyField
from gg.crm.models import Base
from gg.services.models import Service

@python_2_unicode_compatible
class User(AbstractUser):

	EXECUTANT = 'executant'
	CLIENT = 'client'   

	USER_ROLES = (
		(EXECUTANT, _('Executant')),
		(CLIENT, _('Client')),
	)

	# First Name and Last Name do not cover name patterns
	# around the globe.
	role = MultiSelectField(
		max_length=30, 
		null=True,
		choices=USER_ROLES,
	)
	is_performer = models.BooleanField(default=False)
	is_client = models.BooleanField(default=False)
	name = models.CharField(_('Name of User'), blank=True, max_length=255)
	balance = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.username

	def get_absolute_url(self):
		return reverse('users:detail', kwargs={'username': self.username})



@python_2_unicode_compatible
class PriceList(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, blank=True, 
        related_name='executant_price')
    #trouble = models.ManyToManyField('service.Trouble', blank=True, 
    #    verbose_name='Проблема', related_name='executant_price')
    #time = models.TimeField(null=True, blank=True, 
    #    verbose_name='Время, за которое осуществляется услуга за указанную сумму')
    from_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        null=True)
    to_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        null=True)
    above_price = MoneyField(max_digits=10, decimal_places=2, default_currency='BYN',
        null=True)
    
    def __str__(self):
        if self.service.name:
            return 'Service: %s' % str(self.service.name)
    
    #class Meta:
    #    verbose_name = "Прейскурант цен"
    #    verbose_name_plural = "Прейскурант цен"

from gg.users import meta_badges