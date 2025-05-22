from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supplies/', include('supplies.urls', namespace='supplies')),
    path('archive/', include('archive.urls', namespace='archive')),
    path('lending/', include('lending.urls', namespace='lending')),
    path('accounts/', include('accounts.urls', namespace='accounts')),  # permissions→accounts
    # path('review/', include('review.urls', namespace='review')),  # reviewアプリ削除のためコメントアウトまたは削除
    path('search/', include('search.urls', namespace='search')),
    path('', include('supplies.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)