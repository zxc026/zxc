from django.urls import path
from . import views

urlpatterns = [
    path('', views.configurator, name='configurator'),
    path('catalog/', views.catalog, name='catalog'),
    path('component/<str:model_type>/<int:pk>/', views.component_detail, name='component_detail'),
]