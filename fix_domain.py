#!/usr/bin/env python
"""
Script to fix the domain issue for localhost development
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
django.setup()

from tenants.models import Tenant, Domain

# Get all tenants
tenants = Tenant.objects.all()

if not tenants:
    print("No tenants found. Please create one first.")
    sys.exit(1)

for tenant in tenants:
    # Get or create domain for localhost
    domain, created = Domain.objects.get_or_create(
        tenant=tenant,
        defaults={
            'domain': 'localhost',
            'is_primary': True,
        }
    )
    
    if created:
        print(f"✓ Created domain 'localhost' for tenant '{tenant.name}'")
    else:
        print(f"✓ Domain 'localhost' already exists for tenant '{tenant.name}'")

print("\nUpdating /etc/hosts:")
print("Add this line to your /etc/hosts file:")
print("127.0.0.1   localhost")
print("\nYou should already have this, but verify it exists.")
