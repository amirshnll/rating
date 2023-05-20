from django.urls import path
from .views import RateApi, RateListApi, TotalRatePostApi

urlpatterns = [
    path("", RateApi.as_view()),
    path("list/", RateListApi.as_view()),
    path("total/<str:blog_post_id>/", TotalRatePostApi.as_view()),
]
