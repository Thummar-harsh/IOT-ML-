from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    # path("aboutus/", views.about, name="about"),
    path('delete/<int:pk>/', views.delete_data, name='delete_data'),
    path('add/', views.add_data, name='add_data'),
    # path('Edit/', views.Edit_data, name='Edit_data'),
    path('edit/<int:pk>/', views.edit_data, name='edit_data'),
    path('prediction_data', views.prediction_data, name='prediction_data'),
    path('submit_data_ajax/', views.submit_data_ajax, name='submit_data_ajax'),
]