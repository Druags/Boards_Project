from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Board


# Create your views here.


def home_view(request):
    boards = Board.objects.all()

    return render(request, 'home.html', {'boards': boards})


def board_topics_view(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except:
        raise Http404
    return render(request, 'topics.html', {'board':board})
