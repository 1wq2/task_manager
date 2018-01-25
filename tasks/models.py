from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Permission, User

from django.contrib.auth.models import AbstractUser, BaseUserManager
from task_manager import settings

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,

        )
        # user.is_admin = True
        user.save(using=self._db)
        return user


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
    tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        return self.tasks



class Project(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)

    project_title = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    tasks = []


    def add_task(self, task):
        self.tasks.append(task)
        return self.tasks

    def __str__(self):
       return self.project_title

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='task', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length=100)
    task_due_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    assigned_date = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.task_title + '-' + self.task_description + '-' + self.task_due_date




