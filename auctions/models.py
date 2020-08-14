from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.TextField(null=True, blank=True)
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
    category = models.CharField(max_length=11, choices=CATEGORY_CHOICES, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    auction_user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True, blank=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    auction_winner = models.IntegerField(null=True, blank=True)
    
    def __str__ (self):
        return f"{self.id}: {self.title} {self.category} {self.starting_bid}"

class Bid(models.Model):
    bid_listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        return f"{self.id}: {self.bid_listing.title} {self.bid}"

class Comment(models.Model):
    comment = models.TextField()
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_dt = models.DateTimeField(auto_now_add=True)
    comment_auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__ (self):
        return f"{self.id}: {self.comment_auction.title} '{self.comment}' by {self.comment_user.username}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist_auction = models.ManyToManyField(Auction, blank=True)
    
    def __str__ (self):
        return f"{self.id}: {self.user}"
