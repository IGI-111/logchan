from rest_framework import viewsets
from .serializers import BoardSerializer, ThreadSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Board, Thread, Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from ..templatetags import logchan_extras
from ..api import *

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

    def create(self, request):
        if request.user is not None and logchan_extras.is_in_group(request.user, "Admin") or (
                grecaptcha_verify(request)):
            return super(ThreadViewSet, self).create(request)
        else:
            return Response('Captcha not validated', status=status.HTTP_400_BAD_REQUEST)
class ThreadByBoardViewSet(ThreadViewSet):
    def list(self, request, board_pk=None):
        queryset = self.queryset.filter(board=board_pk)
        serializer = ThreadSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def create(self, request):
        if request.user is not None and logchan_extras.is_in_group(request.user, "Admin") or (
                grecaptcha_verify(request)):
            return super(ThreadViewSet, self).create(request)
        else:
            return Response('Captcha not validated', status=status.HTTP_400_BAD_REQUEST)

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

    def create(self, request):
        if request.user is not None and logchan_extras.is_in_group(request.user, "Admin") or (
                grecaptcha_verify(request)):
            return super(ThreadViewSet, self).create(request)
        else:
            return Response('Captcha not validated', status=status.HTTP_400_BAD_REQUEST)

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

