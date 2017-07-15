from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Service(MPTTModel):
    slug = models.CharField(
    	verbose_name=_('Slug of Service'),
    	max_length=50, 
    	unique=True, 
    	null=True, 
    	blank=True)
    name = models.CharField(
    	_('Name of this service'),
    	max_length=50, 
    	unique=True)
    parent = TreeForeignKey(
        'self',
    	verbose_name=_('Parent of this service'),
    	null=True, 
    	blank=True, 
    	related_name='children', 
    	db_index=True)
    '''
   	problems = models.ManyToManyField(
   		'services.Trouble', 
   		related_name='service', 
   		blank=True,
   		_('The problems that are solved by this service'))
	'''
    class Meta:
    	verbose_name = "Услуга"
    	verbose_name_plural = "Услуги"


    class MPTTMeta:
        order_insertion_by = ['name']
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Service, self).save(*args, **kwargs)
    
    def __str__(self):
    	return self.name

    def get_absolute_url(self):
    	return reverse('services:detail', kwargs={'slug': self.slug})


