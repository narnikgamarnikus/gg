import ujson as json
from dal import autocomplete
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from hitcount.views import HitCountDetailView
from .filters import JobFilter
from .forms import JobForm
from .models import (
	Service, Job, Offer, 
	Proposal, PriceList,
	ServiceUser)
from django.views.generic import (
	View, DetailView, ListView, 
	RedirectView, UpdateView, CreateView
	)

class ServiceUserDetailView(HitCountDetailView):
	model = ServiceUser

	def get_object(self):
		return settings.AUTH_USER_MODEL.objects.get_or_404(slug=self.kwargs['username'])



class ServiceListView(ListView):
	# These next one line tell the view to index lookups by slug
	model = Service


class ServiceDetailView(HitCountDetailView):
	model = Service



class ServiceCreateView(CreateView):
	model = Service
	message = _('Thank you! Your service has been created.')
	fields = ['title', 'description', 'name', 'parent']

	def get_success_url(self):
		messages.success(
			self.request, self.message)
		return reverse('service:service_detail', kwargs={'slug': self.object.slug})


class ServiceUpdateView(UpdateView):
	fields = ['name', 'parent']
	# we already imported Service in the view code above, remember?
	model = Service
	message = _('Thank you! Your service has been updated.')

	def get_success_url(self):
		messages.success(
			self.request, self.message)
		return reverse('service:service_detail', kwargs={'slug': self.object.slug})


'''
class ServiceRedirectView(RedirectView):
	permanent = False

	def get_redirect_url(self, *args, **kwargs):
		return reverse('services:detail',
			kwargs={'slug': self.kwargs.get("slug")})
'''



class JobListView(ListView):
	model = Job

	def get_queryset(self):
		queryset = Job.objects.order_by('created').distinct()
		if self.request.GET:
			f = JobFilter(self.request.GET, queryset)
			return f.qs
		return queryset


class JobDetailView(HitCountDetailView):
	model = Job


class JobCreateView(CreateView):
	model = Job
	message = _('Thank you! Your job has been created.')
	fields = ['title', 'description', 'type', 'services', 'date', 'address']

	def form_valid(self, form):
		form.instance.user = self.request.user.service_user
		return super(JobCreateView, self).form_valid(form)

	def get_success_url(self):
		messages.success(
			self.request, self.message)
		return reverse('service:job_detail', kwargs={'slug': self.object.slug})


class JobUpdateView(UpdateView):
	model = Job
	fields = ['title', 'description', 'services', 'date', 'address']
	message = _('Thank you! Your job has been updated.')

	def get_success_url(self):
		messages.success(
			self.request, self.message)
		return reverse('service:job_detail', kwargs={'slug': self.object.slug})


class OfferListView(ListView):
	model = Offer


class OfferDetailView(HitCountDetailView):
	model = Offer


class OfferCreatedView(CreateView):
	model = Offer
	fields = ['user']
	message = _('Thank you! Your offer has been created.')

	def get_success_url(self):
		messages.success(
			self.request, self.message)
		return reverse('service:offer_detail', kwargs={'slug': self.object.slug})


class ProposalCreateView(CreateView):
	model = Proposal
	fields = ['description', 'bet']
	message = _('Thank you! Your proposal has been posted.')

	def form_valid(self, form):
		form.instance.user = self.request.user.service_user
		return super(ProposalCreateView, self).form_valid(form)

	def get_success_url(self):
		messages.success(
			self.request, self.message)
		return reverse('service:job_detail', kwargs={'slug': self.object.job.slug})


class ProposalDetailView(LoginRequiredMixin, HitCountDetailView):
    # These next one line tell the view to index lookups by slug
    model = Proposal

    def get_context_data(self, **kwargs):
    	context = super(ProposalDetailView, self).get_context_data(**kwargs)
    	return context


class ProposalListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = Proposal

    def get_queryset(self):
    	return Proposal.objects.filter(job=self.job).order_by('-bet')


class PriceListCreateView(CreateView):
    model = PriceList
    message = _('Thank you! Your pricelist has been created.')
    fields = ['service', 'from_price', 'to_price', 'above_price']

    def form_valid(self, form):
    	form.instance.created_by = self.request.user.service_user
    	return super(PriceListCreateView, self).form_valid(form)


class PriceListDetailView(DetailView):
    model = PriceList
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

'''
class PriceListRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pricelist_detail'


    def get_redirect_url(self, *args, **kwargs):
        return reverse('pricelist:detail',
                       kwargs={'pk': kwargs['pk']})
'''

class PriceListUpdateView(LoginRequiredMixin, UpdateView):
	fields = '__all__'
	# we already imported PriceList in the view code above, remember?
	message = _('Thank you! Your pricelist has been updated.')
	model = PriceList

	# send the user back to their own page after a successful update
	def get_success_url(self, *args, **kwargs):
		return reverse('service:pricelist_detail',
			kwargs={'pk': kwargs['pk']})


class PriceListListView(LoginRequiredMixin, ListView):
	# These next one line tell the view to index lookups by slug
	model = PriceList

	def get_queryset(self):
		return PriceList.objects.filter(user__user=self.request.user)





'''
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
'''

class ServicesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Service.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs