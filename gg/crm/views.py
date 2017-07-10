from django.views.generic import DetailView, CreateView, ListView
from .models import Assignment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gg.services.models import Service
import json


class AssignmentCreateView(CreateView):
	model = Assignment
	fields = '__all__'

	def post(self, request, *args, **kwargs):
		a = Assignment.objects.create(type='In')
		for i in json.loads(request.body.decode('utf-8', 'slashescape')):
			service = Service.objects.get(name=i)
			a.services.add(service)
		a.save()
		return super(AssignmentCreateView, self).post(request, *args, **kwargs)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(AssignmentCreateView, self).dispatch(request, *args, **kwargs)


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    # These next one line tell the view to index lookups by slug
    model = Assignment


class AssignmentListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = Assignment


