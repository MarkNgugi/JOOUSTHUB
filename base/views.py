from django.shortcuts import render
from .models import Room

rooms = [

    {"id":1,"name":"DJANGO"},
    {"id":2,"name":"WEB DEVELOPMENT"},
    {"id":3,"name":"BACKEND DEVELOPMENT"},
    {"id":4,"name":"POLITICS"},
    {"id":5,"name":"MUSIC"},
    {"id":6,"name":"SPORTS"},
    {"id":7,"name":"GAMING"},


]

def home(request):

    rooms = Room.objects.all()
    context = {"rooms":rooms}
    return render(request,"home.html",context)

def room(request,pk):

    room = Room.objects.get(id=pk)
    context = {"room":room}
    return render(request,"room.html",context)
