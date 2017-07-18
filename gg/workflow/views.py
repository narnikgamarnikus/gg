from django.views.generic import DetailView, CreateView, ListView, View
from django.views.generic.edit import BaseCreateView
from django.views.decorators.csrf import csrf_exempt

from django.core.urlresolvers import reverse

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import ujson as json
from dal import autocomplete

from hitcount.views import HitCountDetailView

from gg.services.models import Service
from .filters import ProposalFilter
from .forms import ProposalForm
from .models import Proposal, Response


class ProposalCreateView(CreateView):
    model = Proposal
    form_class = ProposalForm
    message = _('Thank you! Your proposal has been posted.')


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ProposalCreateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(
            self.request, self.message)
        return reverse('crm:proposal_detail', kwargs={'slug': self.object.slug})

class ProposalDetailView(LoginRequiredMixin, HitCountDetailView):
    # These next one line tell the view to index lookups by slug
    model = Proposal

    def get_context_data(self, **kwargs):
    	context = super(ProposalDetailView, self).get_context_data(**kwargs)
    	return context

class ProposalListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = Proposal
    template_name = 'workflow/proposal_list.jinja'

    def get_queryset(self):
        queryset = Proposal.objects.order_by('created').distinct()
        if self.request.GET:
            f = ProposalFilter(self.request.GET, queryset)
            return f.qs
        return queryset


class ResponseCreateView(CreateView):
    model = Response
    message = _('Thank you! Your response has been posted.') 

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ResponseCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, self.message)
        return reverse('crm:response_detail', kwargs={'slug': self.object.slug})

class ResponseDetailView(LoginRequiredMixin, HitCountDetailView):
    model = Response

    def get_context_data(self, **kwargs):
        context = super(ResponseDetailView, self).get_context_data(**kwargs)
        return context

class ResponseListView(LoginRequiredMixin, ListView):
    model = Response

    def get_queryset(self):
        queryset = Proposal.objects.order_by('created').distinct()
        return queryset


class ServicesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Service.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs