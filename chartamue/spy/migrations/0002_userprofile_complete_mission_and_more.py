# Generated by Django 4.0.4 on 2022-04-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='complete_mission',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ongoing_mission',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='waiting_mission',
            field=models.IntegerField(default=0),
        ),
    ]