import random
import markdownify

from django import forms
from django.shortcuts import redirect, render
from markdown2 import Markdown

from . import util


def index(request):

    return render(
        request, 
        "encyclopedia/index.html", 
        {"entries": util.list_entries()}
    )


def view_entry(request, entry_title):

    entry_contents = util.get_entry(entry_title)

    if entry_contents == None:
        return render(
            request, 
            "encyclopedia/error.html", 
            {"entry_title": entry_title}
        )

    markdowner = Markdown()
    entry_contents_converted = markdowner.convert(entry_contents)

    return render(
        request,
        "encyclopedia/entry.html",
        {"entry_title": entry_title, "entry_contents": entry_contents_converted},
    )


def edit_entry(request, entry_title):

    entry_contents = util.get_entry(entry_title)

    if entry_contents == None:
        return render(
            request, 
            "encyclopedia/error.html", 
            {"entry_title": entry_title}
        )

    markdowner = Markdown()
    entry_contents_converted = markdowner.convert(entry_contents)

    return render(
        request,
        "encyclopedia/edit.html",
        {"entry_title": entry_title, "entry_contents": entry_contents_converted},
    )


def save_entry(request, entry_title):

    if request.method == "POST":

        entry_contents = request.POST.get("edit").strip()

        util.save_entry(entry_title.capitalize(), markdownify.markdownify(entry_contents.strip()))
        
        return redirect("wiki", entry_title=entry_title)


        
def random_entry(request):

    random_entry = random.choice(util.list_entries())

    return redirect("wiki", entry_title=random_entry)
