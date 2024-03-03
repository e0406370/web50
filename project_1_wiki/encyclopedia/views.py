from . import util

from django.shortcuts import render
from django.shortcuts import redirect

from markdown2 import Markdown
import random

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
    
def random_entry(request):
    
    random_entry = random.choice(util.list_entries())
    
    return redirect("wiki", entry_title = random_entry)