from django.conf.urls import url
from . import views



urlpatterns = [

url(r'^$', views.VisitorView.as_view(), name='base_visitor'),
]