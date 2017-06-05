from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group

from logchan.models import Board, Thread, Post

class RestApiTestPostNotLoggedIn(TestCase):
    def setUp(self):
        self.dumBoard = Board(name='TestBoard')
        self.dumBoard.save()
        self.dumThread = Thread(board=self.dumBoard, subject='TestThread')
        self.dumThread.save()
        self.dumPost = Post(thread=self.dumThread, user_name='testUser',
            message='Test message')
        self.dumPost.save()

    def test_message_post(self):
        client = APIClient()
        postMessage = 'Test post'
        data = {
            'thread': self.dumThread.id,
            'message': 'test message',
            'user_name': 'user',
        }

        request = client.post('/api/post/', data, format='json')

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_message_get(self):
        client = APIClient()
        url = '/api/post/{}/'.format(self.dumPost.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_delete(self):
        p = Post(thread=self.dumThread, user_name='testUser',
            message='Test message')
        p.save()
        client = APIClient()
        url = '/api/post/{}/'.format(p.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_message_by_thread_get(self):
        client = APIClient()
        url = '/api/thread/{}/post/{}/'.format(self.dumThread.id, self.dumPost.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_by_thread_delete(self):
        p = Post(thread=self.dumThread, user_name='testUser',
            message='Test message')
        p.save()
        client = APIClient()
        url = '/api/thread/{}/post/{}/'.format(self.dumThread.id, p.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

