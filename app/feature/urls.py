from django.urls import path
from . import views

urlpatterns = [
    path('api/hello/', views.hello_world, name='hello_world'),
]