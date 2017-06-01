from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

import logchan.views
import logchan.api

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', logchan.views.index, name='index'),
    url(r'^login', logchan.views.login, name='login'),
    url(r'^api/', include(logchan.api)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<board_name>[^/]+)/$', logchan.views.board, name='board'),
    url(r'^(?P<board_name>[^/]+)/(?P<thread_id>[^/]+)/$', logchan.views.thread, name='board'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
