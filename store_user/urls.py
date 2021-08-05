from django.urls import path, re_path
from .views import UserRegistrationView, get_username, UserLogin, ForgotPasswordView, HintQuestionsView

urlpatterns = [
    path('register',UserRegistrationView.as_view()),
    path('username-check/<str:username>',get_username),
    path(r'login', UserLogin.as_view()),
    path(r'forgot-password', ForgotPasswordView.as_view()),
    path(r'hints', HintQuestionsView.as_view()),
]
