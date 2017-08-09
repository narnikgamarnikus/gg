from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = 'gg.services'
    verbose_name = 'Services'

    def ready(self):
    	import gg.services.tasks
    	import gg.services.consumers
