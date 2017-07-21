from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from .models import TypologyItem, Action, Subject, Brand


class TypologyForm(forms.ModelForm):

	class Meta:
		model = TypologyItem
		fields = [
		'title', 'description', 'name',
		'action', 'subject', 'brand'
		]

		widgets = {
			'action': forms.Textarea(attrs={'cols': 10, 'rows': 20}),
			'subject': forms.Textarea(attrs={'cols': 10, 'rows': 20}),
			'brand': forms.Textarea(attrs={'cols': 10, 'rows': 20}),
		}

	def clean_name(self):
		print('CLEANED DATA IS: ' + str(self.cleaned_data))
		self.actions = '123'#[line for line in self.cleaned_data['action'].text_area_value.split('\n')]
		self.subjects = '321'#[line for line in self.cleaned_data['subject'].text_area_value.split('\n')]
		self.brands = '555'#[line for line in self.cleaned_data['brand'].text_area_value.split('\n')]

	def save(self, commit=False):
		print('CLEANED DATA IS: ' + str(self.cleaned_data))
		print(self.actions)
		print(self.subjects)
		print(self.brands)
