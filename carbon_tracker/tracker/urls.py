from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activity/add/', views.add_activity, name='add_activity'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('goal/set/', views.set_goal, name='set_goal'),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]