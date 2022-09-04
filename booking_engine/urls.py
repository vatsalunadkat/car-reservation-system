from django.urls import path
from .views import RegisterBookingView, RetrieveBookingView, UpdateBookingView, CancelBookingView

urlpatterns = [
    path('register', RegisterBookingView.as_view()),
    path('current', RetrieveBookingView.as_view()),
    path('update', UpdateBookingView.as_view()),
    path('cancel', CancelBookingView.as_view()),
]
