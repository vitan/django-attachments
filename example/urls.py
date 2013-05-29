from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Enable the admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.home'),
    url(r'^message/(?P<id>.+)$', 'core.views.message', name='message_detail'),
    url(r'^attachments/', include('attachments.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
