from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from .models import Service


class ServiceDetailView(DetailView):
	model = Service
	slug_field = 'slug'
	slug_url_kwarg = 'slug'


class ServiceUpdateView(UpdateView):
	fields = ['name', 'parent']

	# we already imported Service in the view code above, remember?
	model = Service

	# send the service back to their own page after a successful update
	def get_success_url(self):
		return reverse('services:detail',
			kwargs={'slug': self.kwargs.get("slug")})

	def get_object(self):
	# Only get the Service record for the service making the request
		return Service.objects.get(slug=self.kwargs.get("slug"))


class ServiceRedirectView(RedirectView):
	permanent = False

	def get_redirect_url(self):
		return reverse('services:detail',
			kwargs={'slug': self.kwargs.get("slug")})

class ServiceListView(ListView):
    # These next one line tell the view to index lookups by slug
    model = Service