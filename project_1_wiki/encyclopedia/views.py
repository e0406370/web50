import random
import markdownify

from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render

from markdown2 import Markdown
from . import util


def index(request: HttpRequest) -> HttpResponse:

    return render(
        request,
        template_name="encyclopedia/index.html",
        context={"entries": util.list_entries()},
    )


def search_entry(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:

    query = request.GET["q"]

    if not query:
        return redirect(
            to="index"
        )

    query = query.strip()
    entries = util.list_entries()
    results = []

    for entry in entries:
        if query == entry:
            return redirect(
                to="wiki",
                entry_title=entry
            )

        if query.lower() in entry.lower() != -1:
            results.append(entry)

    return render(
        request,
        template_name="encyclopedia/search.html",
        context={"query": query, "results": results},
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


def create_entry(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:

    if request.method == "POST":

        form = EntryForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_contents = form.cleaned_data["contents"]

            if util.get_entry(entry_title):
                messages.error(
                    request, 
                    message=f"Entry with title '{entry_title}' already exists."
                )

                return render(
                    request,
                    template_name="encyclopedia/create.html",
                    context={"form": form}
                )

            else:
                util.save_entry(
                    title=entry_title.strip(), 
                    content=markdownify.markdownify(entry_contents.strip())
                )

                return redirect(
                    to="wiki", 
                    entry_title=entry_title
                )

    return render(
        request,
        template_name="encyclopedia/create.html",
        context={"form": EntryForm()},
    )


def view_entry(request: HttpRequest, entry_title: str) -> HttpResponse:

    entry_contents = util.get_entry(entry_title)

    if entry_contents == None:
        return render(
            request, 
            template_name="encyclopedia/error.html", 
            context={"entry_title": entry_title}
        )

    markdowner = Markdown()
    entry_contents_converted = markdowner.convert(entry_contents)

    return render(
        request,
        template_name="encyclopedia/entry.html",
        context={"entry_title": entry_title, "entry_contents": entry_contents_converted},
    )


def edit_entry(request: HttpRequest, entry_title: str) -> HttpResponse:

    entry_contents = util.get_entry(entry_title)

    if entry_contents == None:
        return render(
            request,
            template_name="encyclopedia/error.html", 
            context={"entry_title": entry_title}
        )

    markdowner = Markdown()
    entry_contents_converted = markdowner.convert(entry_contents)

    return render(
        request,
        template_name="encyclopedia/edit.html",
        context={"entry_title": entry_title, "entry_contents": entry_contents_converted},
    )


def save_entry(request: HttpRequest, entry_title: str) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    if request.method == "POST":

        entry_contents = request.POST["edit"].strip()

        util.save_entry(
            title=entry_title, 
            content=markdownify.markdownify(entry_contents)
        )
        
        return redirect(
            to="wiki", 
            entry_title=entry_title
        )
        
    return redirect(
        to="index"
    )


def random_entry(request: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    random_entry = random.choice(util.list_entries())

    return redirect(
        to="wiki", 
        entry_title=random_entry
    )
