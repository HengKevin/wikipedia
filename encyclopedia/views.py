import markdown2 as mk2
from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import secrets

class NewPageForm(forms.Form):
    title = forms.CharField(label="New Title", widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    mk = mk2.Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExisting.html", {
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": mk.convert(entryPage),
            "entryTitle": entry
        })

def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    else:
        subStr = [entry for entry in util.list_entries() if value.upper() in entry.upper()]
        return render(request, "encyclopedia/index.html", {
                    "entries": subStr,
                    "search": True,
                    "value": value
                })
        

def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data['edit'] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs=({'entry': title})))
            else:
                return render(request, "encyclopedia/newPage.html", {
                    "form": form,
                    "existing":True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "form": NewPageForm(),
            "existing": False
        })

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExisting.html", {
            "entryTitle": entry
        })
    else:
        form = NewPageForm()
        form.fields['title'].initial = entry
        form.fields['title'].widget = forms.HiddenInput()
        form.fields['content'].initial = entryPage
        form.fields['edit'].initial = True
        return render(request, "encyclopedia/newPage.html", {
            "form": form,
            "edit": form.fields['edit'].initial,
            "entryTitle": form.fields['title'].initial
        })

def random(request):
    list_all = util.list_entries()
    randomPage = secrets.choice(list_all)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomPage}))
