from django import template
from allauth.account.forms import LoginForm, SignupForm

register = template.Library()

@register.inclusion_tag('_formtag.html')
def allauth_popup(request):
    return {
    'login_form': LoginForm(), 
    'signup_form': SignupForm()
    }