from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('archive/', include('archive.urls', namespace='archive')),
    path('lending/', include('lending.urls', namespace='lending')),
    path('permissions/', include('permissions.urls', namespace='permissions')),
    path('review/', include('review.urls', namespace='review')),
    path('search/', include('search.urls', namespace='search')),
    path('', include('inventory.urls', namespace='inventory')),  # ルートは備品一覧
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)