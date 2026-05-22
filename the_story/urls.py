from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views
from blog.views import home
from django.contrib.auth.forms import AuthenticationForm
from django import forms, views
from blog.views import PostListAPIView 
from django.urls import path
from blog import views  # Make sure this points to YOUR app name (e.g., 'pages')

# 1. Your Custom Email Form (Keep this)
class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # FIX: Point the root URL to your home view and give it the name 'home'
    path('', views.home, name='home'), 
    
    path('home/', views.home, name='home_alternate'), # Optional: keep this if you want /home/ to work too
    path('accounts/', include('allauth.urls')), 
    path('api/posts/', views.PostListAPIView.as_view(), name='post-api'),
    path('kanye/', views.kanye_quote_view, name='kanye-quotes'),
    path('post/new/', views.create_post, name='post_create'),
]

