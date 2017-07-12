from gg.badges.utils import MetaBadge
from gg.users.models import User
from gg.badges.utils import register as register_badge


class Autobiographer(MetaBadge):
    id = "autobiographer"
    model = User
    one_time_only = True

    title = "Autobiographer"
    description = "Completed the User Profile"
    level = "1"

    progress_start = 0
    progress_finish = 1
    
    def get_user(self, instance):
        return instance

    def get_progress(self, user):
        has_email = 1 if user.email else 0
        return has_email + has_bio
    
    def check_email(self, instance):
        return instance.email


register_badge(Autobiographer)
