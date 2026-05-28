from django.contrib import admin
from django.urls import path
from builder import views   # импортируем views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.configurator, name='configurator'),   # главная страница будет конфигуратором
]