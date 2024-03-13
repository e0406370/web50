from .models import Bid, Comment, Listing, User, WatchList

placeholder_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/1022px-Placeholder_view_vector.svg.png"


def parse_categories(categories_string: str):

    return categories_string.split(" ")


def get_categories():

    all_categories = set()

    for listing in Listing.objects.all():

        if listing.categories:
            all_categories.update(
                category.strip().title() 
                for category in listing.categories 
                if category
            )

    return sorted(all_categories)


def get_listings():
    
    return Listing.objects.all()


def get_listing_by_id(listing_id: int):
    
    return Listing.objects.get(id=listing_id)


def get_listings_by_category(category: str):

    all_listings = Listing.objects.all()

    filtered_listings = [
        listing 
        for listing in all_listings
        for listing_category in listing.categories
        if listing_category.strip().title() == category
    ]

    return filtered_listings


def add_listing_to_watchlist(user: User, listing: Listing):
    
    WatchList.objects.create(user=user, listing=listing)
    

def delete_listing_from_watchlist(user: User, listing: Listing):
    
    WatchList.objects.filter(user=user, listing=listing).first().delete()


def is_listing_in_watchlist(user: User, listing: Listing):

    return WatchList.objects.filter(user=user, listing=listing).exists()


def get_watchlist_by_user(user: User):
    
    watchlist_objects = WatchList.objects.filter(user=user)

    watchlist_listings = [obj.listing for obj in watchlist_objects]
    
    return watchlist_listings


def get_comments_by_listing(listing: Listing):
    
    return Comment.objects.filter(comment_listing=listing)


def get_highest_bid(listing: Listing):
    
    existing_bids = Bid.objects.filter(bid_listing=listing)
    
    if not (existing_bids.exists()):
        return listing.starting_bid
    
    highest_bid = max([bid.bid_amount for bid in existing_bids])
    
    return highest_bid