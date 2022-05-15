from inspect import _void
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LogoutView


from .forms import LoginForm

from django.shortcuts import redirect

def user_login(request):
    print(request.user)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/polls/')
                else:
                    return HttpResponse('Disabled account')
            #else:
                #return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    
    return render(request, 'authorization/login.html', {'form': form})

def redir(request):
    return HttpResponseRedirect('/login/')
