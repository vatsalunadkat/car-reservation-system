from django.urls import path
from .views import RegisterVehicleView, UpdateVehicleView, RetrieveVehicleView, DeleteVehicleView

urlpatterns = [
    path('register', RegisterVehicleView.as_view()),
    path('<int:id>', RetrieveVehicleView.as_view()),
    path('update/<int:id>', UpdateVehicleView.as_view()),
    path('delete/<int:id>', DeleteVehicleView.as_view()),
]
