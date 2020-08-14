from django.contrib.auth import authenticate
from .models import User, Auction, Bid, Comment, Wishlist

def wishlist_count(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        try:
            wishlist = Wishlist.objects.get(user=user)
            wishlist_number = len(wishlist.wishlist_auction.all())
        except:
            wishlist_number = 0
    else:
        wishlist_number = None
    return {
        "wishlist_count": wishlist_number
    }