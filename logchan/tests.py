from django.test import TestCase
from rest_framework.test import APIClient

from logchan.models import Board

class RestApiTest(TestCase):
    def test_post(self):
        factory = APIClient()
        boardName = 'Test board'
        request = factory.post('/api/boards/', {'name': boardName}, format='json')
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Board.objects.get(name=boardName).name, boardName)

## Test view
# https://github.com/erkarl/django-rest-framework-oauth2-provider-example/blob/master/apps/users/tests.py
