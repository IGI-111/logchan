from django.conf.urls import url, include
from .models import Board, Thread
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

# ViewSets define the view behavior.
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'threads', ThreadViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]