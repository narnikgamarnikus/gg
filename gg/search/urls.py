from django.conf.urls import include, url
from .views import autocomplete


urlpatterns = [
    url(r'^', include('haystack.urls')),
    url(r'^autocomplete/', autocomplete, name='autocomplete'),
]