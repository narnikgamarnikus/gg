from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        regex=r'^services-autocomplete/$',
        view=views.ServicesAutocomplete.as_view(),
        name='services-autocomplete',
    ),
]

urlpatterns += [

    url(
        regex=r'^$',
        view=views.AssignmentListView.as_view(),
        name='assignment_list'
    ),
    url(
        regex=r'^~create/$',
        view=views.AssignmentCreateView.as_view(),
        name='assignment_create'
    ),
    #url(
    #    regex=r'^~redirect/$',
    #    view=views.UserRedirectView.as_view(),
    #    name='redirect'
    #),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/$',
        view=views.AssignmentDetailView.as_view(),
        name='assignment_detail'
    ),
    #url(
    #    regex=r'^~update/$',
    #    view=views.UserUpdateView.as_view(),
    #    name='update'
    #),
]
