# Contributing to TaskForce

## Development Setup

### 1. Clone and Setup
```bash
git clone <repo-url>
cd tenants
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env  # Copy and fill in your values
python manage.py migrate_schemas --shared
python manage.py create_dev_tenant
```

### 3. Run Development Server
```bash
python manage.py runserver 0.0.0.0:8001
```

## Project Roadmap

### Phase 1: Core Infrastructure ✅ COMPLETE
- [x] Multi-tenant setup with schema isolation
- [x] Authentication & User model
- [x] Admin interface
- [x] Domain routing
- [x] Health check endpoint

### Phase 2: Project Management (NEXT)
- [ ] Create `projects` app
- [ ] Implement Project model
- [ ] Implement Task model
- [ ] Build Project & Task APIs
- [ ] Add task assignment logic

### Phase 3: Collaboration Features
- [ ] Comments on tasks
- [ ] File attachments
- [ ] Activity audit logging
- [ ] Real-time notifications

### Phase 4: Analytics & Reporting
- [ ] Usage analytics
- [ ] Project reports
- [ ] Team performance metrics

### Phase 5: Frontend
- [ ] React/Vue dashboard
- [ ] Project views
- [ ] Task board (Kanban)

## Creating a New App

### 1. Create the App
```bash
python manage.py startapp myapp
```

### 2. Register in Settings
For **shared** apps (all tenants see it):
```python
# In SHARED_APPS
SHARED_APPS = [
    # ... existing apps
    'myapp',
]
```

For **tenant-specific** apps (isolated per tenant):
```python
# In TENANT_APPS
TENANT_APPS = [
    # ... existing apps
    'myapp',
]
```

### 3. Create Models
```python
# In myapp/models.py
from core.models import TenantModel

class MyModel(TenantModel):
    """Tenant-isolated model"""
    name = models.CharField(max_length=255)
    
    class Meta:
        # Required for tenant apps
        app_label = 'myapp'
```

### 4. Create Migrations
```bash
python manage.py makemigrations myapp
python manage.py migrate_schemas
```

### 5. Create Serializers
```python
# In myapp/serializers.py
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'created_at']
```

### 6. Create Views
```python
# In myapp/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]
```

### 7. Register URLs
```python
# In core_project/urls.py
from rest_framework.routers import DefaultRouter
from myapp.views import MyModelViewSet

router = DefaultRouter()
router.register(r'mymodels', MyModelViewSet)

urlpatterns = [
    # ... existing patterns
    path('api/', include(router.urls)),
]
```

## Code Style Guide

### Python
- Follow PEP 8
- Use 4 spaces for indentation
- Line length max 88 characters
- Use type hints where possible

```python
def get_user_projects(user: User) -> QuerySet:
    """Get all projects for a user."""
    return Project.objects.filter(created_by=user)
```

### Django Models
```python
class Project(TenantModel):
    """Detailed docstring about the model."""
    
    # Fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Methods
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['-created_at']
```

### Views & Serializers
```python
class ProjectSerializer(serializers.ModelSerializer):
    """Serialize Project model."""
    
    created_by_name = serializers.CharField(
        source='created_by.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'created_by_name', 'created_at']
```

## Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test projects

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Write Tests
```python
# In myapp/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectTestCase(TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_project_creation(self):
        """Test creating a project."""
        project = Project.objects.create(
            name='Test Project',
            created_by=self.user
        )
        self.assertEqual(project.name, 'Test Project')
```

## Git Workflow

### Branch Naming
- `feature/` - New feature (e.g., `feature/task-comments`)
- `bugfix/` - Bug fix (e.g., `bugfix/domain-routing`)
- `docs/` - Documentation (e.g., `docs/api-guide`)

### Commit Messages
```
[TAG] Brief description

Longer explanation if needed.

- Bullet point 1
- Bullet point 2
```

Tags: `[FEAT]`, `[FIX]`, `[DOCS]`, `[TEST]`, `[REFACTOR]`

Example:
```
[FEAT] Add task assignment API endpoint

Implements endpoint to assign tasks to team members.
Includes proper permission checks and audit logging.

- POST /api/tasks/{id}/assign/
- Requires admin or owner role
- Returns 200 with updated task
```

### Pull Request Process
1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push to repository: `git push origin feature/my-feature`
4. Create pull request on GitHub
5. Wait for review and tests to pass
6. Merge when approved

## Database Migrations

### Creating Migrations
```bash
python manage.py makemigrations myapp
```

### Applying Migrations
```bash
# Shared schema only
python manage.py migrate_schemas --shared

# All tenant schemas
python manage.py migrate_schemas
```

### Rolling Back
```bash
python manage.py migrate_schemas myapp 0001_initial
```

## Debugging

### Django Shell
```bash
python manage.py shell

# Once in shell:
from tenants.models import Tenant
from projects.models import Project

tenant = Tenant.objects.first()
projects = Project.objects.filter(created_by=tenant.user_set.first())
```

### Debug SQL Queries
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    Project.objects.all().count()
    print(context.captured_queries)
```

### Print Debug Info
```python
from django.utils import timezone
import json

@api_view(['GET'])
def debug_view(request):
    """Debug endpoint."""
    return Response({
        'tenant': str(request.tenant),
        'user': str(request.user),
        'timestamp': timezone.now().isoformat(),
    })
```

## Performance Tips

1. **Use select_related() for ForeignKeys**
   ```python
   projects = Project.objects.select_related('created_by')
   ```

2. **Use prefetch_related() for ManyToMany**
   ```python
   tasks = Task.objects.prefetch_related('comments')
   ```

3. **Use only() to select specific fields**
   ```python
   projects = Project.objects.only('name', 'created_at')
   ```

4. **Add database indexes**
   ```python
   class Project(TenantModel):
       name = models.CharField(max_length=255, db_index=True)
   ```

## Documentation

- Update README.md for major changes
- Add docstrings to all functions/classes
- Comment complex logic
- Include examples for APIs

## Questions?

- Check existing issues for similar problems
- Review code in the repository
- Check Django and django-tenants docs
- Open a GitHub issue with detailed description

---

**Happy coding!** 🎉
