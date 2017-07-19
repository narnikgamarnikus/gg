from __future__ import absolute_import, unicode_literals
from celery import shared_task
from gg.users.models import User
from annoying.functions import get_object_or_None
from datetime import timedelta
from celery.task import periodic_task
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.conf import settings


@periodic_task(run_every=timedelta(days=30))
def changed_user_balance(user_pk):
	user = get_object_or_None(User, pk=user_pk)
	if user:
		user.balance = settings.USER_MOUNTHLY_BALANCE
	return user


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
	if created:
		changed_user_balance(instance.id)