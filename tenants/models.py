from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    """
    Represents a SaaS customer (company / organization).
    Lives in the public schema.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    # Billing plan info
    plan = models.CharField(
        max_length=100,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Required by tenant_schemas
    auto_create_schema = True
    
    def save(self, *args, **kwargs):
        """Override save to set schema_name based on slug"""
        if not self.schema_name:
            # PostgreSQL schema names must be valid identifiers
            # Replace hyphens with underscores
            self.schema_name = f"tenant_{self.slug.replace('-', '_')}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Domain(DomainMixin):
    """
    Represents a domain for a tenant.
    """
    pass
