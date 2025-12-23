from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom user model
class User(AbstractUser):
    """
    Custom user linked to a tenant.
    """
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('staff', 'Staff'),
        ('user', 'User'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    
    def is_owner(self):
        return self.role == 'owner'
    
    def is_admin(self):
        return self.role in ['owner', 'admin']
    
    
    def __str__(self):
        return f"{self.username} | ({self.role})"

# Tenant-specific data model
class TenantModel(models.Model):
    """
    Abstract base model for tenant-specific data.
    Automatically isolated by schema.
    """
    class Meta:
        abstract = True