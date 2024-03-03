from django.shortcuts import render
from . import util
from markdown2 import Markdown

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    
    entry_contents = util.get_entry(entry_title)
    
    if (entry_contents == None):
        return render (request, "encyclopedia/error.html", {
            "entry_title": entry_title
        })
    
    markdowner = Markdown()
    entry_contents_converted = markdowner.convert(entry_contents)
    
    return render (request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry_contents": entry_contents_converted
    })    