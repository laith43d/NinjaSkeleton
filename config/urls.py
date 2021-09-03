from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from ninja import NinjaAPI

api = NinjaAPI(
    version='1.0.0',
    title='client API v1',
    description='API documentation',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]

# if settings.DEBUG:
#     urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
