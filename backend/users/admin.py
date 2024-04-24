from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'last_login',
        'date_joined',
    )
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff',)


admin.site.empty_value_display = 'Значение не задано'
