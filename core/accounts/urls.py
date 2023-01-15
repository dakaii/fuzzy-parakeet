from django.urls import path

from core.accounts.controllers.social_signup import GoogleSignUp
from core.accounts.controllers.users import (AccountOwnerView, UserDetailView,
                                             UserListView)

urlpatterns = [
    path('social/google/', GoogleSignUp.as_view(), name='social-google'),
    path('users/me/', AccountOwnerView.as_view(), name='users-me'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-details'),
]
