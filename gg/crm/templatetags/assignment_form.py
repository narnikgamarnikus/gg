from django import template
from ..forms import AssignmentForm 
register = template.Library()

@register.inclusion_tag('crm/templatetags/assignment_form.html', takes_context=True)
def assignment_form(context):
	return {
        'assignment_form': AssignmentForm(),
    }