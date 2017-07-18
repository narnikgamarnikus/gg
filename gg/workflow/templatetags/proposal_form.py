from django import template
from ..forms import ProposalForm 
register = template.Library()

@register.inclusion_tag('crm/templatetags/proposal_form.html', takes_context=True)
def proposal_form(context):
	return {
        'proposal_form': ProposalForm(),
    }