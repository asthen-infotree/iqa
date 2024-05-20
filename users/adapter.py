from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse
from django.http import Http404


class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email_domain = sociallogin.user.email.split('@')[1].lower()
        if not email_domain in ["infotree.net.my", "ikram.com.my"]:
            raise ImmediateHttpResponse(HttpResponse(sociallogin.user.email + ' is not valid memeber of ikram.com.my'))
        else:
            pass
