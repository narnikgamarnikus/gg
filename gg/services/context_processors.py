from django import template
from gg.services.forms import JobForm

#register = template.Library()

#@register.inclusion_tag('_formtag.html')
def job_form(request):
	job_form = JobForm() 
	return {
		"job_form": job_form
	}