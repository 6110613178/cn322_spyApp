from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from .rsatest import generateKey
import rsa 
#createuser => rsa 

# Create your views here.
def LoginPage(request):
    if request.user.is_authenticated :
        if request.user.userprofile.role == 'Admin' :
            request.session["role"] = 'Admin' 
            return redirect('Adminhomepage')  
        elif request.user.userprofile.role == 'Spy' :
            request.session["role"] = 'Spy'
            return redirect('SpyHomepage')
    return render(request,"login.html")


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            role = request.user.userprofile.role
            if role == 'Admin' :
                request.session["role"] = 'Admin'  
            elif role == 'Spy' and username==password :
                request.session["role"] = 'Spy'
                return HttpResponseRedirect(reverse('EditPassword'))
            
            return HttpResponseRedirect(reverse('{}homepage'.format(role)))

        messages.error(request,"Invalid username or password.")

    return HttpResponseRedirect(reverse('LoginPage'))

def Logout(request):
    if request.user.is_authenticated :
        logout(request)
        try:
            del request.session["role"]
        except:
            pass
    return redirect('/')
    
def MissionDetail(request , mission_id) :
    if request.user.is_authenticated :
        mission = Mission.objects.get(id=mission_id)
        userprofile = mission.spy.userprofile
        rsa_key = userprofile.rsa_key.getValueInt()
        privateKey = rsa.PrivateKey(n=rsa_key["n"],e=rsa_key["e"],d=rsa_key["d"],p = rsa_key["p"] ,q= rsa_key["q"])
        name_decrypt = rsa.decrypt(mission.mission_name, privateKey).decode()
        descriptions_decrypt = rsa.decrypt(mission.mission_descriptions, privateKey).decode()
        if request.method == "POST" :
            print(request.POST)
            status = request.POST['status']
            mission.status = status
            mission.save()

        return render(request , "mission_detail.html" ,  {   "id": mission.id,
                    "mission_name": name_decrypt,
                    "mission_descriptions" : descriptions_decrypt,
                    "date_start": mission.date_start,
                    "status": mission.status
                 })

    return redirect('/')

def SpyProfile(request,id):
    if request.user.is_authenticated :
        user = User.objects.get(pk=id) # Spy
        missions = Mission.objects.filter(spy=user).order_by('date_start')
        userprofile = user.userprofile
        rsa_key = userprofile.rsa_key.getValueInt()
        privateKey = rsa.PrivateKey(n=rsa_key["n"],e=rsa_key["e"],d=rsa_key["d"],p = rsa_key["p"] ,q= rsa_key["q"])
        missionDecrypt= []
        for mission in missions:
            name_decrypt = rsa.decrypt(mission.mission_name, privateKey).decode()
            descriptions_decrypt = rsa.decrypt(mission.mission_descriptions, privateKey).decode()
            missionDecrypt.append(
                {   "id": mission.id,
                    "mission_name": name_decrypt,
                    "mission_descriptions" : descriptions_decrypt,
                    "date_start": mission.date_start,
                    "status": mission.status
                 }
            )
        return render(request, "spy_profile.html" , {
            'missions' : missionDecrypt,
            'user' : user
        })
    return redirect('/')

def DeleteSpyProfile(request,id):
    if request.user.is_authenticated :
        if request.method == 'POST':
            print("delete")
            delete_user = User.objects.get(id=id)
            delete_user.delete()
            return HttpResponseRedirect(reverse('Adminhomepage'))
        return render(request, "admin_homepage.html")
    return redirect('/')

def SpyHomepage(request):
    if request.user.is_authenticated :
        user_profile = request.user.userprofile
        missions = Mission.objects.filter(spy=request.user).order_by('date_start')
        return render(request,"spy_homepage.html" , {
            'missions' : missions,
            'total' : user_profile.complete_mission + user_profile.ongoing_mission + user_profile.waiting_mission
        })
    return HttpResponseRedirect(reverse('LoginPage'))
    #return redirect('/')


def AddSpy(request):
    if request.user.is_authenticated  and request.user.userprofile.role == 'Admin' :
        if request.method == 'POST':
            code_name = request.POST.get('code_name')
            password = request.POST.get('username')
            print(password)
            print(code_name)
            user = User.objects.create_user(username=code_name , password=password)
            n,e,d,p,q = generateKey()
            rsa_key = RSAKey(n=n,e=e,d=d,p=p,q=q)
            rsa_key.save()
            new_user = UserProfile(user = user,role='Spy',code_name=code_name,rsa_key = rsa_key)
            new_user.save()
            return HttpResponseRedirect(reverse('Adminhomepage'))
        return render(request,"add_spy.html")
    return redirect('/')
    
def EditPassword(request):
    form = PasswordChangeForm(request.user , request.POST or None)

    if form.is_valid() :

        form.save()

    return render(request,"Edit_password.html" , {
        'form' : form
    })

def Adminhomepage(request):
    if request.user.is_authenticated :
        all_spy = UserProfile.objects.filter(role = "Spy")
        
            
        return render(request,"admin_homepage.html",
        {
            'all_spy' : all_spy
        })
    return redirect('/')


def AddMission(request):
    if request.user.is_authenticated and request.user.userprofile.role == 'Admin' :
        if request.method == 'POST':
            missionName = request.POST['mission_title']
            missionDescriptions = request.POST['mission_detail']
            date = request.POST['dateMission']
            status = "on going"
            spyID = request.POST['spy_mission_owner'] #'9'

            userProfile = UserProfile.objects.filter(id = spyID)[0] #Object UserProfile
            rsa_key = userProfile.rsa_key.getValueInt()

            publicKey_spy = rsa.PublicKey(n=rsa_key["n"],e=rsa_key["e"])
            admin = UserProfile.objects.filter(role = "Admin")[0]
            rsa_key_admin = admin.rsa_key.getValueInt()
            publicKey_admin = rsa.PublicKey(n=rsa_key_admin["n"],e= rsa_key_admin["e"])

            encMissionNameSpy = rsa.encrypt(missionName.encode(),publicKey_spy)
            encMissionNameAdmin = rsa.encrypt(missionName.encode(),publicKey_admin)

            print(encMissionNameSpy)
                
            encMissionDesSpy = rsa.encrypt(missionDescriptions.encode(),publicKey_spy)
            encMissionDesAdmin = rsa.encrypt(missionDescriptions.encode(),publicKey_admin)

            user = userProfile.user #Object User
            mission = Mission(mission_name=encMissionNameSpy,mission_descriptions=encMissionDesSpy,date_start=date,status=status,spy=user)
            mission.save()
            missionAdd = MissionAdmin(mission_name=encMissionNameAdmin,mission_descriptions=encMissionDesAdmin,date_start=date,status=status,spy=user,mission=mission)
            missionAdd.save()
        else:
            all_spy = UserProfile.objects.filter(role='Spy')
            return render(request,"add_mission.html",{'all_spy': all_spy})
    return redirect('/')
    