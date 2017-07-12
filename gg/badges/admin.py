from django.contrib import admin

from gg.badges.models import Badge
from gg.users.models import User


class InlineBadgeToUser(admin.StackedInline):
	model = User.badges.through

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    fields = ('icon', 'level')
    list_display = ('id','level')
    inlines = [InlineBadgeToUser]


