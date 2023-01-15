import os
from django.contrib.auth import get_user_model
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from core.accounts.serializers.account_owners import GoogleSignUpSerializer

AccountOwner = get_user_model()

GOOGLE_WEB_ID = os.environ.get("GOOGLE_WEB_ID", default='secret')


class GoogleSignUp(generics.CreateAPIView):

    serializer_class = GoogleSignUpSerializer
    permission_classes = (permissions.AllowAny, )

    def _google_auth(self, auth_info):
        token = auth_info['id_token']
        idinfo = id_token.verify_oauth2_token(token, Request(), GOOGLE_WEB_ID)
        if idinfo['aud'] not in [GOOGLE_WEB_ID]:
            raise ValueError('Could not verify audience.')
        return idinfo['email']

    def create(self, request, *args, **kwargs):
        # login_type = request.data.get('idp_id')
        # if login_type == 'google':
        email = self._google_auth(request.data)
        try:
            user = AccountOwner.objects.get(email=email)
        except AccountOwner.DoesNotExist:
            serializer = self.serializer_class(data={
                'email': email,
                # 'password': uuid.uuid4().hex
            })
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        }, status=status.HTTP_200_OK)