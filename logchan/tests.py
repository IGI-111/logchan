from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from logchan.models import Board

class RestApiTest(TestCase):
    def test_post(self):
        client = APIClient()
        boardName = "Test board"
        request = client.post("/api/boards/", {"name": boardName}, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.get(name=boardName).name, boardName)

    def test_get(self):
        boardName = "Test board"
        b = Board(name=boardName)
        b.save()

        client = APIClient()
        url = "/api/boards/" + b.id
        request = client.get(url, format="json")
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(request.data.name, boardName)

    def test_put(self):
        boardName = "Test board"
        b = Board(name=boardName)
        b.save()

        client = APIClient()
        url = "/api/boards/" + b.id
        boardName = "Change name"
        request = client.put(url, data={"name": boardName, id:  b.id}, content_type="json")

        b = board.objects.get(id=b.id)
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(boardName, b.name)

## Test view
# https://github.com/erkarl/django-rest-framework-oauth2-provider-example/blob/master/apps/users/tests.py
