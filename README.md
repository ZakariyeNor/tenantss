# TaskForce - Multi-Tenant Project Management SaaS

A production-ready **semi-isolated multi-tenant SaaS application** built with Django and PostgreSQL. Each tenant gets a completely isolated database schema, ensuring complete data separation and security.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Development Workflow](#development-workflow)
- [Multi-Tenancy](#multi-tenancy)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Features (Implemented)
- ✅ **Multi-tenant architecture** with schema-based isolation
- ✅ **Custom user authentication** with role-based access control
- ✅ **JWT token authentication** via djangorestframework-simplejwt
- ✅ **Admin interface** for tenant and domain management
- ✅ **Redis caching** for performance optimization
- ✅ **CORS support** for cross-origin requests
- ✅ **Health check endpoint** for monitoring

### Upcoming Features (TODO)
- 📋 Project management endpoints
- 📋 Task management and tracking
- 📋 Team collaboration features
- 📋 Activity audit logging
- 📋 File attachment support
- 📋 Real-time notifications
- 📋 Advanced reporting and analytics

## 🏗️ Architecture

### Multi-Tenancy Overview

This application implements **schema-based multi-tenancy**, where:

```
┌─────────────────────────────────────────────────────────────┐
│                        PostgreSQL Database                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Public Schema│  │  tenant_dev  │  │ tenant_acme  │      │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤      │
│  │ - Tenant     │  │ - Project    │  │ - Project    │      │
│  │ - Domain     │  │ - Task       │  │ - Task       │      │
│  │ - User       │  │ - Comment    │  │ - Comment    │      │
│  │ - Auth       │  │ - Activity   │  │ - Activity   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- **Public Schema**: Contains Tenant, Domain, and User models (shared across all tenants)
- **Tenant Schemas**: Each tenant gets isolated schema (e.g., `tenant_dev`, `tenant_acme`)
- **Automatic Isolation**: Database-level isolation ensures no data leakage
- **Domain Routing**: Requests routed by hostname to correct tenant schema

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.0
- **Database**: PostgreSQL with django-tenants
- **API**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Caching**: Redis with django-redis
- **Task Queue**: Celery (configured, ready for use)
- **Web Server**: Gunicorn (production)

### Frontend (Future)
- React or Vue.js (to be implemented)

### DevOps
- Docker & Docker Compose (optional)
- Environment variables (.env)
- WhiteNoise for static files

## 📦 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Redis (optional, for caching)
- pip and virtualenv

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd tenants
```

### Step 2: Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
Create a `.env` file in the project root:

```env
# PostgreSQL Configuration
DB_NAME=tenants
DB_USER=tenant_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Initialize Database
```bash
# Run migrations for shared (public) schema
python manage.py migrate_schemas --shared

# Create a development tenant (optional)
python manage.py create_dev_tenant --slug dev --name "Dev Tenant"

# Add localhost domain mapping
python manage.py fix_localhost_domain
```

### Step 6: Create Superuser (for admin)
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver 0.0.0.0:8001
```

Access the app:
- **API Health**: http://localhost:8001/api/health/
- **Admin Panel**: http://localhost:8001/admin/

## 📁 Project Structure

```
tenants/
├── README.md                          # This file
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables (gitignored)
├── fix_domain.py                      # Domain fixing utility
│
├── core_project/                      # Project configuration
│   ├── settings.py                    # Main Django settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI config
│   └── asgi.py                        # ASGI config
│
├── core/                              # Shared/public schema app
│   ├── models.py                      # User model (shared)
│   ├── views.py                       # Shared views
│   ├── admin.py                       # Admin configuration
│   ├── apps.py                        # App config
│   ├── tests.py                       # Tests
│   ├── migrations/                    # Database migrations
│   └── management/commands/           # Custom management commands
│       ├── create_dev_tenant.py       # Create dev tenant
│       └── fix_localhost_domain.py    # Fix domain mapping
│
├── tenants/                           # Tenant management app (public schema)
│   ├── models.py                      # Tenant & Domain models
│   ├── views.py                       # Tenant views (future)
│   ├── admin.py                       # Tenant admin
│   ├── apps.py                        # App config
│   ├── tests.py                       # Tests
│   └── migrations/                    # Database migrations
│
├── env/                               # Virtual environment (gitignored)
│   ├── bin/                           # Python executables
│   └── lib/                           # Installed packages
│
└── .gitignore                         # Git ignore file
```

## 🗄️ Database Schema

### Public Schema Tables

#### `tenants_tenant`
Stores information about each SaaS customer.

| Column | Type | Description |
|--------|------|-------------|
| id | BigAutoField | Primary key |
| schema_name | CharField | PostgreSQL schema name (e.g., tenant_dev) |
| name | CharField | Customer/company name |
| slug | SlugField | URL-friendly identifier |
| plan | CharField | Subscription plan (free, basic, premium, enterprise) |
| is_active | BooleanField | Whether tenant is active |
| created_at | DateTimeField | Creation timestamp |

#### `tenants_domain`
Maps domain names to tenants.

| Column | Type | Description |
|--------|------|-------------|
| id | BigAutoField | Primary key |
| domain | CharField | Domain name (e.g., localhost, acme.example.com) |
| is_primary | BooleanField | Primary domain flag |
| tenant_id | ForeignKey | Reference to Tenant |

#### `core_user`
Custom user model for authentication.

| Column | Type | Description |
|--------|------|-------------|
| id | BigAutoField | Primary key |
| username | CharField | Unique username |
| email | EmailField | Email address |
| password | CharField | Hashed password |
| role | CharField | User role (admin, owner, staff, user) |
| is_active | BooleanField | Whether user can login |
| is_staff | BooleanField | Admin access flag |
| date_joined | DateTimeField | Account creation time |
| last_login | DateTimeField | Last login timestamp |

### Tenant-Specific Schema Tables (Future)

These will be created per-tenant schema:

```
tenant_dev/
├── projects_project          # Project data
├── projects_task             # Task data
├── projects_comment          # Task comments
├── projects_attachment       # File attachments
└── projects_activity         # Audit log
```

## 🔌 API Documentation

### Authentication Endpoints (TODO)

#### Register New User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "password_confirm": "secure_password"
}

Response: 201 Created
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Health Check Endpoint

#### Check API Status
```http
GET /api/health/

Response: 200 OK
{
  "status": "healthy",
  "message": "TaskForce API is running"
}
```

### Project Endpoints (TODO)

```http
GET    /api/projects/               # List projects
POST   /api/projects/               # Create project
GET    /api/projects/{id}/          # Get project details
PUT    /api/projects/{id}/          # Update project
DELETE /api/projects/{id}/          # Delete project
```

### Task Endpoints (TODO)

```http
GET    /api/projects/{id}/tasks/    # List tasks
POST   /api/projects/{id}/tasks/    # Create task
GET    /api/tasks/{id}/             # Get task details
PUT    /api/tasks/{id}/             # Update task
DELETE /api/tasks/{id}/             # Delete task
```

### Tenant Management (TODO)

```http
GET    /api/tenants/me/             # Get current tenant
PUT    /api/tenants/me/             # Update tenant
GET    /api/tenants/members/        # List team members
POST   /api/tenants/members/        # Invite member
DELETE /api/tenants/members/{id}/   # Remove member
```

## 🔄 Development Workflow

### Creating a New Tenant

```bash
# Create a new tenant
python manage.py create_dev_tenant \
  --slug acme \
  --name "Acme Corporation" \
  --domain acme.local

# Add to /etc/hosts
echo "127.0.0.1   acme.local" | sudo tee -a /etc/hosts

# Access the tenant
# http://acme.local:8001/
```

### Adding Domain to Existing Tenant

```bash
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
django.setup()

from tenants.models import Tenant, Domain

tenant = Tenant.objects.get(slug='dev')
Domain.objects.create(
    domain='dev.example.com',
    tenant=tenant,
    is_primary=False
)
print('✓ Domain added')
"
```

### Running Migrations for All Tenants

```bash
# Migrate shared schema
python manage.py migrate_schemas --shared

# Migrate all tenant schemas
python manage.py migrate_schemas
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core
python manage.py test tenants
```

## 🏢 Multi-Tenancy Details

### Tenant Isolation

**Database Level**: Each tenant has a separate PostgreSQL schema
```sql
-- Public schema (shared by all tenants)
SELECT * FROM public.tenants_tenant;

-- Tenant-specific schema
SELECT * FROM tenant_dev.projects_project;
```

**Application Level**: Middleware automatically routes requests

```python
# In requests, the current tenant is available:
request.tenant  # Returns the Tenant object
request.tenant.schema_name  # Returns "tenant_dev"
```

### User Role-Based Access

| Role | Permissions | Description |
|------|-------------|-------------|
| Owner | Full control | Created tenant, manages billing |
| Admin | Admin access | Manage projects & team members |
| Member | Read/Write | Create & edit their own items |
| Viewer | Read-only | View projects only |

### Subscription Plans

| Plan | Max Projects | Max Tasks | Max Members | Price |
|------|-------------|-----------|------------|-------|
| Free | 1 | 10 | 3 | Free |
| Basic | 5 | 50 | 10 | $9/mo |
| Premium | 50 | 500 | 100 | $29/mo |
| Enterprise | Unlimited | Unlimited | Unlimited | Custom |

## 🐛 Troubleshooting

### Issue: "No tenant for hostname"

**Cause**: The domain in the request doesn't exist in the database.

**Solution**:
```bash
# Add the domain to your tenant
python manage.py fix_localhost_domain

# Or manually add it
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
django.setup()

from tenants.models import Tenant, Domain
tenant = Tenant.objects.get(slug='dev')
Domain.objects.create(domain='localhost', tenant=tenant)
"
```

### Issue: "Invalid string used for the schema name"

**Cause**: Slug contains invalid PostgreSQL schema characters (hyphens, special chars).

**Solution**: The model now auto-converts slugs. Use alphanumeric characters and underscores:
```bash
python manage.py create_dev_tenant --slug my_tenant --name "My Tenant"
```

### Issue: PostgreSQL Connection Error

**Cause**: PostgreSQL not running or credentials incorrect.

**Solution**:
```bash
# Check PostgreSQL is running
psql -U tenant_user -d tenants -h localhost

# Verify .env credentials
cat .env | grep DB_

# Start PostgreSQL (macOS)
brew services start postgresql
```

### Issue: Redis Connection Error

**Cause**: Redis not running (optional, can disable).

**Solution**:
```bash
# Start Redis (macOS)
brew services start redis

# Or disable caching in settings.py (not recommended)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

## 📝 Environment Variables Reference

```env
# Database Configuration
DB_NAME=tenants                 # PostgreSQL database name
DB_USER=tenant_user             # PostgreSQL user
DB_PASSWORD=secure_password     # PostgreSQL password
DB_HOST=localhost               # PostgreSQL host
DB_PORT=5432                    # PostgreSQL port

# Django Configuration
SECRET_KEY=your-secret-key      # Django secret (change in production!)
DEBUG=True                      # Debug mode (set to False in production)
ALLOWED_HOSTS=localhost,127.0.0.1  # Allowed hostnames

# Redis Configuration (optional)
REDIS_HOST=127.0.0.1            # Redis host
REDIS_PORT=6379                 # Redis port
REDIS_DB=1                      # Redis database number
```

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure PostgreSQL for production
- [ ] Set up Redis for caching
- [ ] Configure static files with WhiteNoise
- [ ] Set up SSL/TLS certificates
- [ ] Configure email backend for notifications
- [ ] Set up Celery worker for async tasks
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging

### Using Gunicorn
```bash
# Install gunicorn (already in requirements.txt)
gunicorn core_project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync
```

### Using Docker (Future)
```bash
docker-compose up -d
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [django-tenants Documentation](https://django-tenants.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Last Updated**: December 23, 2025  
**Version**: 1.0.0 (MVP - Core Infrastructure Complete)
