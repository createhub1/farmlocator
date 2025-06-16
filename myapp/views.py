from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile, FAQ
from django.views import View
import re

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == "farmer":
                    return redirect("farmer_dashboard") 
                else:
                    return redirect("consumer_dashboard") 
            except UserProfile.DoesNotExist:
                messages.error(
                    request, "User profile not found. Please contact support."
                )
                return redirect("login")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "consumer")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        latitude = request.POST.get("latitude") if role == "farmer" else None
        longitude = request.POST.get("longitude") if role == "farmer" else None
        farm_image = request.FILES.get("farm_image") if role == "farmer" else None

        if not all([username, email, password, confirm_password, first_name, last_name]):
            messages.error(request, "All fields are required!")
            return render(request, "signup.html")
        
        if not (first_name.isalpha() and last_name.isalpha()):
            messages.error(request, "First name and last name should contain only letters.")
            return render(request, 'signup.html')
        
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
            messages.error(request, "Password must be at least 8 characters long and contain at least one uppercase letter and one number.")
            return render(request, "signup.html")

        if password != confirm_password:
            messages.error(request, "Password and Confirm Password must be same!")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, "signup.html")

        if role == "farmer":
            if not all([latitude, longitude, farm_image]):
                messages.error(request, "Please select location and upload a farm image.")
                return render(request, "signup.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        UserProfile.objects.create(
            user=user,
            role=role,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None,
            farm_image=farm_image
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect("index")

def faq(request):
    if request.method == "POST":
        email = request.POST.get('email')
        title = request.POST.get('title')
        question = request.POST.get('question')
        
        faq = FAQ.objects.create(email=email, title=title, question=question)
        faq.save()
    
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')
        