from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    profile_image_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)
    
    
    @staticmethod
    def from_twitter(userinfo):
        screen_name = userinfo.screen_name

        user, created = User.objects.get_or_create(username=screen_name)
        if created:
            # create and set a random password so user cannot login using django built-in authentication
            temp_password = User.objects.make_random_password(length=12)
            user.set_password(temp_password)

        user.first_name = userinfo.name
        user.backend = "twitter"
        user.save()

        # Get the user profile
        userprofile = UserProfile.get_or_create(user)
        userprofile.user = user
        userprofile.access_token = "token"
        userprofile.url = userinfo.url
        userprofile.location = userinfo.location
        userprofile.description = userinfo.description
        userprofile.profile_image_url = userinfo.profile_image_url
        userprofile.save()
    
        return userprofile
    
    @staticmethod
    def get_user_profile_from_user_name(username):
        try:
            u = User.objects.get(username = username)
            return UserProfile.objects.get(user = u)    
        except:
            return None
    
    @staticmethod
    def get_user_profile_from_user_id(id):
        try:
            return UserProfile.objects.get(user = User.objects.get(id=id))
        except:
            return None
    
    @staticmethod
    def get_or_create(user):
        try:
            return UserProfile.objects.get(user=user)
        except:
            return UserProfile()
    
    def __str__(self):
        return "%s's profile" % self.user