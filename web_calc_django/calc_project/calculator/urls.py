from django.urls import path
from .views import calculator_view, clear_history_view

urlpatterns = [
    path("", calculator_view, name="calculator"),
    path("clear/", clear_history_view, name="clear_history"),
]
