from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('knowme.common.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('knowme.accounts.urls')),
    path('posts/', include('knowme.posts.urls')),
    path('direct/', include('knowme.direct.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
