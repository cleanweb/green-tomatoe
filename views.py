from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from datafeed.models import State



def index(request):
	states = State.objects.all().order_by('name')
	return render_to_response("index.html",{"states":states})
