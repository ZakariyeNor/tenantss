from django.contrib import admin
from .models import Tenant, Domain


# Register tenant
class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'is_active', 'created_at')
    search_fields = ('name', 'plan')
    list_filter = ('created_at', 'plan')
    readonly_fields = ('slug',)
    ordering = ('-created_at',)
    inlines = [DomainInline]


# Register Domain
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('tenant', 'is_primary')
    search_fields = ('domain',)