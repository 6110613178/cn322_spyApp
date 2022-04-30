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
    def getValueInt(self):
        Intn =  int(self.n)
        Inte =  int(self.e)
        Intq =  int(self.q)
        Intp =  int(self.p)
        Intd =  int(self.d)
        return {"n":Intn, "e":Inte ,"d":Intd, "p": Intp ,"q":Intq}


class UserProfile(models.Model) :
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    role = models.CharField(max_length=5)
    code_name = models.CharField(max_length=15)
    rsa_key = models.OneToOneField(RSAKey , on_delete=models.CASCADE)
    ongoing_mission = models.IntegerField(default=0)
    waiting_mission = models.IntegerField(default=0)
    complete_mission = models.IntegerField(default=0)

class Mission(models.Model):
    mission_name = models.BinaryField()
    mission_descriptions = models.BinaryField()
    date_start = models.DateField()
    status = models.CharField(max_length=8)
    spy = models.ForeignKey(User , on_delete=models.CASCADE)

class MissionAdmin(models.Model):
    mission_name = models.BinaryField()
    mission_descriptions = models.BinaryField()
    date_start = models.DateField()
    status = models.CharField(max_length=8)
    spy = models.ForeignKey(User , on_delete=models.CASCADE)
    mission = models.OneToOneField(Mission , on_delete=models.CASCADE)