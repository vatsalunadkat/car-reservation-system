from django.urls import path
from .views import RegisterView, AuthenticateView, RetrieveView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', AuthenticateView.as_view()),
    path('whoami', RetrieveView.as_view()),
    path('logout', LogoutView.as_view()),
]
