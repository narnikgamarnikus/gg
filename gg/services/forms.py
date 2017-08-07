from .models import Job
from django import forms
from dal import autocomplete
from parsley.decorators import parsleyfy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout


#@parsleyfy
class JobForm(forms.ModelForm):
	'''
	def __init__(self, *args, **kwargs):
		super(JobForm, self).__init__(*args, **kwargs)
		helper = FormHelper()
		helper.layout = Layout(
			Field('date', css_class='datepicker'),
		)
	'''
	class Meta:
		model = Job
		exclude = ('state', 'slug', 'is_removed', 'created_by', 'address', 'type', 'user', 'services')
		#parsley_namespace = 'parsley'
		#widgets = {
			#'services': autocomplete.ModelSelect2Multiple(url='crm:services-autocomplete')
			#'date': forms.DateField()
			#}
