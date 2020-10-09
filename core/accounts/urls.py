from django.urls import path

from core.accounts.views import (PasswordResetConfirmationView,
                                 UserActivationView,
                                 UsernameResetConfirmationView)

urlpatterns = [
    path('activate/<str:uid>/<str:token>/',
         UserActivationView.as_view(), name='user-activation'),
    path('password/reset/confirm/<str:uid>/<str:token>/',
         PasswordResetConfirmationView.as_view(), name='password-reset'),
    path('username/reset/confirm/<str:uid>/<str:token>/',
         UsernameResetConfirmationView.as_view(), name='username-reset'),
]
