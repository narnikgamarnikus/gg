from channels import Group
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed
from .models import Job, PriceList, ServiceUser, Proposal
from annoying.functions import get_object_or_None
import ujson as json
from channels.auth import channel_session_user, channel_session_user_from_http, http_session
from django.core import serializers
from .serializers import ExtJsonSerializer, ExtPythonSerializer


@channel_session_user_from_http
def services_connect(message):
    message.reply_channel.send({"accept": True})
    Group("services").add(message.reply_channel)


@receiver(m2m_changed, sender=Job.services.through)
def new_job(sender, instance, action, **kwargs):
    user = ServiceUser.objects.get(user=instance.user)
    Group("services").send({
        "text": json.dumps({
            "jobs": user.jobs_json,
            "proposals": user.proposals_jobs,
        })
    })
    '''
    if action is "post_add":
        print(instance.date)
        pricelists = PriceList.objects.filter(service__in=[s for s in instance.services.all()]).select_related()
        print(pricelists)

        for pricelist in pricelists:
            print('USERNAME IS: {} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(pricelist.user.user.username))
            Group("services").send({
                "text": json.dumps({
                    "id": instance.id,
                    "title": instance.title,
                    "description": instance.description,
                    "user": instance.user,
                    "datetime": instance.date,
                })
            })
    '''

@receiver(post_save, sender=Proposal)
def new_proposal(sender, created, instance, **kwargs):
    user = ServiceUser.objects.get(user=instance.user)
    Group("services").send({
        "text": json.dumps({
            "jobs": user.jobs_json,
            "proposals": user.proposals_jobs,
        })
    })  
    '''
    proposals = [proposal for proposal in 
    Proposal.objects.filter(job=instance.job).
    order_by('discount', 'bet').all()]
    #a = serializers.serialize("json", Proposal.objects.filter(job=instance.job).order_by('discount', 'bet').all()) 
    a = {index: obj for index, obj in enumerate(proposals, 1)}
    print(a)
    
    #proposals = enumerate(Proposal.objects.filter(job=instance.job).all(), start=1)     
    Group("services").send({
        "text": json.dumps({
            "job": instance.job,
            "user": instance.user,
            "description": instance.description,
            "bet": instance.bet,
            "discount": instance.discount,
            })
        })
    '''



@channel_session_user
def services_message(message):

    if message.user.is_authenticated():
        user = ServiceUser.objects.get(user=message.user)
        Group("services").send({
            "text": json.dumps({
                "jobs": user.jobs_json,
                "proposals": user.proposals_jobs,
            })
        })  
        
@channel_session_user
def services_disconnect(message):
    Group("services").discard(message.reply_channel)
