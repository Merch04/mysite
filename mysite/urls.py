from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('polls/', include('polls.urls'), name="period"),
    path('admin/', admin.site.urls),
    path('', include('authorization.urls')),
    path('/login', LogoutView.as_view(template_name="index.html"), name="logout"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
