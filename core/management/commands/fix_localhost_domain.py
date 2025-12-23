from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = "Add localhost domain to all tenants for development"

    def handle(self, *args, **options):
        tenants = Tenant.objects.all()

        if not tenants.exists():
            self.stdout.write(
                self.style.WARNING('No tenants found. Please create one first.')
            )
            return

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
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created domain 'localhost' for tenant '{tenant.name}'"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Domain already exists for tenant '{tenant.name}'"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                '\n✓ All tenants configured for localhost\n'
                'You can now access the app at: http://localhost:8001'
            )
        )
