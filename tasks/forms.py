from django import forms
from .models import Project, Task

from django.contrib.auth import get_user_model
User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    """is_staff for Developer(optinal) 
       is_staff + is_superuser for Manager"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser']

        #fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'role_id')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['id', 'title']

        # fields = ('id', 'title', 'description', 'created_date', 'users_ids', 'users' )


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date']

        #fields = ('id', 'project_id', 'user_id', 'project', 'user', 'title',
        #          'description', 'created_date', 'due_date', 'assigned_date')