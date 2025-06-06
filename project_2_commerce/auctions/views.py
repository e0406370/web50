from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from auctions import util
from .models import Bid, Comment, Listing, User


def index(request: HttpRequest) -> HttpResponse:

    listings = util.get_active_listings()

    return render(
        request, 
        template_name="auctions/index.html", 
        context={"listings": listings}
    )


def categories(request: HttpRequest) -> HttpResponse:

    categories = util.get_categories()

    return render(
        request, 
        template_name="auctions/categories.html", 
        context={"categories": categories}
    )


def category_listing(request: HttpRequest, category: str) -> HttpResponse:

    listings = util.get_active_listings_by_category(category)

    return render(
        request,
        template_name="auctions/categorylisting.html",
        context={"listings": listings, "category": category},
    )

    
def view_listing(request: HttpRequest, listing_id: int) -> HttpResponse:
    
    listing = util.get_listing_by_id(listing_id)
    user = request.user

    is_in_watchlist = False
    is_listing_created_by_user = False
    is_highest_bidder = False

    if user.is_authenticated:
        is_in_watchlist = util.is_listing_in_watchlist(user, listing)
        is_listing_created_by_user = util.is_listing_created_by_user(user, listing_id)
        is_highest_bidder = util.is_auction_winner(user, listing_id)

    comments = util.get_comments_by_listing(listing)
    highest_bid = util.get_highest_bid(listing)

    return render(
        request,
        template_name="auctions/listing.html",
        context={"listing": listing, 
         "listing_id": listing_id, 
         "is_in_watchlist": is_in_watchlist,
         "comments": comments,
         "highest_bid": highest_bid,
         "is_listing_created_by_user": is_listing_created_by_user,
         "is_highest_bidder": is_highest_bidder
        }
    )


def login_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(viewname="index"))
        else:
            return render(
                request,
                template_name="auctions/login.html",
                context={"message": "Invalid username and/or password."},
            )
    else:
        return render(
            request,
            template_name="auctions/login.html"
        )


def logout_view(request: HttpRequest) -> HttpResponseRedirect:

    logout(request)

    return HttpResponseRedirect(reverse(viewname="index"))


def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, 
                template_name="auctions/register.html", 
                context={"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                template_name="auctions/register.html",
                context={"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse(viewname="index"))
    
    else:
        return render(
            request,
            template_name="auctions/register.html"
        )


class ListingForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "name": "title"
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 
                "name": "description"
            }
        )
    )

    starting_bid = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control", 
                "name": "starting_bid"
            }
        )
    )

    image_url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "name": "image_url"
            }
        ),
        required=False,
    )

    categories = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "name": "categories"
                }
        ),
        required=False,
    )

    def clean(self) -> None:
        data = self.cleaned_data

        if data.get("title") is None:
            raise forms.ValidationError("Must indicate a title for the listing!")

        if data.get("description") is None:
            raise forms.ValidationError("Must indicate a description for the listing!")

        if data.get("starting_bid") is None:
            raise forms.ValidationError("Must indicate a starting bid for the listing!")


@login_required
def create_listing(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:

    if request.method == "POST":

        form = ListingForm(request.POST)

        if form.is_valid():
            listing_title = form.cleaned_data["title"]
            listing_description = form.cleaned_data["description"]
            listing_starting_bid = form.cleaned_data["starting_bid"]
            listing_image_url = form.cleaned_data["image_url"]
            listing_categories = form.cleaned_data["categories"]

            if not listing_image_url:
                listing_image_url = util.PLACEHOLDER_IMAGE

            new_listing = Listing.objects.create(
                title=listing_title,
                description=listing_description,
                starting_bid=listing_starting_bid,
                image_url=listing_image_url,
                categories=util.parse_categories(listing_categories),
                creation_user=request.user,
            )

            return redirect(
                to='listing',
                listing_id=new_listing.id
            )

        else:
            return render(
                request, 
                template_name="auctions/createlisting.html",
                context={"form": form}
            )

    return render(
        request, 
        template_name="auctions/createlisting.html",
        context={"form": ListingForm()}
    )


@login_required
def add_to_watchlist(request: HttpRequest, listing_id: int) -> HttpResponseRedirect:
    
    selected_listing = util.get_listing_by_id(listing_id)
    
    util.add_listing_to_watchlist(request.user, selected_listing)
    
    return HttpResponseRedirect(reverse(viewname="watchlist"))


@login_required
def delete_from_watchlist(request: HttpRequest, listing_id: int) -> HttpResponseRedirect:
    
    selected_listing = util.get_listing_by_id(listing_id)
    
    util.delete_listing_from_watchlist(request.user, selected_listing)
    
    return HttpResponseRedirect(reverse(viewname="watchlist"))


@login_required
def view_watchlist(request: HttpRequest):
    
    watchlist_listings = util.get_watchlist_by_user(request.user)
    
    return render(
        request, 
        template_name="auctions/watchlist.html",
        context={"watchlist": watchlist_listings}
    )


@login_required
def add_comment(request: HttpRequest, listing_id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    selected_listing = util.get_listing_by_id(listing_id)
    current_user = request.user

    if request.method == "POST":

        comment_text = request.POST["comment"]
        
        new_comment = Comment(
            comment_text=comment_text,
            comment_user=current_user,
            comment_listing=selected_listing,
        )
        new_comment.save()

    return redirect(
        to='listing',
        listing_id=selected_listing.id
    )


@login_required
def add_bid(request: HttpRequest, listing_id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    selected_listing = util.get_listing_by_id(listing_id)
    current_user = request.user

    if request.method == "POST":

        bid_amount = request.POST["bid"]

        if util.is_valid_bid(float(bid_amount), selected_listing):

            new_bid = Bid(
                bid_amount=bid_amount,
                bid_user=current_user,
                bid_listing=selected_listing,
            )
            new_bid.save()

            return redirect(
                to='listing',
                listing_id=selected_listing.id
            )

        else:
            error_message = "Invalid bid amount. Bid must be higher than the starting bid and the highest bid."
            messages.error(request, error_message)

            return redirect(
                to='listing', 
                listing_id=selected_listing.id
            )

    return redirect(
        to='listing',
        listing_id=selected_listing.id
    )


@login_required
def close_auction(request: HttpRequest, listing_id: int):

    selected_listing = util.get_listing_by_id(listing_id)

    selected_listing.active_state = False
    selected_listing.save()

    return HttpResponseRedirect(reverse(viewname="index"))