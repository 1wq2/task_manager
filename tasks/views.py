from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.urls import reverse_lazy

from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasScope, TokenHasReadWriteScope

from tasks.models import Task, Project, UserRole
from tasks.utils.exceptions import ResourceNotFoundException
from tasks.serializers import UserSerializer, UserRoleSerializer,  TaskSerializer, \
                            ProjectSerializer, ProjectTasksSerializer


from django.contrib.auth import login
User = get_user_model()


class VisitorView(generic.TemplateView):
    template_name = 'tasks/base_visitor.html'


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/tasks/login_user'
    redirect_field_name = 'redirect_to'

    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        print(self.request.user)
        return Task.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/tasks/login_user'
    redirect_field_name = 'redirect_to'

    model = Task
    template_name = 'tasks/detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    login_url = '/tasks/login_user'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['task_title', 'task_description', 'task_due_date',  'created_date', 'assigned_date']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login_user/'
    redirect_field_name = 'redirect_to'

    model = Task
    fields = ['task_title', 'task_description', 'task_due_date', 'created_date', 'assigned_date']

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


def get_object(_model, pk):
    try:
        return _model.objects.get(pk=pk)
    except _model.DoesNotExist:
        raise ResourceNotFoundException


class UserList(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        users = User.objects.order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, pk, format=None):
        try:
            user = get_object(User, pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)

    def put(self, request, pk, format=None):
        try:
            user = get_object(User, pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)

    def delete(self, request, pk, format=None):
        user = get_object(User, pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleList(APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def get(self, request, format=None):
        user_roles = UserRole.objects.all()
        serializer = UserRoleSerializer(user_roles, many=True)
        return Response(serializer.data)


class TaskList(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        tasks = Task.objects.order_by('-created_date')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetail(APIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = TaskSerializer

    def get(self, request, pk, format=None):
        try:
            task = get_object(Task, pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)

    def put(self, request, pk, format=None):
        try:
            task = get_object(Task, pk)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)

    def delete(self, request, pk, format=None):
        task = get_object(Task, pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectList(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        projects = Project.objects.order_by('-created_date')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetail(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, pk, format=None):
        try:
            project = get_object(Project, pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)

    def put(self, request, pk, format=None):
        try:
            project = get_object(Project, pk)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)

    def delete(self, request, pk, format=None):
        project = get_object(Project, pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectTasks(APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def get(self, request, pk, format=None):
        try:
            project = get_object(Project, pk)
            tasks = project.tasks.order_by('-created_date')
            serializer = ProjectTasksSerializer(tasks, many=True)
            return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)


class UserProjects(APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def get(self, request, pk, format=None):
        try:
            user = get_object(User, pk)
            projects = user.projects.order_by('-created_date')
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)


class ProjectUsers(APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def get(self, request, pk, format=None):
        try:
            project = get_object(Project, pk)
            users = project.users.order_by('-date_joined')
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except ResourceNotFoundException as exc:
            return Response(data=exc.data, status=exc.status_code)