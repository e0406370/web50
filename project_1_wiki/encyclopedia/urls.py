from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.entry, name="error"),
    path("wiki/<str:entry_title>", views.entry, name="wiki"),
    path("random", views.random_entry, name="random")
]
