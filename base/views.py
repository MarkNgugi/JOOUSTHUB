from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# rooms = [

#     {"id":1,"name":"DJANGO"},
#     {"id":2,"name":"WEB DEVELOPMENT"},
#     {"id":3,"name":"BACKEND DEVELOPMENT"},
#     {"id":4,"name":"POLITICS"},
#     {"id":5,"name":"MUSIC"},
#     {"id":6,"name":"SPORTS"},
#     {"id":7,"name":"GAMING"},

# ]

def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Username or Password')

    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def RegisterUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('RegisterUser')

    context = {'form':form}
    return render(request, 'base/login_register.html',context)


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()

    rooms = Room.objects.filter (
        Q(Topic__Topic_name__icontains=q) |
        Q(Room_name__icontains=q) |
        Q(description__icontains=q) |
        Q(Host__username=q)
    )

    room_messages = Message.objects.filter(Q(room__Topic__Topic_name__icontains=q))
    room_count = rooms.count()
    context = {"rooms":rooms,"topics":topics,"room_count":room_count,'room_messages':room_messages}
    return render(request,"base/home.html",context)

def room(request,pk):

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {"room":room,'room_messages':room_messages,'participants':participants}
    return render(request,"base/room.html",context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request,"base/room_form.html",context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,"base/room_form.html",context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {"item":room}
    return render(request,"base/delete.html",context)


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = {"item":message}
    return render(request,"base/delete.html",context)