from django.apps import AppConfig


class CMRConfig(AppConfig):
	name = 'gg.crm'
	verbose_name = 'CRM'

	def ready(self):
		pass
