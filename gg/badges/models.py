from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

from gg.badges.signals import badge_awarded
from gg.badges.managers import BadgeManager
from django.utils.translation import ugettext_lazy as _


if hasattr(settings, 'BADGE_LEVEL_CHOICES'):
    LEVEL_CHOICES = settings.BADGE_LEVEL_CHOICES
else:
    LEVEL_CHOICES = (
        ("1", _("Bronze")),
        ("2", _("Silver")),
        ("3", _("Gold")),
        ("4", _("Diamond")),
    )

class Badge(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        related_name="badges", 
        through='BadgeToUser',
        verbose_name=_("user"))
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, verbose_name=_("level"))
    
    icon = models.ImageField(upload_to='badge_images', verbose_name=_("icon"))
    
    objects = BadgeManager()
    
    @property
    def meta_badge(self):
        from gg.badges.utils import registered_badges
        return registered_badges[self.id]
    
    @property
    def title(self):
        return self.meta_badge.title
    
    @property
    def description(self):
        return self.meta_badge.description
    
    def __unicode__(self):
        return u"%s" % self.title
    
    def get_absolute_url(self):
        return reverse('badge_detail', kwargs={'slug': self.id})
    
    def award_to(self, user):
        has_badge = self in user.badges.all()
        if self.meta_badge.one_time_only and has_badge:
            return False
        
        BadgeToUser.objects.create(badge=self, user=user)
                
        badge_awarded.send(sender=self.meta_badge, user=user, badge=self)
        
        return BadgeToUser.objects.filter(badge=self, user=user).count()

    def number_awarded(self, user_or_qs=None):
        """
        Gives the number awarded total. Pass in an argument to
        get the number per user, or per queryset.
        """
        kwargs = {'badge':self}
        if user_or_qs is None:
            pass
        elif isinstance(user_or_qs, get_user_model()):
            kwargs.update(dict(user=user_or_qs))
        else:
            kwargs.update(dict(user__in=user_or_qs))
        return BadgeToUser.objects.filter(**kwargs).count()


class BadgeToUser(models.Model):
    badge = models.ForeignKey(Badge)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    created = models.DateTimeField(default=timezone.now)


from gg.badges import listeners
