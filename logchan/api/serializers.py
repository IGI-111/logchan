from rest_framework import serializers
from ..models import Board, Thread

# Serializers define the API representation.
class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ["name"]

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = ["id", "board", "subject"]
