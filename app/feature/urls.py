from django.urls import path, include
from . import views

urlpatterns = [
    path('api/hello/', views.hello_world, name='hello_world'),
    path('api/subscribe/', include('app.feature.subscribe.urls')),
]