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
        self.dumPost = Post(thread=self.dumThread, date=datetime.now(), user_name='testUser',
            deletion_password='hdfkhnlf', message='Test message')
        self.dumPost.save()

    def test_message_post(self):
        client = APIClient()
        data = {
            'message': 'test message',
            'date': datetime.now(),
            'user_name': 'user',
            'deletion_password': 'jsdfhbd',
        }
        post = Post(thread=self.dumThread, date=data['date'], user_name=data['user_name'],
            deletion_password=data['deletion_password'], message=data['message'])

        postMessage = 'Test post'
        request = client.post('/api/board/{}/{}/'.format(self.dumBoard.name, 
            self.dumThread.subject), data, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(thread_contain_post(self.thread, post), True)

    def test_message_get(self):
        self.assertEquals(True, False)
        client = APIClient()
        url = '/api/board/{}/{}/'.format(testBoard, testThread)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 'subject': testThread })

    def test_message_put(self):
        # TODO
        self.assertEquals(True, False)
        client = APIClient()
        url = '/api/board/{}/{}/'.format(testBoard, testThread)
        newName = 'new'
        request = client.put(url, data={'subject': newName}, content_type='json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        t = Thread.objects.get(board=testBoard, subject=threadName)
        self.assertEqual(newName, t.subject)

    def thread_contain_post(thread, post):
        posts = Post.objects.get(thread=threadName)
        for p in posts:
            if(p.message == post.message and p.date == post.date 
                and p.user_name == post.user_name):
                return True
        return False

## Test view
# https://github.com/erkarl/django-rest-framework-oauth2-provider-example/blob/master/apps/users/tests.py
