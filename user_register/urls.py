from django.urls import path
from .views import RegisterView, AuthenticateView, WhoAmIView, RetrieveView, RetrieveAllView, UpdateView, DeleteView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', AuthenticateView.as_view()),
    path('whoami', WhoAmIView.as_view()),
    path('<int:id>', RetrieveView.as_view()),
    path('all', RetrieveAllView.as_view()),
    path('update/<int:id>', UpdateView.as_view()),
    path('delete/<int:id>', DeleteView.as_view()),
    path('logout', LogoutView.as_view()),
]
