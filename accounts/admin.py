from .models import CustomUser
from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'password', 'icon', 'ranking', 'score', 'last_login', 'date_joined', 'last_name',
        'first_name', 'is_superuser', 'is_staff', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = (
        'id', 'username', 'email', 'password', 'icon', 'ranking', 'score', 'last_login', 'date_joined', 'last_name',
        'first_name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = (
        'last_login', 'date_joined', 'is_superuser', 'is_staff', 'is_active')


admin.site.register(CustomUser, CustomerAdmin)
