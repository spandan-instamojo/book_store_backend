from django.urls import path, re_path
from .views import UserRegistrationView, get_username, UserLogin, HintQuestionsView, \
    ResetPasswordView, UserVerification

urlpatterns = [
    path('register',UserRegistrationView.as_view()),
    path('username-check/<str:username>', get_username),
    path(r'login', UserLogin.as_view()),
    path(r'verify', UserVerification.as_view()),
    path(r'reset-password', ResetPasswordView.as_view()),
    path(r'hints', HintQuestionsView.as_view()),
]
