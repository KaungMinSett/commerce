from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_lists, Category, Watchlists, Bids, Comments




def index(request):


    return render(request, "auctions/index.html", context={"auctions": Auction_lists.objects.all().order_by('-created_at')})


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

def get_bidder(id):
    auction = Auction_lists.objects.get(id=id)
    last_bidder = Bids.objects.filter(auction=auction).last()
    if last_bidder is None:
        bidder_name = None
    else:
        bidder_name = last_bidder.user
    return bidder_name

def view_details(request, id):

    auction = Auction_lists.objects.get(id=id)
    user = request.user
    bidder_name = get_bidder(id)


    if Watchlists.objects.filter(user=user, auction=auction).exists():
        status = True
    else:
        status = False
    
    comments = Comments.objects.filter(auction=auction)

    return render(request, "auctions/list_details.html", context={
        'auction': auction,
        'categories': auction.category.all(),
        'status': status,
        'last_bidder': bidder_name,
        'comments': comments,
    })


def toggle_watchlist(request, id):
    auction = Auction_lists.objects.get(id=id)
    user = request.user

    if Watchlists.objects.filter(user=request.user, auction=auction).exists():

        Watchlists.objects.filter(user=request.user, auction=auction).delete()
    else:
        Watchlists.objects.create(user=user, auction=auction)
    
    return HttpResponseRedirect(reverse("view_details", args=(auction.id,)))


        



def place_bid(request,id):
    user = request.user
    auction = Auction_lists.objects.get(id=id)
    bid = request.POST.get('current_bid')
    if int(bid) <= auction.starting_bid:
        bidder_name = get_bidder(id)
        return render(request, "auctions/list_details.html", {
            'auction': auction,
            'last_bidder': bidder_name,
            'error': "Your bid should be higher than the starting bid."
        })
    else:
        Bids.objects.create(user=user, auction=auction, bid=bid)
        Auction_lists.objects.filter(id=id).update(starting_bid=bid)
        return HttpResponseRedirect(reverse("view_details", args=(auction.id,)))
  


def close_auction(request, id):
    if request.user == Auction_lists.objects.get(id=id).created_by:
        auction = Auction_lists.objects.get(id=id)
        auction.is_active = False
        auction.save()
    else:
        return render(request, "auctions/list_details.html", {

            'error': "You are not authorized to close this auction."
        })
    return HttpResponseRedirect(reverse("view_details", args=(auction.id,)))

def add_comment(request, id):
    auction = Auction_lists.objects.get(id=id)
    user = request.user
    comment = request.POST.get('comment')
    Comments.objects.create(user=user, auction=auction, comment=comment)
    return HttpResponseRedirect(reverse("view_details", args=(auction.id,)))


def watchlist(request):
    user = request.user
    watchlists = Watchlists.objects.filter(user=user)  #get query set objects
    auction_ids = [watchlist.auction_id for watchlist in watchlists] # get related auction ids from watchlist
    auctions = Auction_lists.objects.filter(id__in=auction_ids) # get auction objects using auction ids
    
    return render(request, "auctions/watch_list.html", context={
        'auctions': auctions

        
    })

def view_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", context={
        'categories': categories
    })

def viewby_category(request, id):
    category = Category.objects.get(id=id)
    auctions = Auction_lists.objects.filter(category=category)

    return render(request, "auctions/list_by_category.html", context={
        'auctions': auctions,
        'category': category
    })