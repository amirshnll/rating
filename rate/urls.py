from django.urls import path
from .views import RateApi

urlpatterns = [
    path("", RateApi.as_view()),
]
