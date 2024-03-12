from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.model):

    ## DEFINED IN 'Create Listing' FORM
    title = models.CharField(max_length=64)  # required
    description = models.CharField(max_length=128)  # required
    starting_bid = models.FloatField()  # required
    image_url = models.URLField(max_length=128, blank=True, null=True)  # optional
    categories = models.JSONField(default=list, blank=True, null=True)  # optional

    ## INITIALISED UPON CREATION
    listing_id = models.UUIDField()  # path variable for accessing listings
    creation_date = models.DateTimeField(auto_now_add=True)  # when the listing was created
    creation_user = models.CharField() # user who created the listing
    comments = models.JSONField(default=list, blank=True, null=True) # comment field
    bid_quantity = models.IntegerField(default=0) # bid field
