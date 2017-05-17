from django.shortcuts import render
from django.http import HttpResponse

from .models import Board

def index(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})
