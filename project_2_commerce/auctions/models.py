from django.contrib.auth.models import AbstractUser
from django.db import models

# Comment -> User (1 Comment -> 1 User, 1 User -> Many Comments): OneToMany
# Bid -> User (1 Bid -> 1 User, 1 User -> Many Bids): OneToMany
# Listing -> User (1 Listing -> 1 User, 1 User -> Many Listings): OneToMany
# applies to Comment -> Listing, Bid -> Listing 

class User(AbstractUser):
    pass

# foreign key to user
class Listing(models.Model):

    ## DEFINED IN 'Create Listing' FORM
    title = models.CharField(max_length=64)  # required
    description = models.CharField(max_length=128)  # required
    starting_bid = models.FloatField()  # required
    image_url = models.URLField(max_length=128, blank=True, null=True)  # optional
    categories = models.JSONField(default=list, blank=True, null=True)  # optional

    ## INITIALISED UPON CREATION
    creation_date = models.DateTimeField(auto_now_add=True)  # when the listing was created
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")  # User who created the listing

# foreign key to user
# foreign key to listing
class Bid(models.Model):
    bid_amount = models.FloatField()  # value of bid in decimal
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")  # User linked to this bid
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")  # Listing linked to this bid


# foreign key to user
# foreign key to listing
class Comment(models.Model):
    comment_text = models.CharField(max_length=256)  # value of comment in string
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # User linked to this comment
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")  # Listing linked to this comment