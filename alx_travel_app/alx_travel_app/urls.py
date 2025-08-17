from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel API",
      default_version='v1',
      description="API documentation for ALX Travel App listing service",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('listings.urls')), 
    path('api/payments/', include('listings.urls')),  # Assuming payments are handled in listings app
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("payments/initiate/", views.initiate_payment, name="initiate_payment"),
    path("payments/verify/<str:tx_ref>/", views.verify_payment, name="verify_payment"),
]

