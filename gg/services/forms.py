from .models import Job
from django import forms
from dal import autocomplete


class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		exclude = ('state', 'slug', 'is_removed', 'created_by')
		widgets = {
			'services': autocomplete.ModelSelect2Multiple(url='crm:services-autocomplete')
			}
