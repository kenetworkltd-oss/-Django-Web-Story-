from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework import generics
from .serializers import PostSerializer
import requests
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# --- BLOG VIEWS ---

def home(request):
    """Handles search and displays posts ordered by newest first."""
    query = request.GET.get('search')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.all()
    
    posts = posts.order_by('-date_published')
    return render(request, 'blog/index.html', {'posts': posts})

# --- API VIEWS ---

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# --- AUTHENTICATION VIEWS ---

def signup(request):
    """Creates an inactive user and sends a verification email."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Keep inactive until email confirmed
            user.save()

            try:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('pages/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                
                # Note: UserCreationForm doesn't have an email field by default.
                # If you need the email, you must use a custom form or add it.
                to_email = request.POST.get('email') 
                
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                
                return HttpResponse('<h1>Check your Gmail!</h1><p>Confirm your email to login.</p>')
            
            except Exception as e:
                return HttpResponse(f'User created (Inactive), but email failed to send: {e}')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})

def activate(request, uidb64, token):
    """Activates the user account when they click the email link."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Success! Your account is active. You can now login.')
    else:
        return HttpResponse('Activation link is invalid!')
    

def kanye_quote_view(request):
    # Fetch the quote from the external API
    response = requests.get('https://api.kanye.rest')
    data = response.json()
    quote = data.get('quote')

    return render(request, 'blog/kanye.html', {'quote': quote})



def create_post(request):
    if request.method == "POST":
        # Bind the submitted data to the form instance
        form = PostForm(request.POST)
        
        # This is the "Magic" step: Django validates types, lengths, and security
        if form.is_valid():
            # Save the new post to the database
            form.save()
            return redirect('post_list') 
    else:
        # Provide a blank form for the user to fill out
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})


@login_required # This is the "Security Guard" for this specific view
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Before saving, we link the post to the currently logged-in user
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})