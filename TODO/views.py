from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def signupuser(request):
    if request.method == 'GET':
        # return to signup page
        return render(request, 'TODO/signupuser.html', {'form': UserCreationForm()})
    else:
        # creating a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                                                password=request.POST['password1']
                                                )
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request,
                              'TODO/signupuser.html',
                              {'form': UserCreationForm(),
                               'error_msg':'That username has already been taken.'})
                               
            
        else:
            # tell the user that passwords did not match
            return render(request,
                          'TODO/signupuser.html',
                          {'form': UserCreationForm(),
                           'error_msg':'Passwords did not match.'})

@login_required(login_url='TODO/signupuser.html')
def currenttodos(request):
    return render(request, 'TODO/currenttodos.html')

@login_required(login_url='TODO/signupuser.html')
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request,
                     'TODO/login.html',
                     {'form': AuthenticationForm()}
                     )

    if request.method == 'POST':
        try:
            # check if user exists
            user = authenticate(request,
                                username=request.POST['username'],
                                password=request.POST['password']
                                )
            if user is None:
                return render(request,
                     'TODO/login.html',
                     {  'form': AuthenticationForm(),
                        'error_msg': 'Username and/or password did not match'
                     }
                     )
            else:
                login(request, user)
                return redirect('currenttodos')

        except:
            # catch following errors
                # username does not exist
                # password incorrect
                # database configuration problem
            pass
    pass

def home(request):
    return render(request, 'TODO/home.html')
