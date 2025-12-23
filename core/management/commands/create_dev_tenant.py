from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = "Create a development tenant for localhost testing"

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='127.0.0.1:8000',
            help='Domain to associate with the tenant (default: 127.0.0.1:8000)',
        )
        parser.add_argument(
            '--name',
            type=str,
            default='Dev Tenant',
            help='Name of the tenant (default: Dev Tenant)',
        )
        parser.add_argument(
            '--slug',
            type=str,
            default='dev',
            help='Slug for the tenant (default: dev)',
        )

    def handle(self, *args, **options):
        domain = options['domain']
        name = options['name']
        slug = options['slug']

        # Check if tenant already exists
        if Tenant.objects.filter(slug=slug).exists():
            self.stdout.write(
                self.style.WARNING(f'Tenant with slug "{slug}" already exists.')
            )
            return

        try:
            # Create the tenant
            tenant = Tenant.objects.create(
                name=name,
                slug=slug,
                plan='premium',  # Dev gets full features
                is_active=True,
            )

            # Create the domain
            Domain.objects.create(
                domain=domain,
                tenant=tenant,
                is_primary=True,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Tenant "{name}" created successfully!\n'
                    f'  Domain: {domain}\n'
                    f'  Slug: {slug}\n'
                    f'  Schema: {tenant.schema_name}\n\n'
                    f'You can now access the app at: http://{domain}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating tenant: {str(e)}')
            )
