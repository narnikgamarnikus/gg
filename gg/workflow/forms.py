from .models import Proposal
from django import forms
from dal import autocomplete


class ProposalForm(forms.ModelForm):
	class Meta:
		model = Proposal
		exclude = ('state', 'slug', 'is_removed', 'created_by')
		widgets = {
			'services': autocomplete.ModelSelect2Multiple(url='crm:services-autocomplete')
			}
