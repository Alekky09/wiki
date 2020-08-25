from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
import random

def index(request):
    if request.method == "POST":
        query = request.POST["q"]

        if query in util.list_entries():
            return HttpResponseRedirect(reverse("entryPage", args=(query, )))

        else:
            entries= []
            for entry in util.list_entries():
                if query in entry:
                    entries.append(entry)
            
            return render(request, "encyclopedia/query_page.html", {
                "entries": entries
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request, title):

    if request.method == "POST":
        entry = request.POST["entry"]
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit_entry.html", {
            "title": entry,
            "content": content
        })

        
    entry = util.get_entry(title)
    if entry:
        markdown = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry_page.html", {
            "entry": title,
            "markdown": markdown
        })

    else:
        return render(request, "encyclopedia/error_page.html", {
            "error": "Requested page not found."
        })

def newEntry(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if title in util.list_entries():
            return render(request, "encyclopedia/error_page.html", {
                "error": "Entry already exists."
            })

        formatted_content = f"#{title}" + "\n" + f"{content}"

        util.save_entry(title, formatted_content)

        return HttpResponseRedirect(reverse("entryPage", args=(title, )))


    return render(request, "encyclopedia/new_entry.html")

def randomPage(request):

    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entryPage", args=(entry, )))

def editEntry(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("entryPage", args=(title, )))
    
    
    return render(request, "encyclopedia/error_page.html", {
        "error": "Method not allowed."
    })
