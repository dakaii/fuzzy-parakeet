from core.locations.views import CountryListView
from django.urls import path

urlpatterns = [
    path('countries/', CountryListView.as_view(),
         name='countries'),
]
