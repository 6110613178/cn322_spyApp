from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class RSAKey(models.Model) :
    # PrivateKey(n: int, e: int, d: int, p: int, q: int)
    # PublicKey(n: int, e: int)¶
    n = models.CharField(max_length=1024)
    e = models.CharField(max_length=1024)
    q = models.CharField(max_length=1024)
    p = models.CharField(max_length=1024)
    d = models.CharField(max_length=1024)

class UserProfile(models.Model) :
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    role = models.CharField(max_length=5)
    code_name = models.CharField(max_length=15)
    rsa_key = models.OneToOneField(RSAKey , on_delete=models.CASCADE)

class Mission(models.Model):
    mission_name = models.CharField(max_length=255)
    mission_descriptions = models.CharField(max_length=255)
    date_start = models.DateField()
    status = models.BooleanField()
    spy = models.ForeignKey(User , on_delete=models.CASCADE)

class MissionAdmin(models.Model):
    mission_name = models.CharField(max_length=255)
    mission_descriptions = models.CharField(max_length=255)
    date_start = models.DateField()
    status = models.BooleanField()
    spy = models.ForeignKey(User , on_delete=models.CASCADE)
    mission = models.OneToOneField(Mission , on_delete=models.CASCADE)