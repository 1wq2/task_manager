from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Project, Task
from django.http import HttpResponse
from django.template import loader

from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin

#############################

from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

################
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
################

from django.contrib.auth import login

class VisitorView(generic.TemplateView):
    template_name = 'tasks/base_visitor.html'

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/tasks/login_user'
    redirect_field_name = 'redirect_to'

    template_name = 'tasks/index.html'
    context_object_name = 'tasks' #all_samples

    def get_queryset(self):
        print(self.request.user)
        return Task.objects.filter(user=self.request.user)
        #return Task.objects.all()


class DetailView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/tasks/login_user'
    redirect_field_name = 'redirect_to'

    model = Task
    template_name = 'tasks/detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    login_url = '/tasks/login_user'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['task_title', 'task_description', 'task_due_date']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login_user/'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['task_title', 'task_description', 'task_due_date']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(TaskUpdate, self).form_valid(form)

class TaskDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login_user/'
    redirect_field_name = 'redirect_to'

    model = Task
    success_url = reverse_lazy('tasks:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'tasks/register.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tasks:index')
        return render(request, self.template_name, {'form': form})


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """ List all of the notes for a user """
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('-pub_date')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer