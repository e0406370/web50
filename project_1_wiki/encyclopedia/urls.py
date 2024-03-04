from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_entry, name="search"),
    path("errorwiki", views.view_entry, name="errorwiki"),
    path("wiki/<str:entry_title>", views.view_entry, name="wiki"),
    path("erroredit", views.edit_entry, name="erroredit"),
    path("edit/<str:entry_title>", views.edit_entry, name="edit"),
    path("save/<str:entry_title>", views.save_entry, name="save"),
    path("random", views.random_entry, name="random")
]
