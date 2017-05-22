from rest_framework import serializers
from ..models import Board, Thread, Post

# Serializers define the API representation.
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["name"]

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ["id", "board", "subject"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "thread", "date", "user_name", "image", "message"]
