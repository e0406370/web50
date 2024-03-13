from django.contrib import admin
from auctions.models import Listing, Bid, Comment, WatchList

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "image_url", "categories", "creation_date", "creation_user", "active_state")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_amount", "bid_user", "bid_listing")
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment_text", "comment_user", "comment_listing")
       
class WatchListAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")
    
# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList, WatchListAdmin)