from channels import Group
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed
from .models import Job, PriceList, ServiceUser
from annoying.functions import get_object_or_None
import ujson as json

def bet_connect(message):
    message.reply_channel.send({"accept": True})
    Group("bet").add(message.reply_channel)


@receiver(m2m_changed, sender=Job.services.through)
def create_job(sender, instance, **kwargs):
	services = PriceList.objects.filter(service__in=[i for i in instance.services.all()]).select_related()
	for service in services:
		print('USERNAME IS: {} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(service.user.user.username))
		Group("bet").send({
            "text": json.dumps({
                "id": instance.id,
                "title": instance.title,
                "description": instance.description,
                "user": instance.user,
                "datetime": instance.date,
                "content": [s.name for s in instance.services.all()]
            })
        })



def bet_disconnect(message):
    Group("bet").discard(message.reply_channel)


