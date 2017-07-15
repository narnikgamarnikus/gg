from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, PriceList


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

    fields = ['name', 'is_client', 'is_performer']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_performer:
            self.fields = ['name', 'is_client']
        if request.user.is_client:
            self.fields = ['name', 'is_performer']
        if request.user.is_client and request.user.is_performer:
            self.fields = ['name']
        # Check permissions for the request.user here
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

class UserListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = User
    #slug_field = 'username'
    #slug_url_kwarg = 'username'

    def get_queryset(self):
        return User.objects.filter(is_performer=True)


class PriceListUpdateView(LoginRequiredMixin, UpdateView):
    fields = '__all__'

    # we already imported PriceList in the view code above, remember?
    model = PriceList

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:pricelist_detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class PriceListListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = PriceList
    template_name = 'users/pricelist_list.jinja'
    #slug_field = 'pk'
    #slug_url_kwarg = 'pk'

    def get_queryset(self):
        return PriceList.objects.filter(
            user=self.request.user) if self.request.user.is_performer else reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class PriceListDetailView(DetailView):
    model = PriceList
