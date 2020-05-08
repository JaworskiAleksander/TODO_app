from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone

from .forms import TodoForm
from .models import Todo

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

@login_required(login_url='loginuser')
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'TODO/currenttodos.html', {'todos': todos})

@login_required()
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

@login_required(login_url='loginuser')
def createtodo(request):
    if request.method == 'GET':
        return render(request,
                     'TODO/createtodo.html',
                     {'form': TodoForm()}
                     )
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError as identifier:
            return render(request,
                     'TODO/createtodo.html',
                     {'form': TodoForm(),
                      'error_msg': identifier
                     }
                     )

@login_required(login_url='loginuser')
def viewtodo(request, todo_pk):
    try:
        todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    except Http404:
        return redirect('home')            
    # add handling 404 exception
    # redirect to homepage and
    # display error_msg: you are not authorized to view this note
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'TODO/viewtodo.html', {'todo': todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError as identifier:
            return render(request,
                          'TODO/viewtodo.html',
                          {'todo': todo, 'form':form, 'error_msg': 'Bad info!'}
                          )

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
