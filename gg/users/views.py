from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View, CreateView
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import ugettext_lazy as _

from .models import User

from hitcount.views import HitCountDetailView

from friendship.models import Friend, FriendshipRequest

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from annoying.functions import get_object_or_None


class UserDetailView(LoginRequiredMixin, HitCountDetailView):
    # These next one line tell the view to index lookups by slug
    model = User
    count_hit = True
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['friendship_request'] = Friend.objects.can_request_send(self.request.user, user)
        context['friends'] = Friend.objects.friends(user)
        return context



class UserRedirectView(LoginRequiredMixin, RedirectView):
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


class UserFriendsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_friends.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserFriendsListView, self).get_context_data(*args, **kwargs)
        context['unrejected_friends'] = FriendshipRequest.objects.filter(to_user=self.request.user, rejected__isnull=True)[:5]
        context['unviewed_friends'] = FriendshipRequest.objects.filter(to_user=self.request.user, viewed__isnull=True)[:5]
        context['all_friends'] = Friend.objects.friends(user=self.request.user)[:5]
        return context

    #def get_queryset(self):
    #    return Friend.objects.unread_requests(user=self.request.user).order_by('-created')


class UserAddToFriendView(LoginRequiredMixin, RedirectView):
    pattern_name = 'users:detail'
    permanent = False
    query_string = True
    http_method_names = [u'post'] 
    # we already imported User in the view code above, remember?
    model = User

    def post(self, request, *args, **kwargs):
        print(kwargs['username'])
        user = get_object_or_404(User, username=kwargs['username'])
        Friend.objects.add_friend(self.request.user, user)
        return super(UserAddToFriendView, self).post(request, *args, **kwargs)

    # send the user back to their own page after a successful update
    def get_success_url(self, *args, **kwargs):
        return super(UserAddToFriendView, self).get_redirect_url(*args, **kwargs)


class UserFriendshipDetailView(LoginRequiredMixin, DetailView):
    # These next one line tell the view to index lookups by slug
    model = FriendshipRequest
    pk_url_kwarg = 'friendship_request_id' 
    template_name = 'users/user_friendship.html'
    context_object_name = 'object'

    def get_context_data(self, *args, **kwargs):
        context = super(UserFriendshipDetailView, self).get_context_data(*args, **kwargs)
        context['user'] = context['object'].from_user
        return context    

    def get(self, request, *args, **kwargs):
        get = super(UserFriendshipDetailView, self).get(request, *args, **kwargs)
        context = self.get_context_data(object=self.object)
        if not context['object'].viewed:
            context['object'].mark_viewed()
        return get



class UserFriendRejectView(LoginRequiredMixin, RedirectView):
    pattern_name = 'users:friendship'
    http_method_names = [u'post', u'get'] 
    model = FriendshipRequest

    def post(self, request, *args, **kwargs):
        friendship_request = get_object_or_404(FriendshipRequest,
            id=kwargs['friendship_request_id'])
        friendship_request.reject()
        return super(UserFriendRejectView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('%s#unrejected-friends' % reverse('users:friends'))


class UserFriendAcceptView(LoginRequiredMixin, RedirectView):
    http_method_names = [u'post', u'get'] 
    # we already imported User in the view code above, remember?
    model = FriendshipRequest

    def post(self, request, *args, **kwargs):
        friendship_request = get_object_or_404(FriendshipRequest,
            id=kwargs['friendship_request_id'])
        friendship_request.accept()
        return super(UserFriendAcceptView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('%s#unrejected-friends' % reverse('users:friends'))


class UserFriendCancelView(LoginRequiredMixin, RedirectView):
    http_method_names = [u'post', u'get'] 
    # we already imported User in the view code above, remember?
    model = FriendshipRequest

    def post(self, request, *args, **kwargs):
        friendship_request = get_object_or_404(FriendshipRequest,
            id=kwargs['friendship_request_id'])
        friendship_request.cancel()
        return super(UserFriendCancelView, self).post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return redirect('%s#all-friends' % reverse('users:friends'))


class UserFriendViewedView(LoginRequiredMixin, RedirectView):
    pattern_name = 'users:friendship'
    http_method_names = [u'post', u'get'] 
    # we already imported User in the view code above, remember?
    model = FriendshipRequest

    def post(self, request, *args, **kwargs):
        friendship_request = get_object_or_404(FriendshipRequest,
            id=kwargs['friendship_request_id'])
        friendship_request.mark_viewed()
        return super(UserFriendViewedView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('%s#unviewed-friends' % reverse('users:friends'))

class UserListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = User
