from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


class Client(models.Model):
    balance = models.IntegerField(blank=False, default=0)
    first_name = models.CharField(blank=False, max_length=30, default='qwerty')
    last_name = models.CharField(blank=True, max_length=30)
    reg_date = models.DateField(auto_now=True, blank=True)
    birth_date = models.DateField(auto_now=False, blank=True, default=datetime.date(2023, 1, 1))

    def __str__(self):
        return self.first_name


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    otchestv = models.CharField(blank=True, max_length=20)
    birthdate = models.DateField(auto_now=False)
    def __str__(self):
        return self.user.first_name


class Address(models.Model):
    city = models.CharField(blank=False, default='123', max_length=30)
    street = models.CharField(blank=False, default='123', max_length=30)
    house = models.CharField(blank=True, max_length=30)
    building = models.CharField(blank=True, max_length=30)
    flat = models.CharField(blank=True, max_length=30)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Parents(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True, max_length=30)
    email = models.CharField(blank=True, max_length=30)
    telephone = models.CharField(blank=True, max_length=30)


class Team(models.Model):
    name = models.CharField(max_length=20, default="qwerty")
    clients = models.ManyToManyField(Client)
    trainer = models.ForeignKey(Trainer, models.CASCADE, blank=True, null=True)
    sport = models.CharField(blank=True, max_length=30, null=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    price = models.IntegerField(blank=False, default=0)
    act_date = models.DateField(auto_now=False, blank=False)
    act_time_begin = models.TimeField(auto_now=False)
    act_time_end = models.TimeField(auto_now=False)
    clients = models.ManyToManyField(Client)
    trainer = models.ForeignKey(Trainer, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default="Состоится")

    def to_json(self):
        return {
            'price': self.price,
            'act_date': self.act_date.strftime('%Y-%m-%d'),
            'act_time_begin': self.act_time_begin.strftime('%H:%M:%S'),
            'act_time_end': self.act_time_end.strftime('%H:%M:%S'),
            'clients': [client.id for client in self.clients.all()],
            'trainer': self.trainer.user.first_name,
            'status': self.status,
        }


class News(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    expiry_date = models.DateTimeField('expiry date')
    text = models.TextField()

    def __str__(self):
        return self.title

    def is_expired(self):
        return timezone.now() > self.expiry_date

    class Meta:
        ordering = ['-pub_date']
