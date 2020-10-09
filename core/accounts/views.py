import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class UserActivationView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, uid, token):
        url = settings.FRONTEND_DOMAIN + f'/user/activation/{uid}/{token}'
        return redirect(url)

        # protocol = 'https://' if request.is_secure() else 'http://'
        # web_url = protocol + request.get_host()
        # post_url = web_url + "/api/users/activation/"
        # post_data = {'uid': uid, 'token': token}
        # result = requests.post(post_url, data=post_data)
        # if result.status_code == 204:
        #     return redirect(settings.FRONTEND_DOMAIN)
        # return redirect('https://google.com')


class PasswordResetConfirmationView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, uid, token):
        url = settings.FRONTEND_DOMAIN + f'/password/reset/{uid}/{token}'
        return redirect(url)


class UsernameResetConfirmationView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, uid, token):
        url = settings.FRONTEND_DOMAIN + f'/username/reset/{uid}/{token}'
        return redirect(url)
