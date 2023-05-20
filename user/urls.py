from django.urls import path
from .views import UserApi, UserAuthorApi, UserTypeList, UserAuthApi

urlpatterns = [
    path("", UserApi.as_view()),
    path("author/", UserAuthorApi.as_view()),
    path("type/list/", UserTypeList.as_view()),
    path("auth/", UserAuthApi.as_view()),
]
