from django import forms
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Service

class ServiceModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)

    '''
    def get_queryset(self, request):
    	return super(ServiceMPTTModelAdmin, self).get_queryset(request).annotate(avg_from_price=Avg('executant_price__from_price'), avg_to_price=Avg('executant_price__to_price'))

    def avg_from_price(self, obj):
    	return obj.avg_from_price
    avg_from_price.short_description = 'Средняя цена от'
    avg_from_price.empty_value_display = 'Цена не указана'

    def avg_to_price(self, obj):
    	return obj.avg_to_price
    avg_to_price.short_description = 'Средняя цена до'
    avg_to_price.empty_value_display = 'Цена не указана'

    def get_readonly_fields(self, obj, request):
    	return super(ServiceMPTTModelAdmin, self).get_readonly_fields(obj, request) if not None else + ('avg_from_price', 'avg_to_price')
	'''

admin.site.register(Service, ServiceModelAdmin)
