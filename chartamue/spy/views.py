import re
from tabnanny import check
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
#createuser => rsa 

# Create your views here.
def LoginPage(request):
    if request.user.is_authenticated :
        if request.user.userprofile.role == 'Admin' :
            request.session["role"] = 'Admin' 
            return redirect('AdminHomepage')  
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
            if request.user.is_authenticated :
                if request.user.userprofile.role == 'Admin' :
                    request.session["role"] = 'Admin' 
                    return redirect('AdminHomepage')  
                elif request.user.userprofile.role == 'Spy' :
                    request.session["role"] = 'Spy'
                    return redirect('SpyHomepage')
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('/')
    return redirect('/')

def Logout(request):
    if request.user.is_authenticated :
        logout(request)
        try:
            del request.session["role"]
        except:
            pass
    return redirect('/')
    
def MissionDetial(request , mission_id) :
    # mission = Mission.objects.get(id=mission_id)
    return render(request , "mission_detail.html" , {
        # 'mission' : mission
    })

def SpyProfile(request):
    return render(request, "spy_profile.html")

def SpyHomepage(request):
    return render(request,"spy_homepage.html")

def AddMission(request):
    return render(request,"add_mission.html")

def AddSpy(request):
    return render(request,"add_spy.html")
    
def EditPassword(request):
    form = PasswordChangeForm(request.POST or None)

    if request.method == 'POST' :
        form.save()

    return render(request,"Edit_password.html" , {
        'form' : form
    })

def AdminHomepage(request):
    return render(request,"admin_homepage.html")

"""
def MissionInsert(request):
    if request.user.is_authenticated :
        if request.user.userprofile.role == 'admin' : 
            if request.user.MissionAdmin.mission_name != MissionAdmin.objects.filter(mission_name=request.POST['text']):
                missionName = request.POST['mission_title']
                mission_descriptions = request.POST['mission_detail']
                date_start = request.POST[]
                status = request.POST[]
                spy = request.POST['spy_mission_owner']

    return redirect("AdminHomepage")
    """