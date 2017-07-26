from django.core.urlresolvers import reverse
from django.views.generic import CreateView, FormView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from .models import UserFace


'''
class UserFaceFormView(FormView):
	form_class = UserFaceForm
	template_name = 'facecontrol/index.html'

	def form_valid(self, form):
		video = form.cleaned_data['video']
		form.delete_temporary_files()

		return super(UserFaceFormView, self).form_valid(form)
'''

@login_required
@csrf_exempt
def createUserFace(request):
	if request.method == 'POST':
		if request.is_ajax():
			video = request.POST.get('data')
			userface, created = UserFace.objects.get_or_create(user=request.user)
			userface.video=request.FILES.get('data')
			userface.save()
			data = '123'
		return JsonResponse({"data" : data})

	return render(request,'facecontrol/index.html')

'''
class UserFaceCreateView(LoginRequiredMixin, CreateView):
	model = UserFace
	fields = ['video'] 
	message = _('Thank you! The interview is over. The result will be sent to your e-mail')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(UserFaceCreateView, self).form_valid(form)

	def form_invalid(self, form):
		print('invalid')
		return super(UserFaceCreateView, self).form_invalid(form)

	def get_success_url(self):
		if messages:
			messages.success(self.request, self.message)
			print(message)
			print(self.request.user.get_absolute_url())
			return self.request.user.get_absolute_url()

'''