from django.conf.urls import url

from . import views

urlpatterns = [
	url(
		regex=r'^$',
		view=views.ServiceListView.as_view(),
		name='list'
	),
	url(
    	regex=r'^~redirect/$',
    	view=views.ServiceRedirectView.as_view(),
    	name='redirect'
    ),
    url(
    	regex=r'^~update/(?P<slug>[\w.@+-]+)/$',
    	view=views.ServiceUpdateView.as_view(),
    	name='update'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/$',
        view=views.ServiceDetailView.as_view(),
        name='detail'
    ),
]
