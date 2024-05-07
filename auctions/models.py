from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Auction_lists(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(null=True, blank=True)
    category = models.ManyToManyField(Category, related_name="auctions")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f" {self.title} at {self.starting_bid} by {self.created_by}"

 

class Bids(models.Model):
    auction = models.ForeignKey(Auction_lists, on_delete=models.CASCADE, related_name="bidders")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid} by {self.user} on {self.auction}"

class Comments(models.Model):
    auction = models.ForeignKey(Auction_lists, on_delete=models.CASCADE, related_name="commenters")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment} by {self.user} on {self.auction}"

class Watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    auction = models.ForeignKey(Auction_lists, on_delete=models.CASCADE, related_name="watchedby")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} watching {self.auction}"