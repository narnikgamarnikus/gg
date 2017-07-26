from .models import Job
from django import forms
from dal import autocomplete
from parsley.decorators import parsleyfy


@parsleyfy
class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		exclude = ('state', 'slug', 'is_removed', 'created_by')
		parsley_namespace = 'parsley'
		widgets = {
			'services': autocomplete.ModelSelect2Multiple(url='crm:services-autocomplete')
			}
