from django.contrib.auth.models import AbstractUser
from django.db import models

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    content = models.CharField(max_length=512)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    bids = models.ManyToManyField(Bid, blank=True, related_name="listings")
    comments = models.ManyToManyField(Comment, blank=True, related_name="listings")
    owner_id = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def highest_bid(self):
        if self.bids.all():
            return max([bid.amount for bid in self.bids.all()])
        else:
            return self.starting_bid
        
    def bid_count(self):
        return len(self.bids.all())
    
    def bid_leader(self):
        if self.bid_count() == 0:
            return None
        else:
            return User.objects.get(bidden=self.bids.all().order_by('-amount')[0])
        
    def listing_owner(self):
        return User.objects.get(owned=self)
    
    def get_comments(self):
        return self.comments.all()

class User(AbstractUser):
    owned = models.ManyToManyField(Listing, blank=True, related_name="owners")
    watchlisted = models.ManyToManyField(Listing, blank=True, related_name="watchlisters")
    bidden = models.ManyToManyField(Bid, blank=True, related_name="bidders")
    commented = models.ManyToManyField(Comment, blank=True, related_name="commenters")

    def watchlist_count(self):
        return len(self.watchlisted.all())