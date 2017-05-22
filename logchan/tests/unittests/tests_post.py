from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.core.urlresolvers import reverse

from logchan.models import Board, Thread, Post

class RestApiTestPost(TestCase):
    def setUp(self):
        self.dumBoard = Board(name='TestBoard')
        self.dumBoard.save()
        self.dumThread = Thread(board=self.dumBoard, subject='TestThread')
        self.dumThread.save()
        self.dumPost = Post(thread=self.dumThread, user_name='testUser',
            deletion_password='hdfkhnlf', message='Test message')
        self.dumPost.save()

    def test_message_post(self):
        client = APIClient()
        threadUrl = '/api/thread/{}/'.format(self.dumThread.id)
        data = {
            'thread': threadUrl,
            'message': 'test message',
            'user_name': 'user',
            'deletion_password': 'jsdfhbd',
        }

        postMessage = 'Test post'
        request = client.post('/api/post/', data, format='json')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_message_get(self):
        client = APIClient()
        url = '/api/post/{}/'.format(self.dumPost.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_delete(self):
        p = Post(thread=self.dumThread, user_name='testUser',
            deletion_password='hdfkhnlf', message='Test message')
        p.save()
        client = APIClient()
        url = '/api/thread/{}/post/{}/'.format(self.dumThread.id, p.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_message_by_thread_post(self):
        client = APIClient()
        threadUrl = '/api/thread/{}/'.format(self.dumThread.id)
        data = {
            'thread': threadUrl,
            'message': 'test message',
            'user_name': 'user',
            'deletion_password': 'jsdfhbd',
        }

        postMessage = 'Test post'
        request = client.post('/api/thread/{}/post/'.format(self.dumThread.id),
            data, format='json')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_message_by_thread_get(self):
        client = APIClient()
        url = '/api/post/{}/'.format(self.dumPost.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_by_thread_delete(self):
        p = Post(thread=self.dumThread, user_name='testUser',
            deletion_password='hdfkhnlf', message='Test message')
        p.save()
        client = APIClient()
        url = '/api/thread/{}/post/{}/'.format(self.dumThread.id, p.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
## Test view
# https://github.com/erkarl/django-rest-framework-oauth2-provider-example/blob/master/apps/users/tests.py
