from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, get_user
from .forms import LoginForm
from .models import group
import string
import random
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def index(request):
   return render(request, 'index.html',{})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
               login(request, user)
               return redirect('join')
            
    else:   
        form = LoginForm()
    if get_user(request).is_anonymous:
      return render(request, 'login.html', {'form': form})
    else:
       return redirect('index')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')  
    else:
        form = UserCreationForm()
    if get_user(request).is_anonymous:
      return render(request, 'register.html', {'form': form})
    else:
       return redirect('index')
  

def join(request):
   return render(request, 'join.html',{'test': get_user(request)})

def createroom(request):
    if request.method == "POST":
       if(get_user(request).is_anonymous):
         return redirect('login')
       else:
        context = {
             'username': get_user(request).username,
             "role": True
            }
        request.session['id_generator'] = id_generator()
        idgenerator = request.session['id_generator']
        test =  group(name=get_user(request).username, groupcode=idgenerator)
        test.save()
        return redirect("../chat/"+idgenerator,context)

    return render(request, 'createroom.html',context)


def room(request,room_name):
   if(get_user(request).is_anonymous):
         return redirect('login')
   else:
      context = {
             'id': get_user(request).id,
             'username': get_user(request).username,
             
             "room_name": room_name
            }
      return render(request, 'room.html', context)