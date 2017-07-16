from django import forms
from multiselectfield import MultiSelectField
from .models import User
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML


class CustomSignupForm(SignupForm):
	is_performer = forms.BooleanField(required=False)
	
	def __init__(self, *args, **kwargs):
		super(CustomSignupForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		# Add magic stuff to redirect back.
		self.helper.layout.append(
			HTML(
				"{% if redirect_field_value %}"
				"<input type='hidden' name='{{ redirect_field_name }}'"
				"value='{{ redirect_field_value }}' />"
				"{% endif %}"
				)
			)
		# Add submit button like in original form.
		self.helper.layout.append(
			HTML(
				'<br/ ><button class="btn btn-custom btn-sm btn-block" type="submit">'
				'%s</button>' % _('Sign Up')
			)
		)
		self.helper.form_class = 'intro-form'
		self.helper.label_class = 'hidden'
		self.helper.field_class = ''