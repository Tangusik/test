from django.db import models
from django.contrib.auth.models import User
import datetime


class Client(models.Model):
    first_name = models.CharField(blank=False, max_length=30, default='qwerty')
    last_name = models.CharField(blank=True, max_length=30)
    reg_date = models.DateField(auto_now=True, blank=True)
    birth_date = models.DateField(auto_now=False, blank=True, default=datetime.date(2023, 1, 1))


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
    date_time = models.CharField(max_length=10, blank=False, default='01.01.2023')
    members = models.ManyToManyField(Client, through='Membership')


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Activity(models.Model):
    regular = models.BooleanField()
    date_time = models.CharField(max_length=10, blank=False, default='01.01.2023')
    place = models.CharField(blank=True, max_length=20)
