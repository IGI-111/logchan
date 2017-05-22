from django.conf.urls import url, include
from rest_framework_nested import routers
from .viewsets import BoardViewSet, ThreadViewSet, ThreadByBoardViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'board', BoardViewSet)
router.register(r'thread', ThreadViewSet)

board_router = routers.NestedSimpleRouter(router, r'board', lookup='board')
board_router.register(r'thread', ThreadByBoardViewSet, base_name='board-thread')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(board_router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]