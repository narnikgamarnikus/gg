from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'gg.users'
    verbose_name = "Users"

    def ready(self):
    	import gg.users.signals
    	import gg.users.tasks
