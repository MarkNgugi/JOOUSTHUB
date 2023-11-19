from django.db.models import Q
from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm

# rooms = [

#     {"id":1,"name":"DJANGO"},
#     {"id":2,"name":"WEB DEVELOPMENT"},
#     {"id":3,"name":"BACKEND DEVELOPMENT"},
#     {"id":4,"name":"POLITICS"},
#     {"id":5,"name":"MUSIC"},
#     {"id":6,"name":"SPORTS"},
#     {"id":7,"name":"GAMING"},

# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()

    rooms = Room.objects.filter (
        Q(Topic__Topic_name__icontains=q) |
        Q(Room_name__icontains=q) |
        Q(description__icontains=q) |
        Q(Host__username=q)
    )

    context = {"rooms":rooms,"topics":topics}
    return render(request,"home.html",context)

def room(request,pk):

    room = Room.objects.get(id=pk)
    context = {"room":room}
    return render(request,"room.html",context)

def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request,"room_form.html",context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,"room_form.html",context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {"item":room}
    return render(request,"delete.html",context)