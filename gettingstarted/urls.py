from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import logchan.views
import logchan.api

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', logchan.views.index, name='index'),
    url(r'^board/(?P<board_name>[^/]+)/$', logchan.views.board, name='board'),
    url(r'^api/', include(logchan.api)),
    # url(r'^admin/', include(admin.site.urls)),
]
