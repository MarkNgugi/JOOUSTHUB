from django.shortcuts import render


rooms = [

    {"id":1,"name":"DJANGO ROOM"},
    {"id":2,"name":"WEB DEVELOPMENT"},
    {"id":3,"name":"BACKEND DEVELOPMENT"},
    {"id":4,"name":"POLITICS"},
    {"id":5,"name":"MUSIC"},
    {"id":6,"name":"SPORTS"},

]

def home(request):
    context = {"rooms":rooms}
    return render(request,"home.html",context)

def room(request,pk):
    room = None
    for i in rooms:
        if i["id"] == int(pk):
            room = i
            
    context = {"room":room}
    return render(request,"room.html",context)
