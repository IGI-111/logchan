from rest_framework import viewsets
from .serializers import BoardSerializer, ThreadSerializer, PostSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Board, Thread, Post

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
        serializer = ThreadSerializer(thread, context={'request':request})
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostByThreadViewSet(PostViewSet):
    def list(self, request, thread_pk=None):
        queryset = self.queryset.filter(thread=thread_pk)
        serializer = PostSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def retreive(self, request, thread_pk=None):
        queryset = self.queryset.filter(thread=thread_pk)
        post = get_object_or_404(queryset, thread=thread_pk)
        serializer = ThreadSerializer(post, context={'request':request})
        return Response(serializer.data)
