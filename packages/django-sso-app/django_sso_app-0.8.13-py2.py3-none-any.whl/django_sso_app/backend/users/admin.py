from django.contrib import admin
from django.contrib.auth import get_user_model

from ...core.apps.users.admin import UserAdmin

User = get_user_model()


admin.site.register(User, UserAdmin)
