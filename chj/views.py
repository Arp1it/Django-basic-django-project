from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    chsud = Chatting.objects.order_by("timestamp")
    lusch = Chatting.objects.last()
    # print(lusch)
    return render(request, "chat.html", {"userschat": chsud, "lchsd": lusch})

def chat(request):
    if request.method == "POST":
        user = request.user
        userch = request.POST["user_chatter"]

        chsu = Chatting(cuser=user, chattts=userch)
        chsu.save()
    return redirect("/")

def user_signin(request):
    if request.method == "POST":
        name = request.POST["username"]
        ugmail = request.POST["user_email"]
        passs = request.POST["password"]

        mwuser = User.objects.create_user(username=name, email=ugmail, password=passs)
        mwuser.save()

        user = authenticate(username=name, password=passs)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/")

    return redirect("/")

def user_login(request):
    if request.method == "POST":
        name = request.POST["username"]
        passs = request.POST["password"]

        user = authenticate(username=name, password=passs)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/")
    return redirect("/")

def user_logout(request):
    logout(request)
    return redirect("/")