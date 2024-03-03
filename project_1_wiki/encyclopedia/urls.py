from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.entry),
    path("wiki/<str:entry_title>", views.entry),
]
