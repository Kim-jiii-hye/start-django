from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscribeViewSet

router = DefaultRouter()
router.register(r'subscribes', SubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', SubscribeViewSet.as_view({'post': 'list_by_params'})),
] 