from django.urls import path
from .views import (
    RegisterView,
    SignInView,
    SignOutView,
    PasswordResetView,
    RegisterView, Success, Tokensend
, VerifyToken)

patterns = [
    path('register/', RegisterView, name='register'),
    path('sign-in/', SignInView, name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('token-send/', Tokensend, name='token_send'),
    path('success/', Success, name='success'),
    path('verify/<auth_token>', VerifyToken, name='verify'),
]


