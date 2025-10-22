from django.urls import path
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
    )
# untuk mengelola login,password reset dan change password jadi tidak perlu buat fungsi di views

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index_profile, name='index'),
    path('user/update_profiles', views.update_profiles, name='update_profiles'),
    path('login/',LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.register_users, name='register'),
    path('password_reset/', PasswordResetView.as_view(template_name= "registration/password_reset_form.html"), 
    name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name= "registration/password_reset_done.html"), 
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name= "registration/password_reset_confirm.html"), 
    name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name= "registration/password_reset_complete.html"), 
    name='password_reset_confirm'),
    path('password_change/', PasswordChangeView.as_view(template_name= "registration/password_change_form.html"), 
    name='password_change'),
    path('password_change/done', PasswordChangeDoneView.as_view(template_name= "registration/password_change_done.html"), 
    name='password_change_done'),
]
