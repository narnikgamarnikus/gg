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
        view=views.ProposalListView.as_view(),
        name='proposal_list'
    ),
    url(
        regex=r'^~create/$',
        view=views.ProposalCreateView.as_view(),
        name='proposal_create'
    ),
    #url(
    #    regex=r'^~redirect/$',
    #    view=views.UserRedirectView.as_view(),
    #    name='redirect'
    #),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/$',
        view=views.ProposalDetailView.as_view(),
        name='proposal_detail'
    ),
    #url(
    #    regex=r'^~update/$',
    #    view=views.UserUpdateView.as_view(),
    #    name='update'
    #),
]
