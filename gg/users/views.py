from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View, CreateView
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import ugettext_lazy as _

from .models import User, PriceList, Device


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
    fields = ['name', 'is_performer']

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




class PriceListCreateView(CreateView):
    model = PriceList
    message = _('Thank you! Your pricelist has been posted.')
    fields = ['service', 'from_price', 'to_price', 'above_price']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(PriceListCreateView, self).form_valid(form)

    '''
    def get_success_url(self):
        messages.success(
            self.request, self.message)
        return reverse('users:pricelist_list')
    '''

class PriceListDetailView(DetailView):
    model = PriceList
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

class PriceListRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pricelist_detail'


    def get_redirect_url(self, *args, **kwargs):
        return reverse('pricelist:detail',
                       kwargs={'pk': kwargs['pk']})

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
    template_name = 'users/pricelist_list.html'
    model = PriceList


    def get_queryset(self):
        return PriceList.objects.filter(
            created_by=self.request.user) if self.request.user.is_performer else reverse('users:detail',
                       kwargs={'username': self.request.user.username})



class WebPushSubscribeView(View):
    model = Device
    http_method_names = [u'post']

    def post(self):
        print(self.request)
