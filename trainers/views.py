from django.shortcuts import render
from .models import Client, Address, Team, Trainer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
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
    if request.user.is_authenticated:
        return render(request, "trainers/client_add.html")
    else:
        return HttpResponseRedirect(reverse('login_page'))

def client_add_action(request):
    client_name = request.POST['client_name']
    client_surname = request.POST['client_surname']
    client_birthdate = request.POST['client_birthdate']
    try:
        Client.objects.create(first_name=client_name, last_name=client_surname, birth_date= client_birthdate)
        return HttpResponseRedirect(reverse('client'))
    except:
        return HttpResponseRedirect(reverse('client_add'))


def teams(request):
    if request.user.is_authenticated:
        team_list = Team.objects.all()
        context = {'teams': team_list}
        return render(request, "trainers/teams.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def team_info(request, team_id):
    if request.user.is_authenticated:
        team = get_object_or_404(Team, pk=team_id)
        clients = team.clients.all()
        context = {'team': team, 'clients': clients}
        return render(request, "trainers/team_info.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def team_add(request):
    if request.user.is_authenticated:
        client_list = Client.objects.all()
        context = {'clients': client_list}
        return render(request, "trainers/team_add.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def team_add_action(request):
    team_name = request.POST['name']
    members = request.POST.getlist('members')
    try:
        team = Team.objects.create(name=team_name)
        for member in members:
            mem = Client.objects.get(pk = member)
            team.clients.add(mem)
        return HttpResponseRedirect(reverse('teams'))
    except:
        return HttpResponseRedirect(reverse('team_add'))


def trainers(request):
    if request.user.is_authenticated:
        trainers = Trainer.objects.all()
        context = {'trainers': trainers}
        return render(request, "trainers/trainers.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def trainers_add(request):
    if request.user.is_authenticated:
        return render(request, "trainers/trainers_add.html")
    else:
        return HttpResponseRedirect(reverse('login_page'))


def trainers_add_action(request):
    trainer_username = request.POST['name']
    trainer_email = request.POST['name']
    trainer_pass = request.POST['name']
    trainer_name = request.POST['name']
