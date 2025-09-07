from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import User, Exercise, Task
from django.db import IntegrityError
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "jpchars/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "jpchars/login.html", {
                "message": "Invalid input."
            })
    else:
        return render(request, "jpchars/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "jpchars/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError as e:
            print(e)
            return render(request, "jpchars/register.html", {
                "message": "Username already taken."
            })
        except ValueError as e:
            print(e)
            return render(request, "jpchars/register.html", {
                "message": "Invalid input."
            })
    else:
        return render(request, "jpchars/register.html")
    
def get_levels(request):
    user = User.objects.get(username=request.user.username)
    levels = []
    levels.append(user.hiragana_level)
    levels.append(user.katakana_level)

    return JsonResponse(levels, safe=False)

def get_exercises(request):
    exercises = Exercise.objects.all()
    return JsonResponse([exercise.serialize() for exercise in exercises], safe=False)

import random

def get_tasks(request, type, level):
    tasks = Task.objects.filter(type=type, min_level=level)

    primary = [task for task in tasks if task.priority == True]
    others = [task for task in tasks if task.priority == False]
    random.shuffle(others)
    tasks = primary + others

    return JsonResponse([task.serialize() for task in tasks], safe=False)


@csrf_exempt
@login_required
def update_level(request):
    user = User.objects.get(username=request.user.username)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(user.hiragana_level)
        if data.get("type") is not None and data.get("level") is not None:

            if data["type"] == "hiragana":
                if user.hiragana_level >= data["level"]:
                    print("Lower level")
                else:
                    exercises = Exercise.objects.filter(level__gte=data["level"],type=data["type"])
                    if len(exercises) > 1:
                        if exercises[1].level % 100 == 0:
                            user.hiragana_level = exercises[1].level
                        else:
                            user.hiragana_level = data["level"]
                    else:
                        user.hiragana_level = data["level"]

            else:
                if user.katakana_level >= data["level"]:
                    print("Lower level")
                else:
                    exercises = Exercise.objects.filter(level__gte=data["level"],type=data["type"])
                    if len(exercises) > 1:
                        if exercises[1].level % 100 == 0:
                            user.katakana_level = exercises[1].level
                        else:
                            user.katakana_level = data["level"]
                    else:
                        user.katakana_level = data["level"]

        user.save()
        if data["type"] == "hiragana":
            return JsonResponse(user.hiragana_level, safe=False)
        else:
            return JsonResponse(user.katakana_level, safe=False)