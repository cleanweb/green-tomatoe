'''
Created on Apr 25, 2011

@author: philip
'''

from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from backends.models import UserProfile

def get_fake_user():
    user, created = User.objects.get_or_create(username="philip_fake")
        
    if created:
        user.first_name = "Philip"
        user.backend = "fake"
        user.save()

    return user

def get_fake_user_profile():
    user = get_fake_user()
    userprofile = UserProfile.get_or_create(user)
    userprofile.user = user
    userprofile.access_token = "qdsfqsdfqsdfqsdf"
    userprofile.url = "http://twitter.com/callmephilip"
    userprofile.location = "San Francisco"
    userprofile.description = "fake user locahost testing purposes only"
    userprofile.profile_image_url = "http://a3.twimg.com/profile_images/1366764862/6d4f6ed7afeb4712bf721073425eb837_7_normal.jpg"
    userprofile.save()
    return userprofile  

def get_user(request):
    if request.META['SERVER_NAME'] == "localhost":
        return get_fake_user()
    else:
        if request.session.has_key("rmp_user"):
            return request.session["rmp_user"]
        else: return None

def get_user_profile(request):
    if request.META['SERVER_NAME'] == "localhost":
        return get_fake_user_profile()
    else:
        if request.session.has_key("rmp_user_profile"):
            return request.session["rmp_user_profile"]
        else: return None
    
def login(request,user,profile):
    django_login(request, user)
    request.session["rmp_user"] = user
    request.session["rmp_user_profile"] = profile
    
def clean_session(request):
    if request.session.has_key("rmp_user"): del request.session["rmp_user"]
    if request.session.has_key("rmp_user_profile"): del request.session["rmp_user_profile"]
    