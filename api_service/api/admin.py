from django.contrib import admin

from .models import UserRequestHistory


# @admin.register(UserRequestHistory)
# class NotificationTypeAdmin(admin.ModelAdmin):
#     pass

admin.site.register(UserRequestHistory)