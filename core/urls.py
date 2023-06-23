from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include

from . import views
from .forms import LoginForm

app_name='core'

urlpatterns=[
    path('',views.login_view, name='login_view'),
    path('index/',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]