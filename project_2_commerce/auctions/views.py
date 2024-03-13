from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from auctions import util

from .models import Comment, Listing, User, WatchList


def index(request):

    listings = Listing.objects.all()

    return render(
        request, 
        "auctions/index.html", 
        {"listings": listings}
    )


def categories(request):

    categories = util.get_categories()

    return render(
        request, 
        "auctions/categories.html", 
        {"categories": categories}
    )


def category_listing(request, category):

    listings = util.get_listings_by_category(category)

    return render(
        request,
        "auctions/categorylisting.html",
        {"listings": listings, "category": category},
    )
 
    
def view_listing(request, listing_id):
    
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    is_in_watchlist = False
    
    if user.is_authenticated:
        is_in_watchlist = util.is_listing_in_watchlist(user, listing)
    
    comments = Comment.objects.filter(comment_listing=listing)

    return render(
        request,
        "auctions/listing.html",
        {"listing": listing, 
         "listing_id": listing_id, 
         "is_in_watchlist": is_in_watchlist,
         "comments": comments
        }
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, 
                "auctions/register.html", 
                {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/register.html")


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

    def clean(self):
        data = self.cleaned_data

        if data.get("title") is None:
            raise forms.ValidationError("Must indicate a title for the listing!")

        if data.get("description") is None:
            raise forms.ValidationError("Must indicate a description for the listing!")

        if data.get("starting_bid") is None:
            raise forms.ValidationError("Must indicate a starting bid for the listing!")


@login_required
def create_listing(request):

    if request.method == "POST":

        form = ListingForm(request.POST)

        if form.is_valid():
            listing_title = form.cleaned_data["title"]
            listing_description = form.cleaned_data["description"]
            listing_starting_bid = form.cleaned_data["starting_bid"]
            listing_image_url = form.cleaned_data["image_url"]
            listing_categories = form.cleaned_data["categories"]

            if not listing_image_url:
                listing_image_url = util.placeholder_image

            new_listing = Listing.objects.create(
                title=listing_title,
                description=listing_description,
                starting_bid=listing_starting_bid,
                image_url=listing_image_url,
                categories=util.parse_categories(listing_categories),
                creation_user=request.user,
            )

            return HttpResponseRedirect(reverse("listing"), args=(new_listing.id))

        else:
            return render(
                request, 
                "auctions/createlisting.html", 
                {"form": form}
            )

    return render(
        request, 
        "auctions/createlisting.html", 
        {"form": ListingForm()}
    )

@login_required
def add_to_watchlist(request, listing_id):
    selected_listing = Listing.objects.get(id=listing_id)
    
    WatchList.objects.create(user=request.user, listing=selected_listing)
    
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def delete_from_watchlist(request, listing_id):
    selected_listing = Listing.objects.get(id=listing_id)
    
    WatchList.objects.filter(user=request.user, listing=selected_listing).first().delete()
    
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def view_watchlist(request):
    
    watchlist_objects = WatchList.objects.filter(user=request.user)
    
    watchlist_listings = [obj.listing for obj in watchlist_objects]
    
    return render(
        request, 
        "auctions/watchlist.html",
        {"watchlist": watchlist_listings}
    )
    
@login_required
def add_comment(request, listing_id):
    
    selected_listing = Listing.objects.get(id=listing_id)
    current_user = request.user
    
    if (request.method == "POST"):
        
        comment_text = request.POST.get("comment")
        
        new_comment = Comment(
            comment_text=comment_text,
            comment_user=current_user,
            comment_listing=selected_listing,
        )
        new_comment.save()
        
    return redirect('listing', listing_id=selected_listing.id)