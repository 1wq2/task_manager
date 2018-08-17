from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView
from django.urls import path

app_name = 'tasks'

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user/$', LoginView.as_view(template_name='tasks/login.html'), name='login_user'),
    url(r'^logout_user/$', LogoutView.as_view(template_name='tasks/login.html'), name='logout_user'),
    path('admin/', RedirectView.as_view(url='http://127.0.0.1:8000/admin'), name='admin'),  # for full crud as superuser

    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'task/add/$', views.TaskCreate.as_view(), name='task-add'),
    url(r'task/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='task-update'),
    url(r'task/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='task-delete'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^tasks/$', views.TaskList.as_view(), name='task-list'),
    url(r'^roles/$', views.RoleList.as_view(), name='role-list'),
    url(r'^projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetail.as_view(), name='task-detail'),
    url(r'^projects/(?P<pk>[0-9]+)$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^users/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/(?P<pk>[0-9]+)/projects', views.UserProjects.as_view(), name='user-projects'),
    url(r'^projects/(?P<pk>[0-9]+)/users$', views.ProjectUsers.as_view(), name='project-users'),
    url(r'^projects/(?P<pk>[0-9]+)/tasks$', views.ProjectTasks.as_view(), name='project-tasks')




]