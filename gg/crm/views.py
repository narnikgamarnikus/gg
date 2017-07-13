from django.views.generic import DetailView, CreateView, ListView, View
from django.views.generic.edit import BaseCreateView
from .models import Assignment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gg.services.models import Service
import ujson as json
from .forms import AssignmentForm
from django.core.urlresolvers import reverse
from dal import autocomplete
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
import ujson as json
from django.core import serializers
from .filters import AssignmentFilter

class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    message = _('Thank you! your assignment has been posted.')


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(
            self.request, self.message)
        return reverse('crm:assignment_detail', kwargs={'slug': self.object.slug})


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    # These next one line tell the view to index lookups by slug
    model = Assignment

    def get_context_data(self, **kwargs):
    	context = super(AssignmentDetailView, self).get_context_data(**kwargs)
    	return context


class AssignmentListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = Assignment
    template_name = 'crm/assignment_list.html'

    def get_queryset(self):
        queryset = Assignment.objects.order_by('created').distinct()
        if self.request.GET:
            f = AssignmentFilter(self.request.GET, queryset)
            return f.qs
        return queryset




class ServicesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Service.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs