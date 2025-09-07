from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active Listings", "listings": Listing.objects.filter(is_active=True)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = float(request.POST["starting_bid"])
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        owner = User.objects.get(username=request.user.username)

        owner_id = owner.id

        is_active = True

        listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, owner_id=owner_id, is_active=is_active)
        
        listing.save()
        owner.owned.add(listing)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

def change_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user.username)
    if listing in user.watchlisted.all():
        user.watchlisted.remove(listing)
    else:
        user.watchlisted.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def submit_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        amount = float(request.POST["bid"])
        if amount <= listing.highest_bid():
            return render(request, "auctions/listing.html", {
            "listing": listing, "message": "Error! Bid must be higher than the current bid."
        })
        user = User.objects.get(username=request.user.username)
        bid = Bid(amount=amount)
        bid.save()
        listing.bids.add(bid)
        user.bidden.add(bid)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))

def submit_comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        content = request.POST["comment"]
        if len(content) < 3:
            return render(request, "auctions/listing.html", {
            "listing": listing, "message1": "Error! Comment too short."
        })
        user = User.objects.get(username=request.user.username)
        comment = Comment(content=content)
        comment.save()
        listing.comments.add(comment)
        user.commented.add(comment)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
def watchlist(request):
    return render(request, "auctions/index.html", {
        "title": "Watchlist", "listings": Listing.objects.filter(watchlisters=User.objects.get(username=request.user.username))
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.objects.values_list('category', flat=True).distinct()
    })

def category(request, category):
    return render(request, "auctions/index.html", {
        "title": ("Category: " + category), "listings": Listing.objects.filter(category=category)
    })