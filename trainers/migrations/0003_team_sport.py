# Generated by Django 3.2.20 on 2023-07-14 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0002_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='sport',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
