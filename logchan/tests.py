from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from logchan.models import Board

class RestApiTest(TestCase):
    def test_post(self):
        client = APIClient()
        boardName = 'Test board'
        request = client.post('/api/boards/', {'name': boardName}, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.get(name=boardName).name, boardName)

    def test_get(self):
        boardName = 'Test board'
        b = Board(name=boardName)
        b.save()

        client = APIClient()
        url = '/api/boards/{}/'.format(b.name)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 'name': boardName })

    def test_put(self):
        boardName = 'Test board'
        b = Board(name=boardName)
        b.save()

        client = APIClient()
        url = '/api/boards/{}/'.format(b.name)
        boardName = 'bant'
        request = client.put(url, data={'name': boardName}, content_type='json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        print(Board.objects.all())
        b = Board.objects.get(name=boardName)
        self.assertEqual(boardName, b.name)

## Test view
# https://github.com/erkarl/django-rest-framework-oauth2-provider-example/blob/master/apps/users/tests.py
