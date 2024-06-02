from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from admin_notification.views import check_notification_view
admin.site.site_header = 'Pharmacy Online Care'

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("api-v1/", include("api.urls")),
    path('check/notification', check_notification_view, name="check_notifications"),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("user/", include("userauths.urls")),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
