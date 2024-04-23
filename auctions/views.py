from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_lists, Category, Watchlists



def index(request):

    return render(request, "auctions/index.html", context={"auctions": Auction_lists.objects.all()})


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

def create_list(request):
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        if int(starting_bid) <= 0:
            return render(request, "auctions/create_list.html", {
                'categories': Category.objects.all(),
                "error": "Starting bid should start from $1.00."
            })
        image_url = request.POST.get('image_url')
        categories = request.POST.getlist('category')
    
        if title == "" or title.strip() == "":
             return render(request, "auctions/create_list.html", {
                'categories': Category.objects.all(),
                "error": "Please fill the title."
            })
        else:

            created_by = request.user
            created_at = request.POST.get('created_at')
            auction_list = Auction_lists.objects.create(
            title=title, 
            description=description, 
            starting_bid=starting_bid, 
            image_url=image_url, 

            created_by=created_by, 
            created_at=created_at
            )
            for category in categories:
                category_id = Category.objects.filter(name=category).first() # get the category id
                auction_list.category.add(category_id)
        
            return HttpResponseRedirect(reverse("index"))
    
           
    return render(request, "auctions/create_list.html", context={
        'categories': Category.objects.all()
    }
    )


def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('category')
        
        try:
            Category.objects.create(name=name)
            return HttpResponseRedirect(reverse("create"))
        except IntegrityError:
            return render(request, "auctions/create_category.html", {
                "error": "Category already exists."
            })
    return render(request, "auctions/create_category.html")


def view_details(request, id):

    auction = Auction_lists.objects.get(id=id)
    user = request.user

    category = Category.objects.filter(auctions=auction).first()
    if Watchlists.objects.filter(user=user, auction=auction).exists():
        status = True
    else:
        status = False
    return render(request, "auctions/list_details.html", context={
        'auction': auction,
        'category': category,
        'status': status
    })


def toggle_watchlist(request, id):
    auction = Auction_lists.objects.get(id=id)
    user = request.user

    if Watchlists.objects.filter(user=request.user, auction=auction).exists():

        Watchlists.objects.filter(user=request.user, auction=auction).delete()
    else:
        Watchlists.objects.create(user=user, auction=auction)
    
    return HttpResponseRedirect(reverse("view_details", args=(auction.id,)))
        



    
  


    