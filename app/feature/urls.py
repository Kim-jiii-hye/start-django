from django.urls import path, include
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger 문서 설정
schema_view = get_schema_view(
    openapi.Info(
        title="Subscribe API",
        default_version='v1',
        description="Subscribe API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@subscribe.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        path('api/subscribe/', include('app.feature.subscribe.urls')),
    ],
)

urlpatterns = [
    path('api/hello/', views.hello_world, name='hello_world'),
    path('api/subscribe/', include('app.feature.subscribe.urls')),

    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]