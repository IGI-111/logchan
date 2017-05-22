from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.core.urlresolvers import reverse

from logchan.models import Board, Thread, Post

class RestApiTestBoard(TestCase):
    def test_board_post(self):
        client = APIClient()
        boardName = 'Test board'
        request = client.post('/api/board/', {'name': boardName}, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.get(name=boardName).name, boardName)

    def test_board_get(self):
        boardName = 'Test board'
        b = Board(name=boardName)
        b.save()

        client = APIClient()
        url = '/api/board/{}/'.format(b.name)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 'name': boardName })

    def test_board_delete(self):
        testBoard = Board(name='Test bb')
        testBoard.save()
        client = APIClient()

        url = '/api/board/{}/'.format(testBoard.name)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

