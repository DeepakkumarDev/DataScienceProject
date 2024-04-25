from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('upload/',views.Fupload,name='fileupload'), 
    path('dataupload/',views.Dataupload,name='dataupload'),
    path('descriptive/',views.DscriptiveStats,name='descriptive'),
    path('selecttable/',views.select_table,name='selecttable')
]
