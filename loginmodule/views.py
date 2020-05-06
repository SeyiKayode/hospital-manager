from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib import messages
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return HttpResponseRedirect('/')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'loginmodule/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are now logged in')
        return HttpResponseRedirect('/')
    else:
        messages.warning(request, 'Invalid login credentials')
        return HttpResponseRedirect('/login')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    messages.info(request, 'You have successfully logged out')
    return HttpResponseRedirect('/login')










