from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse


def index(request):
	return HttpResponse("Green tomatoe")
