from django.contrib.auth import login
from django.shortcuts import render,redirect
from .models import Room,Message
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def CreateRoom(request):
    if request.method == 'POST':
        username = request.user
        room = request.POST['room']
        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
        return redirect('room', room_name=room, username=username)
    return render(request, 'index.html',{'username':request.user})

@login_required
def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)
    
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    
    return render(request, '_message.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('create-room')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})