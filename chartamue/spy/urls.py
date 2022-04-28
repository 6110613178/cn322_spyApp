from django.urls import path
from . import views

urlpatterns = [
    path('',views.LoginPage,name="LonginPage"),
    path('mission_detail/<int:mission_id>',views.MissionDetial,name="mission"),
    path('spy_profile',views.SpyProfile,name="SpyProfile"),
    path('add_mission',views.AddMission,name="add_mission"),
    path('add_spy',views.AddSpy,name="add_spy"),
    path('spy_homepage',views.SpyHomepage,name="Spyhomepage"),
    path('admin_homepage',views.AdminHomepage,name="AdminHomepage"),
    path('edit_password',views.EditPassword,name="EditPassword"),
    path('login',views.Login,name="Login"),
    path('logout',views.Logout,name="Logout"),
]