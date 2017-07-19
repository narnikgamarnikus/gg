from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View, CreateView
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import ugettext_lazy as _

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    # These next one line tell the view to index lookups by slug
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

class UserListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = User
