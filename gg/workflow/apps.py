from django.apps import AppConfig


class WorkflowConfig(AppConfig):
	name = 'gg.workflow'
	verbose_name = 'Workflow'

	def ready(self):
		pass
