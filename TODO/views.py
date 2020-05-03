from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login
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

def currenttodos(request):
    return render(request, 'TODO/currenttodos.html')
