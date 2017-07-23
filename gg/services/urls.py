from django.conf.urls import url

from . import views

urlpatterns = [
	url(
		regex=r'^service/$',
		view=views.ServiceListView.as_view(),
		name='service_list'
	),
    url(
        regex=r'^service/(?P<slug>[\w.@+-]+)/$',
        view=views.ServiceDetailView.as_view(),
        name='service_detail'
    ),
    url(
    	regex=r'^service/~update/(?P<slug>[\w.@+-]+)/$',
    	view=views.ServiceUpdateView.as_view(),
    	name='service_update'
    ),
    url(
        regex=r'^service/~create$',
        view=views.ServiceCreateView.as_view(),
        name='service_create'
    ),

    url(
        regex=r'^pricelist/$',
        view=views.PriceListListView.as_view(),
        name='pricelist_list'
    ),
    url(
        regex=r'^pricelist/~update$',
        view=views.PriceListUpdateView.as_view(),
        name='pricelist_update'
    ),
    url(
        regex=r'^pricelist/~create$',
        view=views.PriceListCreateView.as_view(),
        name='pricelist_create'
    ),
    url(
        regex=r'^pricelist/(?P<pk>[\w.@+-]+)/$',
        view=views.PriceListDetailView.as_view(),
        name='pricelist_detail'
    ),

    url(
        regex=r'^profile/(?P<username>[\w.@+-]+)/$', 
        view=views.ServiceUserDetailView, 
        name='service_user_detail'
    )
]
