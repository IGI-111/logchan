from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Board, Thread, Post
from .api.viewsets import grecaptcha_verify
from .templatetags import logchan_extras

def post_thread(request):
    if not (request.user is not None and logchan_extras.is_in_group(request.user, "Admin")) or (
            not grecaptcha_verify(request)):
        return HttpResponse("Cannot validate captcha", status=400)

    board = Board.objects.get(name=request.POST.get('board'))
    thread = Thread(board=board, subject=request.POST.get('subject'))
    thread.save()

    image = {}
    if 'image' in request.FILES:
        image = request.FILES['image']

    post = Post(
            thread=thread,
            date=request.POST.get('date'),
            user_name=request.POST.get('user_name'),
            image=image,
            message=request.POST.get('message'))

    post.save()

    return HttpResponse('', status=201)

def index(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})

def board(request, board_name):
    boards = Board.objects.all()
    board = Board.objects.get(name=board_name)
    threads = Thread.objects.filter(board=board_name)
    return render(request, 'catalog.html', {
        'boards': boards,
        'board': board,
        'threads':threads
        })

def thread(request, board_name, thread_id):
    boards = Board.objects.all()
    board = Board.objects.get(name=board_name)
    thread = Thread.objects.get(board=board_name, id=thread_id)
    posts = Post.objects.filter(thread=thread_id)
    return render(request, 'thread.html', {
        'boards': boards,
        'board': board,
        'thread':thread,
        'posts':posts
        })

class Login(TemplateView):
    def get(self, request, **kwargs):
        boards = Board.objects.all()
        return render(request, 'login.html', {'boards': boards})
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        boards = Board.objects.all()
        return render(request, 'login.html', {'boards': boards, 'errors' : 'The username or password you entered is incorrect.'})

class Logout(TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

