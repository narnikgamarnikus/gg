from .models import Assignment
from django import forms
from dal import autocomplete


class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		exclude = ('state', 'slug', 'is_removed', 'created_by')
		widgets = {
			'services': autocomplete.ModelSelect2Multiple(url='crm:services-autocomplete')
			}
