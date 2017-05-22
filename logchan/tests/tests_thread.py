from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.core.urlresolvers import reverse

from logchan.models import Board, Thread, Post

class RestApiTestThread(TestCase):
    def setUp(self):
        self.dumBoard = Board(name='TestBoard')
        self.dumBoard.save()
        self.dumThread = Thread(board=self.dumBoard, subject='TestThread')
        self.dumThread.save()

    def test_thread_post(self):
        client = APIClient()
        threadName = 'Test thread'
        boardUrl = '/api/board/{}/'.format(self.dumBoard.name)
        request = client.post('/api/thread/', {'board': boardUrl, 'subject': threadName}, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.get(board=self.dumBoard.name, subject=threadName).subject, threadName)

    def test_thread_get(self):
        client = APIClient()
        url = '/api/thread/{}/'.format(self.dumThread.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], self.dumThread.subject)
        self.assertEqual(response.data['id'], self.dumThread.id)
        self.assertEqual(self.dumThread.board.name in response.data['board'], True)

    def test_thread_delete(self):
        testThread = Thread(subject='Test tt', board=self.dumBoard)
        testThread.save()
        client = APIClient()

        url = '/api/thread/{}/'.format(testThread.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_thread_by_board_post(self):
        client = APIClient()
        threadName = 'Test thread'
        boardUrl = '/api/board/{}/'.format(self.dumBoard.name)
        print(boardUrl)
        request = client.post('{}/thread/'.format(boardUrl), {'board': boardUrl, 'subject': threadName}, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.get(board=self.dumBoard.name, subject=threadName).subject, threadName)

    def test_thread_by_board_get(self):
        client = APIClient()
        url = '/api/board/{}/thread/{}/'.format(self.dumBoard.name, self.dumThread.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], self.dumThread.subject)
        self.assertEqual(response.data['id'], self.dumThread.id)
        self.assertEqual(self.dumThread.board.name in response.data['board'], True)

