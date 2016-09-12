from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin
#admin.site.site_title = 'Stream Repo Server Site Modification'
#admin.site.site_header = 'TIMS(TEST INPUT MANAGEMENT SYSTEM)'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tims/', include(admin.site.urls)),
    url(r'^tims/', include('myproject.tims.urls')),
    url(r'^$', RedirectView.as_view(url='/admin/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
