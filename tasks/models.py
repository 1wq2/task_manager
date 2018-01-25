from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.models import Permission, User

from django.contrib.auth.models import AbstractUser, BaseUserManager

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



class User(AbstractUser):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    projects = []
    tasks = []

    def add_project(self, project):
        self.projects.append(project)
        project.add_user(self)

    def add_task(self, task):
        self.tasks.append(task)
        return self.tasks

class Project(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    project_title = models.CharField(max_length=100)
    users = []
    tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        return self.tasks

    def add_user(self, user):
        self.users.append(user)
        user.add_project(self)

    def __str__(self):
       return self.project_title

class Task(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, default=1, on_delete=models.CASCADE)

    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length=100)
    task_due_date = models.CharField(max_length=100)


    def get_absolute_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.task_title + '-' + self.task_description + '-' + self.task_due_date




