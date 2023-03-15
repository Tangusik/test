from django.shortcuts import render
from .models import Client, Address
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404


def login_page(request):
    if  request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main'))
    else:
        return render(request, 'trainers/login.html')



def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('login_page'))
    else:
        return HttpResponseRedirect(reverse('main'))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))


def main(request):
    if request.user.is_authenticated:
        userinfo = request.user
        context = {'userinfo': userinfo}
        return render(request, 'trainers/main.html', context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def clients(request):
    if request.user.is_authenticated:
        clients = Client.objects.all()
        context = {'clients': clients}
        return render(request, "trainers/clients.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def client_info(request, client_id):
    if request.user.is_authenticated:
        client = get_object_or_404(Client, pk=client_id)
        adr = client.address_set.all()
        context = {'client': client, 'adr': adr}
        return render(request, "trainers/clients_info.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def client_add(request):
    pass