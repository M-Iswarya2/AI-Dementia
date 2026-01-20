from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# -----------------------------
# Public Pages
# -----------------------------
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def instructions(request):
    return render(request, 'pages/instructions.html')

# -----------------------------
# Authentication Views
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'pages/login.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        
        errors = {}
        if not full_name: errors['full_name'] = 'Full name is required'
        if not email: errors['email'] = 'Email is required'
        if User.objects.filter(email=email).exists(): errors['email'] = 'Email already exists'
        if not username: errors['username'] = 'Username is required'
        if User.objects.filter(username=username).exists(): errors['username'] = 'Username already exists'
        if not password: errors['password'] = 'Password is required'
        elif len(password) < 6: errors['password'] = 'Password must be at least 6 characters'
        if password != confirm_password: errors['confirm_password'] = 'Passwords do not match'
        if not phone or len(phone) != 10: errors['phone'] = 'Phone must be 10 digits'
        
        if errors:
            return render(request, 'pages/register.html', {'errors': errors, 'form_data': request.POST})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name.split()[0] if full_name else ''
        user.last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
        user.save()
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'pages/register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

# -----------------------------
# Protected Pages
# -----------------------------
@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')

@login_required
def memory_select(request):
    return render(request, 'pages/memory_select.html')

# -----------------------------
# MEMORY TEST
# -----------------------------
@login_required
def memory_test(request):
    # Just render the template - Flask API handles the logic
    return render(request, 'pages/memory_test.html')

# -----------------------------
# ATTENTION TEST
# -----------------------------
@login_required
def attention_test(request):
    # Just render the template - Flask API handles the logic
    return render(request, 'pages/attention_test.html')

# ❌ REMOVED: memory_attention_start - Now handled by Flask
# ❌ REMOVED: memory_attention_submit - Now handled by Flask

# -----------------------------
# VOICE TEST
# -----------------------------
@login_required
def voice_test(request):
    # Just render the template - Flask API handles the logic
    return render(request, 'pages/voice_test.html')

# -----------------------------
# QUESTIONNAIRE
# -----------------------------
@login_required
def questions(request):
    # Just render the template - Flask API handles the logic
    return render(request, 'pages/questions.html')

# -----------------------------
# RESULTS
# -----------------------------
@login_required
def results(request):
    # Get scores from sessionStorage (sent from frontend)
    # The frontend will need to pass these as query parameters or POST data
    
    # For now, render the template and let the frontend handle the API call
    return render(request, "pages/results.html")