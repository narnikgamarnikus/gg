from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = 'gg.services'
    verbose_name = 'Services'

    def ready(self):
    	pass
