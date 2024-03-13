from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("createlisting", views.create_listing, name="createlisting"),
    path("categories", views.categories, name="categories"),
    
    path("listing/category/<str:category>", views.category_listing, name="categorylisting"),
    path("listing/id/<int:listing_id>", views.view_listing, name="listing"),
    
    path("watchlist/add/<int:listing_id>", views.add_to_watchlist, name="watchlistadd"),
    path("watchlist/delete/<int:listing_id>", views.delete_from_watchlist, name="watchlistdelete"),
    path("watchlist", views.view_watchlist, name="watchlist"),
    
    path("addcomment/<int:listing_id>", views.add_comment, name="addcomment"),
    path("addbid/<int:listing_id>", views.add_bid, name="addbid")
]
