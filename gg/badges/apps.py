from django.apps import AppConfig


class BadgesConfig(AppConfig):
    name = 'gg.badges'
    verbose_name = "Badges"

    def ready(self):
    	import gg.badges.signals
