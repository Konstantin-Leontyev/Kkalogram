# from django.contrib.admin import ModelAdmin, register
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# @register(User)
# class UserAdmin(ModelAdmin):
#     """User model admin site registration class."""
#
#     list_display = [
#         'username',
#         'email',
#         'is_active',
#         'is_staff',
#         'last_login',
#         'date_joined',
#     ]
#     search_fields = ['email', 'username']
#     list_filter = ['is_active', 'is_staff']
