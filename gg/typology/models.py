from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import SoftDeletableModel, TimeStampedModel
from model_utils import FieldTracker

@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
    tracker = FieldTracker()
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class Action(Base):
    name = models.CharField(_('name'),
        max_length=55, 
        null=True)
    title = models.CharField(_('title'),
        max_length=55, 
        null=True)
    description = models.CharField(_('description'),
        max_length=55, 
        null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Subject(Base):
    name = models.CharField(_('name'),
        max_length=55, 
        null=True)
    action = models.ForeignKey(Action,
        null=True,
        verbose_name=_('action'),)

    title = models.CharField(_('title'),
        max_length=55, 
        null=True)
    description = models.CharField(_('description'),
        max_length=255, 
        null=True)

    class Meta:
        unique_together = (('name', 'action'),)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Brand(Base):
    name = models.CharField(_('name'),
        max_length=55, 
        null=True)
    subject = models.ForeignKey(Subject, 
        null=True,
        verbose_name=_('subject'),)

    title = models.CharField(_('title'),
        max_length=55, 
        null=True)
    description = models.CharField(_('description'),
        max_length=255, 
        null=True)

    class Meta:
        unique_together = (('name', 'subject'),)

    def __str__(self):
        return self.name



@python_2_unicode_compatible
class TypologyItem(Base):
    slug = models.SlugField(_('slug'), 
        null=True)
    name = models.CharField(_('name'),
        max_length=55, 
        null=True)
    title = models.CharField(_('title'),
        max_length=55, 
        null=True)
    description = models.CharField(_('description'),
        max_length=55, 
        null=True)

    action = models.ForeignKey(
        Action, 
        null=True, 
        on_delete=models.CASCADE,
        verbose_name=_('action'))
    subject = models.ForeignKey(
        Subject,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('subject'))
    brand = models.ForeignKey(
        Brand,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('brand'))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.id:
            self.name ='{} {} {}'.format(
                self.action.name,
                self.subject.name,
                self.brand.name
                )
            self.slug = slugify(self.name, allow_unicode=True)
        super(TypologyItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
