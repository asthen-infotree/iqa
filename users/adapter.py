from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse
from django.http import Http404


class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.account.user
        print(not u.email.split('@')[1] == "ikram.com.my")
        if not u.email.split('@')[1] in ["infotree.net.my", "ikram.com.my"]:
            raise Http404
