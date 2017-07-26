from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
@register.inclusion_tag('facecontrol/facecontrol_js.html', takes_context=True)
def facecontrol_js(context):
    request = context['request']
    return {'request': request}

