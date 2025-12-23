# Quick Start Guide - TaskForce

Get TaskForce running in **5 minutes**.

## Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Git

## Installation

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd tenants
```

### 2️⃣ Setup Virtual Environment
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment
Create `.env` file:
```bash
cat > .env << 'EOF'
# PostgreSQL
DB_NAME=tenants
DB_USER=tenant_user
DB_PASSWORD=tenant_user
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-change-in-production
EOF
```

### 5️⃣ Initialize Database
```bash
# Migrate shared schema
python manage.py migrate_schemas --shared

# Create dev tenant
python manage.py create_dev_tenant

# Create superuser (for admin)
python manage.py createsuperuser
```

### 6️⃣ Start Server
```bash
python manage.py runserver 0.0.0.0:8001
```

## Access the App

| URL | Purpose |
|-----|---------|
| http://localhost:8001/api/health/ | API Health Check |
| http://localhost:8001/admin/ | Admin Panel |

**Admin Credentials**: Use the superuser you created in step 5

## Next Steps

### Create Another Tenant
```bash
python manage.py create_dev_tenant --slug acme --name "Acme Corp"
```

### Test the API
```bash
# Health check
curl http://localhost:8001/api/health/

# Admin login
# Use admin panel at http://localhost:8001/admin/
```

### View Database
```bash
# Enter PostgreSQL shell
psql -U tenant_user -d tenants

# List schemas
\dn

# List tables in public schema
\dt public.*

# List tables in tenant schema
\dt tenant_dev.*
```

## Development Commands

```bash
# Run tests
python manage.py test

# Make migrations
python manage.py makemigrations appname

# Apply migrations
python manage.py migrate_schemas

# Shell access
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## Troubleshooting

### PostgreSQL Won't Start
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 0.0.0.0:8002
```

### "No tenant for hostname"
```bash
# Add localhost domain
python manage.py fix_localhost_domain
```

### Database Error
```bash
# Check PostgreSQL is running and accessible
psql -U tenant_user -d tenants -h localhost

# Check .env file has correct credentials
cat .env
```

## Project Structure

```
tenants/
├── README.md              # Full documentation
├── CONTRIBUTING.md        # Development guide
├── QUICK_START.md         # This file
├── manage.py
├── requirements.txt
├── .env                   # Your config (not in git)
│
├── core_project/          # Django config
├── core/                  # Shared app (User model)
├── tenants/               # Tenant management app
├── env/                   # Virtual environment
└── .git/                  # Git repository
```

## What's Implemented?

✅ Multi-tenant architecture  
✅ Schema-based isolation  
✅ Custom user model  
✅ JWT authentication setup  
✅ Admin interface  
✅ Domain routing  

## What's Next?

Next step is building the business logic:
1. Create `projects` app
2. Add Project and Task models
3. Build APIs for CRUD operations
4. Add collaboration features

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guides.

## Need Help?

- 📖 Read [README.md](README.md) for full documentation
- 🔧 Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guide
- 🐛 Review [README.md#troubleshooting](README.md#troubleshooting) for common issues
- 💬 Open a GitHub issue for questions

---

**You're all set!** 🚀

Now explore the admin panel and start building your features.
