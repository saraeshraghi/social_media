from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = UserProfile
    # can_delete = False


class ExtendeUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ExtendeUserAdmin)