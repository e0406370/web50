import random
import markdownify

from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render

from markdown2 import Markdown

from . import util


def index(request):

    return render(
        request, 
        "encyclopedia/index.html", 
        {"entries": util.list_entries()}
    )


def search_entry(request):
    
    query = request.GET.get("q").strip()
    
    entries = util.list_entries()
    
    for entry in entries:
        if (query == entry):
            return redirect("wiki", entry_title=entry)
    
    results = []
    
    for entry in entries:
        if entry.lower().find(query.lower()) != -1:
            results.append(entry)
    
    return render(
        request, 
        "encyclopedia/search.html", 
        {"results": results, "query": query}
    )

    
class EntryForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "name": "title"
            }
        )
    )
    
    contents = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 
                "name": "contents"
            }
        )
    )


def create_entry(request):

    if request.method == "POST":

        form = EntryForm(request.POST)
    
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_contents = form.cleaned_data["contents"]
            
            if util.get_entry(entry_title):
                messages.error(request, f"Entry with title '{entry_title}' already exists.")
                
                return render(
                    request,
                    "encyclopedia/create.html",
                    {"form": form}
                )
                
            else:
                util.save_entry(
                    entry_title.strip(), 
                    markdownify.markdownify(entry_contents.strip())
                )
                
                return redirect("wiki", entry_title=entry_title)

    return render(
        request, 
        "encyclopedia/create.html", 
        {"form": EntryForm()}
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

        util.save_entry(
            entry_title, 
            markdownify.markdownify(entry_contents.strip())
        )
        
        return redirect("wiki", entry_title=entry_title)


def random_entry(request):

    random_entry = random.choice(util.list_entries())

    return redirect("wiki", entry_title=random_entry)
