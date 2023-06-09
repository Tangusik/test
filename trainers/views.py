import datetime, calendar

from django.shortcuts import render
from .models import Client, Address, Team, Trainer, Activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
import json


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
        user = request.user
        try:
            trainer = Trainer.objects.get(user=user)
            is_trainer = True
        except Trainer.DoesNotExist:
            trainer = None
            is_trainer = False
        context = {'userinfo': user, 'trainer': trainer, 'is_trainer': is_trainer}
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


def client_add_action(request):
    client_name = request.POST['client_name']
    client_surname = request.POST['client_surname']
    client_birthdate = request.POST['client_birthdate']
    try:
        Client.objects.create(first_name=client_name, last_name=client_surname, birth_date=client_birthdate)
        return HttpResponseRedirect(reverse('clients'))
    except:
        return HttpResponseRedirect(reverse('client_add'))


def teams(request):
    if request.user.is_authenticated:
        team = Team.objects.all()
        context = {'teams': team}
        return render(request, "trainers/teams.html", context)
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
    price = request.POST['price']
    try:
        tr = get_object_or_404(Trainer, pk=trainer)
        team = Team.objects.create(name=team_name, trainer=tr)
        for client in members:
            team.clients.add(client)

        date1 = datetime.date.today()
        date2 = datetime.datetime.strptime(date_end, '%Y-%m-%d')

        while date1 <= date2.date():
            if str(date1.weekday()) in days:
                act = Activity(act_date=date1, act_time_begin=act_begin_time,
                               act_time_end=act_end_time, trainer=tr, price=price)
                act.save()
                for client in members:
                    act.clients.add(client)
                act.save()
            date1 = date1 + datetime.timedelta(days=1)

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
        print('user created')
        trainer = Trainer(user=user, otchestv=trainer_otchestv, birthdate=trainer_birthdate)
        trainer.save()
        return HttpResponseRedirect(reverse('trainers'))
    except:
        return HttpResponseRedirect(reverse('trainers'))
#
# def activity(request):
#     if request.user.is_authenticated:
#         activity_list = Activity.objects.all()
#         context = {'activities': activity_list}
#         return render(request, "trainers/schedule.html", context)
#     else:
#         return HttpResponseRedirect(reverse('login_page'))
#
#
# def activity_info(request, activity_id):
#     if request.user.is_authenticated:
#         act = get_object_or_404(Activity, pk=activity_id)
#         clients = act.clients.all()
#         context = {'act': act, 'clients': clients}
#         return render(request, "trainers/act_info.html", context)
#     else:
#         return HttpResponseRedirect(reverse('login_page'))
#
#
# def activity_change(request, activity_id):
#     status = request.POST['status']
#     client_who_was = request.POST.getlist('client')
#     act = get_object_or_404(Activity, pk=activity_id)
#     try:
#         if status == "Состоится":
#             for id in client_who_was:
#                 client = get_object_or_404(Client, pk=id)
#                 client.balance = client.balance - act.price
#                 client.save()
#             act.status = status
#             act.save()
#         elif status == "Отменено":
#             act.status = status
#             act.save()
#         return HttpResponseRedirect(reverse('activity'))
#     except:
#         return HttpResponseRedirect(reverse('activity'))


def schedule(request):
    # if request.user.is_authenticated:
    #     activities = Activity.objects.all()
    #     json_activities = serialize('json', activities)
    #     context = {'json_activities': json_activities}
    #     return render(request, "trainers/schedule.html", context)
    # else:
    #     return HttpResponseRedirect(reverse('login_page'))
    if request.user.is_authenticated:
        activities = Activity.objects.all()
        context = [activity.to_json() for activity in activities]
        context = json.dumps(context)
        return render(request, "trainers/schedule.html", {'activities': context})
    else:
        return HttpResponseRedirect(reverse('login_page'))
