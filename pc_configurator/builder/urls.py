from django.urls import path
from . import views

urlpatterns = [
    path('', views.configurator, name='configurator'),
    path('catalog/', views.catalog, name='catalog'),
    path('component/<str:model_type>/<int:pk>/', views.component_detail, name='component_detail'),
    path('my-builds/', views.my_builds, name='my_builds'),
    path('save-build/', views.save_build, name='save_build'),
    path('load-build/<int:build_id>/', views.load_build, name='load_build'),
    path('about/', views.about, name='about'),
]