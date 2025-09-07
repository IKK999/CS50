from django.shortcuts import render

from . import util

import markdown

from django import forms

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from random import randint

import os


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def byTitle(request, title):
    markdown_content = util.get_entry(title)
    
    if markdown_content == None:
        return render(request, "encyclopedia/notFound.html", {
            "title": title
        })
    
    html_content = markdown.markdown(markdown_content)

    with open("encyclopedia/templates/encyclopedia/byTitle.html", 'w') as html_file:
        html_file.write(f"{{% extends \"encyclopedia/layout.html\" %}}{{% block title %}}{title}{{% endblock %}}{{% block body %}}<a href=\"../edit/{title}\" style=\"float: right; margin-right: 2%;\">Edit</a><br>{html_content}{{% endblock %}}")
    
    return render(request, "encyclopedia/byTitle.html")

def search(request):
    query = request.GET.get('q')
    markdown_content = util.get_entry(query)

    if markdown_content != None:
        return byTitle(request, query)

    searchCode = f"{{% extends \"encyclopedia/layout.html\" %}}{{% block title %}}{query}{{% endblock %}}{{% block body %}}<h1>Search Results</h1>"

    entries = util.list_entries()
    for entry in entries:
        if query in entry:
            searchCode += f"<li><a href=\"../wiki/{entry}\">{entry}</a></li>"
    searchCode += "{% endblock %}"
    with open("encyclopedia/templates/encyclopedia/search.html", 'w') as html_file:
        html_file.write(searchCode)

    return render(request, "encyclopedia/search.html")

def edit(request, title):
    if request.method == "POST":
        form = OldContentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            with open(f"entries/{title}.md", "w") as file:
                file.write(content)

            return HttpResponseRedirect(f"../wiki/{title}")
            
        else:
            return render(request, "edit.html", {
                "title": title, "content": form
            })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title, "content": OldContentForm(title=title)
    })

def create(request):
    if request.method == "POST":
        form1 = NewTitleForm(request.POST)
        form2 = NewContentForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            title = form1.cleaned_data["title"]
            content = form2.cleaned_data["content"]

            if os.path.exists(f"entries/{title}.md"):
                return render(request, "encyclopedia/exists.html", {
                    "title": title
                })
            else:
                with open(f"entries/{title}.md", "w") as file:
                    file.write(content)

                return HttpResponseRedirect(f"../wiki/{title}")
            
        else:
            return render(request, "create.html", {
                "title": form1, "content": form2
            })
    
    return render(request, "encyclopedia/create.html", {
        "title": NewTitleForm(), "content": NewContentForm()
    })


class NewTitleForm(forms.Form):
    title = forms.CharField(label="New Title", widget=forms.Textarea(attrs={'style': 'padding: 3px; margin: 3px; width: 80vw; height: 5vh;'}))

class NewContentForm(forms.Form):
    content = forms.CharField(label="New Content", widget=forms.Textarea(attrs={'style': 'padding: 3px; margin: 3px; width: 80vw; height: 40vh;'}))

class OldContentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        title = kwargs.pop('title', '')
        super().__init__(*args, **kwargs)
        self.fields['content'].initial = util.get_entry(title)

    content = forms.CharField(label="Edit Page", widget=forms.Textarea(attrs={'style': 'padding: 3px; margin: 3px; width: 80vw; height: 40vh;'}))

def random(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    return byTitle(request, title)