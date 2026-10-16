from django.urls import path
from . import views

urlpatterns = [
    path('', views.scholarship_list, name='scholarship_list'),
    path('add/', views.scholarship_create, name='scholarship_create'),
    path('<int:pk>/edit/', views.scholarship_update, name='scholarship_update'),
    path('<int:pk>/delete/', views.scholarship_delete, name='scholarship_delete'),
]