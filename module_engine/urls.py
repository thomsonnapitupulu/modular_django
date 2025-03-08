# module_engine/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_list, name='module_list'),
    path('<int:module_id>/install/', views.install_module, name='install_module'),
    path('<int:module_id>/upgrade/', views.upgrade_module, name='upgrade_module'),
    path('<int:module_id>/uninstall/', views.uninstall_module, name='uninstall_module'),
]