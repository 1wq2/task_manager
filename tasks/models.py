from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser
from task_manager import settings


class UserRole(models.Model):
    MANAGER = 'Manager'
    DEVELOPER = 'Developer'
    ROLES = (
        (MANAGER, MANAGER),
        (DEVELOPER, DEVELOPER)
    )
    role_name = models.CharField(max_length=15, choices=ROLES, default=DEVELOPER)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    role = models.ForeignKey(UserRole, null=True, blank=False, on_delete=models.CASCADE)


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=2000, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + self.description


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='task', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    due_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    assigned_date = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + '-' + self.description





