from rest_framework import permissions, views
from rest_framework.response import Response

from django_countries import countries


class CountryListView(views.APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(dict(countries))
