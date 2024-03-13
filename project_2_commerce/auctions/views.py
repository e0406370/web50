from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions import util

from .models import Listing, User


def index(request):
    return render(request, "auctions/index.html")


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
        )
    )
    
    categories = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "name": "categories"
            }
        )
    ) 

    def clean(self):
        data = self.cleaned_data
        
        if data.get('title') is None:
            raise forms.ValidationError('Must indicate a title for the listing!')
        
        if data.get('description') is None:
            raise forms.ValidationError('Must indicate a description for the listing!')
        
        if data.get('starting_bid') is None:
            raise forms.ValidationError('Must indicate a starting bid for the listing!')
            

def create_listing(request):

    if request.method == "POST":

        form = ListingForm(request.POST)
    
        if form.is_valid():
            listing_title = form.cleaned_data["title"]
            listing_description = form.cleaned_data["description"]
            listing_starting_bid = form.cleaned_data["starting_bid"]
            listing_image_url = form.cleaned_data["image_url"]
            listing_categories = form.cleaned_data["categories"]
            
            new_listing = Listing.objects.create(
                title = listing_title,
                description = listing_description,
                starting_bid = listing_starting_bid,
                image_url = listing_image_url | util.placeholder_image,
                categories = util.parse_categories(listing_categories) | util.no_category
            )
            
            return HttpResponseRedirect(reverse("index"))
        
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
