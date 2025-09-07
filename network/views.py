from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow, Like

from django.http import JsonResponse

from django.core.paginator import Paginator

import json


def index(request):
    return render(request, "network/index.html", {
        "heading": "All Posts"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        author = User.objects.get(username=request.user.username)

        post = Post(content=content, author=author)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")

def get_page(request, section, page, name):
    if section == 'All Posts':
        posts = Post.objects.all()
    elif section == 'Following':
        follows = Follow.objects.filter(follower=request.user)
        posts = Post.objects.none()
        for follow in follows:
            posts = posts | Post.objects.filter(author=follow.followed)
    elif section == 'Profile':
        author = User.objects.get(username=name)
        posts = Post.objects.filter(author=author)
    else:
        return JsonResponse({"error": "Invalid section."}, status=400)
    
    posts = posts.order_by("-date").all()
    return Paginator(posts, 10).page(page)

def section(request, section, page, name):
    posts = get_page(request, section, page, name)
    return JsonResponse([post.serialize() for post in posts], safe=False)

def following(request):
    return render(request, "network/index.html", {
        "heading": "Following"
    })

def profile(request, author):
        user = User.objects.get(username=author)
        return render(request, "network/index.html", {
        "heading": "Profile", "author": user
    })

def follow_count(request, author):
    user = User.objects.get(username=author)
    follow1 = Follow.objects.filter(follower=user)
    follow2 = Follow.objects.filter(followed=user)
    count1 = follow1.count()
    count2 = follow2.count()
    count = {
        "following": count1,
        "followers": count2
    }
    return JsonResponse(count, safe=False)

def follow_status(request, author):
    follower = User.objects.get(username=request.user.username)
    followed = User.objects.get(username=author)
    follow = Follow.objects.filter(follower=follower, followed=followed)
    status = follow.exists()
    return JsonResponse(status, safe=False)

def flip_status(request, author):
    follower = User.objects.get(username=request.user.username)
    followed = User.objects.get(username=author)
    follow = Follow.objects.filter(follower=follower, followed=followed)
    if follow.exists():
        follow.delete()
    else:
        follow = Follow(follower=follower, followed=followed)
        follow.save()

def pages_present(request, section, page, name):
    posts = get_page(request, section, page, name)
    results = []
    results.append(posts.has_previous())
    results.append(posts.has_next())
    return JsonResponse(results, safe=False)

def edit_post(request, section, page, name, i):
    posts = get_page(request, section, page, name)
    post = posts[i]
    if post.author == request.user and request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

def switch_status(request, section, page, name, i):
    posts = get_page(request, section, page, name)
    post = posts[i]
    like = Like.objects.filter(liker=request.user, post=post)
    is_like = None
    if like.exists():
        like.delete()
        is_like = False
    else:
        like = Like(liker=request.user, post=post)
        like.save()
        is_like = True
    return JsonResponse(is_like, safe=False)

def is_liked(request, section, page, name, i):
    posts = get_page(request, section, page, name)
    post = posts[i]
    like = Like.objects.filter(liker=request.user, post=post)
    return JsonResponse(like.exists(), safe=False)