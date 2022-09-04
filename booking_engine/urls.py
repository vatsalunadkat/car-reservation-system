from django.urls import path
from .views import RegisterBookingView, RetrieveBookingView, UpdateBookingView, CancelBookingView

urlpatterns = [
    path('register', RegisterBookingView.as_view()),
    path('current', RetrieveBookingView.as_view()),
    path('update/<int:id>', UpdateBookingView.as_view()),
    path('delete/<int:id>', CancelBookingView.as_view()),
]
