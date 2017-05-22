from django.conf.urls import url, include
from .models import Board, Thread
from rest_framework import serializers, viewsets
from rest_framework_nested import routers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

# Serializers define the API representation.
class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ["name"]

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = ["id", "board", "subject"]

# ViewSets define the view behavior.
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ThreadByBoardViewSet(ThreadViewSet):
    def list(self, request, board_pk=None):
        queryset = self.queryset.filter(board=board_pk)
        serializer = ThreadSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def retreive(self, request, board_pk=None):
        queryset = self.queryset.filter(board=board_pk)
        thread = get_object_or_404(queryset, board=board_pk)
        serializer = ThreadSerializer(threads, many=True, context={'request':request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
