from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', context_instance=RequestContext(request))


def register_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = User(username=username, password=password)
        user.save()
        return HttpResponseRedirect('/login/')
    return render_to_response('register.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request):
    return HttpResponse("Hello, world!")