from django.db.models.query import QuerySet
from .models import Bid, Comment, Listing, User, WatchList

PLACEHOLDER_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/1022px-Placeholder_view_vector.svg.png"


def parse_categories(categories_string: str) -> list[str]:

    return categories_string.split(" ")


def get_categories() -> list[str]:

    all_categories = set()

    for listing in Listing.objects.all():

        if listing.categories:
            all_categories.update(
                category.strip().title() 
                for category in listing.categories 
                if category
            )

    return sorted(all_categories)


def get_listings() -> QuerySet[Listing]:

    return Listing.objects.all()


def get_listing_by_id(listing_id: int) -> Listing:

    return Listing.objects.get(id=listing_id)


def get_active_listings() -> QuerySet[Listing]:

    return Listing.objects.filter(active_state=True).all()


def get_active_listings_by_category(category: str) -> list[Listing]:

    all_listings = get_active_listings()

    filtered_listings = [
        listing 
        for listing in all_listings
        for listing_category in listing.categories
        if listing_category.strip().title() == category
    ]

    return filtered_listings


def add_listing_to_watchlist(user: User, listing: Listing) -> None:

    WatchList.objects.create(user=user, listing=listing)
    

def delete_listing_from_watchlist(user: User, listing: Listing) -> None:

    WatchList.objects.filter(user=user, listing=listing).first().delete()


def is_listing_in_watchlist(user: User, listing: Listing) -> bool:

    return WatchList.objects.filter(user=user, listing=listing).exists()


def get_watchlist_by_user(user: User) -> list[Listing]:

    watchlist_objects = WatchList.objects.filter(user=user)

    watchlist_listings = [obj.listing for obj in watchlist_objects]

    return watchlist_listings


def get_comments_by_listing(listing: Listing) -> QuerySet[Comment]:

    return Comment.objects.filter(comment_listing=listing)


def get_highest_bid(listing: Listing) -> float:

    existing_bids = Bid.objects.filter(bid_listing=listing)

    if not (existing_bids.exists()):
        return listing.starting_bid

    highest_bid = max([bid.bid_amount for bid in existing_bids])

    return highest_bid


def is_valid_bid(bid: float, listing: Listing) -> bool:

    return bid > max(listing.starting_bid, get_highest_bid(listing))


def is_listing_created_by_user(user: User, listing_id: int) -> bool:

    return Listing.objects.filter(creation_user=user, id=listing_id).exists()


def is_auction_winner(user: User, listing_id: int) -> bool:
    
    selected_listing = get_listing_by_id(listing_id)
    
    # still active listing => False
    if selected_listing.active_state:
        return False
    
    highest_bid = get_highest_bid(selected_listing)
    
    # no match of 1. bid_amount and 2. bid_user => False
    return Bid.objects.filter(bid_amount=highest_bid, bid_user=user).exists()
