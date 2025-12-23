from django.contrib import admin
from .models import User, TenantModel

# Register user model in admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    search_fields = ('username', 'role')
    list_filter = ('role',)
    readonly_fields = ('date_joined', 'last_login')
