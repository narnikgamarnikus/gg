from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'gg.users'
    verbose_name = "Users"

    def ready(self):
    	pass