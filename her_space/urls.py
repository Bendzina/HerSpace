"""
URL configuration for her_space project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="HerSpace API",
      default_version='v1',
      description="API documentation for HerSpace",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/journal/', include('journal.urls')),
    path('api/motherhood/', include('motherhood.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/community/', include('community.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/wellness/', include('wellness.urls')),
]
# Add Swagger UI URLs
urlpatterns += [
    path('api/schema/swagger-ui/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development - must be after all other URL patterns
if settings.DEBUG:
    from django.contrib.staticfiles.views import serve
    from django.views.decorators.cache import never_cache
    
    # Serve media files with proper headers
    urlpatterns += [
        path('media/<path:path>', never_cache(serve), {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    ]