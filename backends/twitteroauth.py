"""Twitter Authentication backend for Django

Requires:
AUTH_PROFILE_MODULE to be defined in settings.py

The profile models should have following fields:
        access_token
        url
        location
        description
        profile_image_url
"""

from django.conf import settings
from django.contrib.auth.models import User

from backends import oauthtwitter
from backends import oauth
from backends.oauthtwitter import OAuthApi 
from backends.oauth import  OAuthToken, SimpleOAuthClient
from backends.models import UserProfile

import settings
from backends.twitter import Api
import logging


CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'TuUdr0gUDNLsu2yPJQGmA')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'j03sJquHe28M4mQBmLo747IF7knwwExWVvEjO3Fzs')



class TwitterBackend:
    """TwitterBackend for authentication
    """
    def authenticate(self, request):
        '''authenticates the token by requesting user information from twitter
        '''
        client = SimpleOAuthClient("https://api.twitter.com/",access_token_url="https://api.twitter.com/oauth/access_token")
        consumer = oauth.OAuthConsumer(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        request_token = oauth.OAuthToken.from_string(request.session['request_token'])
        verifier = request.GET["oauth_verifier"]
        signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=request_token, verifier=verifier, http_url="https://api.twitter.com/oauth/access_token")
        oauth_request.sign_request(signature_method_hmac_sha1, consumer, request_token)
    
    
        logging.error("auth in the backend: request_token = %s verifier=%s" % (request_token,verifier))
    
        token = client.fetch_access_token(oauth_request)
        self._cache_token(token, request)
        
        twitter_api = Api(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, token.key, token.secret)
        
        try:
            userinfo = twitter_api.VerifyCredentials()
        except Exception , x:
            logging.error("error in auth: %s" % x)
            # If we cannot get the user information, user cannot be authenticated    
            return None
        
        user, profile = self._user_and_profile_from_twitter(userinfo, token)

        return {"user" : user, "profile" : profile}
    
    def _user_and_profile_from_twitter(self, twitter_user_info, token):
        """
            Returns Django User and UserProfile objects for given twitter user profile
        """
        screen_name = twitter_user_info.screen_name

        user, created = User.objects.get_or_create(username=screen_name)
        if created:
            # create and set a random password so user cannot login using django built-in authentication
            temp_password = User.objects.make_random_password(length=12)
            user.set_password(temp_password)

        user.first_name = twitter_user_info.name
        user.backend = "twitter"
        user.save()

        # Get the user profile
        userprofile = UserProfile.get_or_create(user)
        userprofile.user = user
        userprofile.access_token = token
        userprofile.url = twitter_user_info.url
        userprofile.location = twitter_user_info.location
        userprofile.description = twitter_user_info.description
        userprofile.profile_image_url = twitter_user_info.profile_image_url
        userprofile.save()
    
        return (user, userprofile)
    
    def _cache_token(self, token, request):
        request.session["user_twitter_token"] = token
    
    def _get_cached_token(self, request):
        if request.session.has_key("user_twitter_token"): return request.session["user_twitter_token"]
        else: return None
    
    def find_user(self, twitter_handle, request):
        token = self._get_cached_token(request)
        if token is None: return None
    
        twitter_api = Api(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, token.key, token.secret)
        us = twitter_api.UsersLookup(screen_name=[twitter_handle])
        if us is not None:
            if len(us) != 0: return us[0] 
        return None
    
    def get_user(self, id):
        try: return User.objects.get(username=id)
        except: return None