from .models import Bid, Listing, User, WatchList

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


def get_listings_by_category(category: str):

    all_listings = Listing.objects.all()

    filtered_listings = [
        listing 
        for listing in all_listings
        for listing_category in listing.categories
        if listing_category.strip().title() == category
    ]

    return filtered_listings


def is_listing_in_watchlist(user: User, listing: Listing):

    return WatchList.objects.filter(user=user, listing=listing).exists()


def get_highest_bid(listing: Listing):
    
    existing_bids = Bid.objects.filter(bid_listing=listing)
    
    if not (existing_bids.exists()):
        return listing.starting_bid
    
    highest_bid = max([bid.bid_amount for bid in existing_bids])
    
    return highest_bid

def get_highest_user(highest_bid: float):
    
    return Bid.objects.filter(bid_amount=highest_bid).first().bid_user