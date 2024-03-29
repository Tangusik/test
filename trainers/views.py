import datetime
from datetime import date
from django.shortcuts import render
from .models import Client, Team, Trainer, Activity, Sport, News, TrainerStatus
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count



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
        news = News.objects.filter(pub_date__lte=timezone.now(), expiry_date__gt=timezone.now())

        user = request.user
        try:
            trainer = Trainer.objects.get(user=user)
            is_trainer = True
        except Trainer.DoesNotExist:
            trainer = None
            is_trainer = False
        context = {'userinfo': user, 'trainer': trainer, 'is_trainer': is_trainer, 'news': news}
        return render(request, 'trainers/main.html', context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def clients(request):
    if request.user.is_authenticated:
        clients = Client.objects.all()
        teams = Team.objects.all()

        sports = Sport.objects.annotate(team_count=Count('team'))


        context = {'clients': clients, 'teams': teams, 'sports': sports}

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
    sport = request.POST['sport']
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
        sport = Sport.objects.all()
        status = TrainerStatus.objects.all()

        if request.GET.get('status'):
            trainers = trainers.filter(status__name=request.GET.get('status'))

        if request.GET.get('sports'):
            trainers = trainers.filter(sports__name=request.GET.get('sports'))



        today = date.today()
        trainers_birth = Trainer.objects.all().order_by('birthdate')
        upcoming_birthdays = []
        today_birthdays = []
        for trainer in trainers_birth:
            #дата> рождения тренера в этом году
            birthdate_this_year = date(today.year, trainer.birthdate.month, trainer.birthdate.day)
            if birthdate_this_year < today:
                birthdate_this_year = date(today.year + 1, trainer.birthdate.month, trainer.birthdate.day)
            #оставшееся время до дня рождения
            time_to_birthday = (birthdate_this_year - today).days
            if time_to_birthday <= 7 & time_to_birthday != 0:
                upcoming_birthdays.append(trainer)
            if time_to_birthday == 0:
                    today_birthdays.append(trainer)
        trainers_search = []
        query = request.GET.get('q')
        if query:
            trainers_search = Trainer.objects.filter(Q(user__first_name__icontains=query) | Q(user__email__icontains=query))

        context = {'trainers': trainers, 'status': status, 'sport': sport, 'upcoming_birthdays': upcoming_birthdays, 'today_birthdays': today_birthdays, 'trainers_search': trainers_search, 'query': query}

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
    if request.user.is_authenticated:
        activities = Activity.objects.all()
        context = [activity.to_json() for activity in activities]
        context = json.dumps(context)
        return render(request, "trainers/schedule.html", {'activities': context})
    else:
        return HttpResponseRedirect(reverse('login_page'))
