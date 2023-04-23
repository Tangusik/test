import datetime, calendar

from django.shortcuts import render
from .models import Client, Address, Team, Trainer, Activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404


def login_page(request):
    if request.user.is_authenticated:
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
        Client.objects.create(first_name=client_name, last_name=client_surname, birth_date=client_birthdate)
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
        trainer_list = Trainer.objects.all()
        context = {'clients': client_list, 'trainers': trainer_list}
        return render(request, "trainers/team_add.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def team_add_action(request):
    team_name = request.POST['name']
    members = request.POST.getlist('members')
    trainer = request.POST['trainer']
    date_end = request.POST['date_end']
    days = request.POST.getlist('days')
    act_begin_time = request.POST['act_begin_time']
    act_end_time = request.POST['act_end_time']
    try:
        for day in days:
            day = int(day)

        tr= get_object_or_404(Trainer, pk=trainer)
        team = Team.objects.create(name=team_name, trainer = tr)
        for client in members:
            team.clients.add(client)

        date = datetime.date.today()

        while date != date_end:
            if date.weekday() in days:
                act = Activity(act_date = date, act_time_begin =act_begin_time, act_time_end=act_end_time)
                act.save()
                for client in members:
                    act.clients.add(client)
                    act.save()
                date = date + datetime.timedelta(days=1)

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
    trainer_name = request.POST['name']
    trainer_last_name = request.POST['last_name']
    trainer_otchestv = request.POST['otchestv']
    trainer_mail = request.POST['mail']
    trainer_pass = request.POST['password']
    trainer_birthdate = request.POST['birth_date']
    try:
        user = User.objects.create_user(username=trainer_mail, email=trainer_mail, password=trainer_pass)
        user.last_name = trainer_last_name
        user.first_name = trainer_name
        user.save()
        trainer = Trainer(user=user, otchestv=trainer_otchestv, birthdate=trainer_birthdate)
        trainer.save()
        return HttpResponseRedirect(reverse('trainers'))
    except:
        return HttpResponseRedirect(reverse('trainers_add'))


def trainer_info(request, trainer_id):
    if request.user.is_authenticated:
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        team_list = Team.objects.filter()
        context = {'trainer': trainer, 'teams': team_list}
        return render(request, "trainers/trainer_info.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))

def activity(request):
    if request.user.is_authenticated:
        activity_list = Activity.objects.all()
        context = {'activities': activity_list}
        return render(request, "trainers/activities.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))