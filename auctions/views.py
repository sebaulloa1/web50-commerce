from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages

from .models import User, Auction, Bid, Comment, Wishlist

class CreateListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=32)
    description = forms.CharField(label='Item Description', widget=forms.Textarea())
    starting_bid = forms.IntegerField(label='Starting bid', min_value=0)
    img_url = forms.CharField(label='Image URL (optional)', required=False)
    CATEGORY_CHOICES = [
        ('ART', 'Collectibles & Art'),
        ('ELECTRONICS', 'Electronics'),
        ('FASHION', 'Fashion'),
        ('HOME', 'Home & Garden'),
        ('PARTS', 'Parts & Accesories'),
        ('MUSICAL', 'Musical Instruments & gear'),
        ('SPORT', 'Sporting goods'),
        ('TOYS', 'Toys & Hobbies'),
        (None, 'Other categories')
    ]
    category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES, required=False)

class NewBidForm(forms.Form):
    bid_ammount = forms.IntegerField(min_value=0, label=None)

class NewCommentForm(forms.Form):
    comment_content = forms.CharField(label="Create a comment", widget=forms.Textarea(attrs={'class' : 'create-comment', 'autocomplete' : 'off'}), max_length=150)

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def index(request):
    listing = Auction.objects.all()
    closed = False
    for auction in listing:
        if not auction.active:
            closed = True
    return render(request, "auctions/index.html", {
        'auctions': listing,
        'closed': closed
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
            messages.success(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
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
            messages.success(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.success(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        messages.success(request, "Registered successfully.")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def listing(request, id):
    if request.method == "GET":
        auction = Auction.objects.get(pk=id)
        bids_count = Bid.objects.filter(bid_listing=id).count()
        form_min = float(auction.starting_bid)
        bid_price = usd(auction.starting_bid)
        current_bidder = Bid.objects.filter(bid_listing=id).order_by('-bid')
        comments = Comment.objects.filter(comment_auction=id)

        user = User.objects.get(pk=request.user.id)
        wishlist_auction = Auction.objects.get(pk=id)
        try:
            wishlist = Wishlist.objects.get(user=user.id, wishlist_auction=wishlist_auction)
            is_wishlist = True
        except:
            is_wishlist = False
        

        listing_creator = False
        if auction.auction_user.id == request.user.id:
            listing_creator = True
        if current_bidder:
            current_bidder = current_bidder.first()  
            if float(current_bidder.bid) >= float(auction.starting_bid):
                bid_price = usd(float(current_bidder.bid))
                form_min = float(current_bidder.bid) + 0.01
        
            if current_bidder.bid_user.id == request.user.id:
                auction.starting_bid = usd(auction.starting_bid)
                return render(request, "auctions/listing.html", {
                    "auction": auction,
                    "bids_count": bids_count,
                    "bid_price": bid_price,
                    "current_bidder": True,
                    "bid_form": NewBidForm(),
                    "category": auction.get_category_display(),
                    "form_min": form_min,
                    "listing_creator": listing_creator,
                    "comments": comments,
                    "comments_form": NewCommentForm(),
                    "is_wishlist": is_wishlist
                })
            else:
                auction.starting_bid = usd(auction.starting_bid)
                return render(request, "auctions/listing.html", {
                    "auction": auction,
                    "bids_count": bids_count,
                    "bid_price": bid_price,
                    "current_bidder": False,
                    "bid_form": NewBidForm(),
                    "category": auction.get_category_display(),
                    "form_min": form_min,
                    "listing_creator": listing_creator,
                    "comments": comments,
                    "comments_form": NewCommentForm(),
                    "is_wishlist": is_wishlist
                })
        else:
            auction.starting_bid = usd(auction.starting_bid)
            return render(request, "auctions/listing.html", {
                    "auction": auction,
                    "bids_count": 0,
                    "bid_price": bid_price,
                    "current_bidder": False,
                    "bid_form": NewBidForm(),
                    "category": auction.get_category_display(),
                    "form_min": form_min,
                    "listing_creator": listing_creator,
                    "comments": comments,
                    "comments_form": NewCommentForm(),
                    "is_wishlist": is_wishlist
                })
    else:
        new_bid_ammount = request.POST["bid_ammount"]
        new_bid = Bid(bid_listing=Auction.objects.get(pk=id), bid=new_bid_ammount, bid_user=User.objects.get(pk=request.user.id))
        new_bid.save()
        Auction.objects.filter(pk=id).update(current_bid=new_bid_ammount)
        return HttpResponseRedirect(reverse("listing", args=[id]))



@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "form": CreateListingForm().as_p()
        })
    else:
        new_listing = CreateListingForm(request.POST)
        print(new_listing.errors.as_data())
        if new_listing.is_valid():
            title = new_listing.cleaned_data['title']
            description = new_listing.cleaned_data['description']
            starting_bid = new_listing.cleaned_data['starting_bid']
            img_url = new_listing.cleaned_data['img_url']
            category = new_listing.cleaned_data['category']
            listing = Auction(title=title, description=description, starting_bid=starting_bid, img_url=img_url, category=category, auction_user=User.objects.get(pk=request.user.id), current_bid=starting_bid)
            listing.save()
            messages.success(request, "Auction created.")
            return HttpResponseRedirect(reverse("index"))
    


@login_required
def close_auction(request, id):
    auction = Auction.objects.get(pk=id)

    user = User.objects.get(pk=request.user.id)
    try:
        wishlist = Wishlist.objects.get(user=user.id, wishlist_auction=auction)
        is_wishlist = True
    except:
        is_wishlist = False

    listing_creator = False
    if auction.auction_user.id == request.user.id:
        listing_creator = True
    auction.starting_bid = usd(auction.starting_bid)
    auction_bidder = Bid.objects.filter(bid_listing=id).order_by('-bid')
    if not auction_bidder:
        Auction.objects.filter(pk=id).update(active=False)
        bid_price = usd(float(auction.starting_bid))
        return render(request, "auctions/closed_auction.html", {
            "auction": auction,
            "bid_price": bid_price,
            "category": auction.get_category_display(),
            "listing_creator": listing_creator,
            "is_wishlist": is_wishlist
        })
    else:
        auction_bidder = auction_bidder.first()
        auction_winner = User.objects.get(pk=auction_bidder.bid_user.id)
        winner = False
        if auction_winner.id == request.user.id:
            winner = True
        Auction.objects.filter(pk=id).update(active=False, auction_winner=auction_bidder.bid_user.id)
        bid_price = usd(auction_bidder.bid)
        return render(request, "auctions/closed_auction.html", {
            "auction": auction,
            "bid_price": bid_price,
            "category": auction.get_category_display(),
            "listing_creator": listing_creator,
            "winner": winner,
            "is_wishlist": is_wishlist
        })

@login_required
def new_comment(request, id):
    if request.method == "POST":
        comment = NewCommentForm(request.POST)
        if comment.is_valid():
            comment_content = comment.cleaned_data["comment_content"]
            comment_user = User.objects.get(pk=request.user.id)
            comment_auction = Auction.objects.get(pk=id)
            new_comment = Comment(comment=comment_content, comment_user=comment_user, comment_auction=comment_auction)
            new_comment.save()
            messages.success(request, "New comment added.")
            return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def add_wishlist(request, id):
    user = User.objects.get(pk=request.user.id)
    print(Wishlist.objects.all())
    auction = Auction.objects.get(pk=id)
    wishlist = Wishlist.objects.get_or_create(user=user)
    try:
        wishlist.wishlist_auction.add(auction)
    except:
        wishlist = Wishlist.objects.get(user=user)
        wishlist.wishlist_auction.add(auction)
    messages.success(request, "Added to your Wishlist.")
    return HttpResponseRedirect(reverse("listing", args=[id]))
    
@login_required
def wishlist(request):
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        wishlist = Wishlist.objects.filter(user=user.id)
        if not wishlist:
            return render(request, "auctions/wishlist.html", {
                "wishlist": None
            })
        else:
            return render(request, "auctions/wishlist.html", {
                "wishlist": wishlist[0].wishlist_auction.all()
            })

def remove_wishlist(request, id):
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        auction = Auction.objects.get(pk=id)
        wishlist = Wishlist.objects.get(user=user.id)
        wishlist.wishlist_auction.remove(auction)
        messages.success(request, "Removed from your Wishlist.")
        return HttpResponseRedirect(reverse("listing", args=[id]))

def remove_wishlist_closed(request, id):
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        auction = Auction.objects.get(pk=id)
        wishlist = Wishlist.objects.get(user=user.id)
        wishlist.wishlist_auction.remove(auction)
        messages.success(request, "Removed from your Wishlist.")
        return HttpResponseRedirect(reverse("closed_auction", args=[id]))

def categories(request):
    if request.method =="GET":
        return render(request, "auctions/categories.html")

def category(request, code):
    if request.method == "GET":
        if code == 'other':
            auctions = Auction.objects.filter(category='', active=True)
        else:
            auctions = Auction.objects.filter(category=code, active=True)
        return render(request, "auctions/category.html", {
            "code": code,
            "auctions": auctions
        })

def delete_auction(request, id):
    if request.method == "GET":
        auction = Auction.objects.get(id=id)
        auction.delete()
        messages.success(request, "Auction deleted.")
        return HttpResponseRedirect("index")
