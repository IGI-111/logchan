from django.conf.urls import url, include
import requests
from rest_framework_nested import routers
from rest_framework import response, decorators
from .viewsets import BoardViewSet, ThreadViewSet, ThreadByBoardViewSet, PostByThreadViewSet, PostViewSet
from django.conf import settings
from rest_framework.response import Response
from .viewsets import grecaptcha_verify

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'board', BoardViewSet)
router.register(r'thread', ThreadViewSet)
router.register(r'post', PostViewSet)

board_router = routers.NestedSimpleRouter(router, r'board', lookup='board')
board_router.register(r'thread', ThreadByBoardViewSet, base_name='board-thread')

thread_router = routers.NestedSimpleRouter(router, r'thread', lookup='thread')
thread_router.register(r'post', PostByThreadViewSet, base_name='thread-post')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(board_router.urls)),
    url(r'^', include(thread_router.urls)),
]

@decorators.api_view(['POST'])
def captcha(request):
    if not grecaptcha_verify(request):
        return Response('Captcha not validated', status=status.HTTP_400_BAD_REQUEST)
    return response.Response(data)
