from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from datafeed.models import State, Column



def index(request):
    states = State.objects.all().order_by('name')
    columns = [x for x in Column.objects.all() if x.description != "EDIT ME IN ADMIN"]
    return render_to_response("index.html",{"states":states, "columns": columns})
