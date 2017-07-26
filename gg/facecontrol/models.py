from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'facecontrol/user_{0}'.format(instance.user.id)


class UserFace(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
	video = models.FileField(upload_to=user_directory_path)
	accepted = models.BooleanField(default=False)


	def __str__(self):  # pragma: no cover
		return self.user.username