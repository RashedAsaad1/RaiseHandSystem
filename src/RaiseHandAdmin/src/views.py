from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, get_user
from .forms import LoginForm
from .models import group
import string
import random
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
   """Generates a random string of uppercase letters and digits.

    Args:
        size (int, optional): The length of the string. Defaults to 10.
        chars (str, optional): The characters to choose from. Defaults to uppercase letters and digits.

    Returns:
        str: The generated string.
    """
   return ''.join(random.choice(chars) for _ in range(size))

def index(request):
   """Renders the index page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered index page.
    """
   return render(request, 'index.html',{})



def login_view(request):
    """Handles the login view.

    If the request method is POST, it tries to authenticate the user. If the user is authenticated, it logs them in and redirects them to the 'join' page.
    If the request method is not POST or the user is not authenticated, it renders the login page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered page or a redirect response.
    """
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
    """Handles the registration view.

    If the request method is POST, it tries to create a new user. If the form is valid, it saves the user and redirects them to the 'login_view' page.
    If the request method is not POST or the form is not valid, it renders the registration page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered page or a redirect response.
    """
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
   """Renders the join page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered join page.
    """
   return render(request, 'join.html',{'test': get_user(request)})

def createroom(request):
    """Handles the room creation view.

    If the request method is POST and the user is authenticated, it creates a new room and redirects the user to the chat page of the new room.
    If the request method is not POST or the user is not authenticated, it renders the room creation page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered page or a redirect response.
    """

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
    """Renders the chat room page.

    If the user is authenticated, it renders the chat room page. If the user is not authenticated, it redirects them to the login page.

    Args:
        request (HttpRequest): The request object.
        room_name (str): The name of the room.

    Returns:
        HttpResponse: The rendered page or a redirect response.
        """
    if(get_user(request).is_anonymous):
         return redirect('login')
    else:
      context = {
             'id': get_user(request).id,
             'username': get_user(request).username,
             
             "room_name": room_name
            }
      return render(request, 'room.html', context)