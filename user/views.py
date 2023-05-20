from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser as CustomUserModel, UserTypes as UserTypesModel
from .serializers import (
    CustomUserSerializers,
    RegisterNewUserSerializer,
    RegisterNewUserAuthorSerializer,
    AuthValidationSerializer,
)
from .permissions import method_permission_classes, IsLogginedUser
from .defs import make_auth_obj


class UserApi(APIView):
    # get user
    @method_permission_classes([IsLogginedUser])
    def get(self, request):
        try:
            user_obj = CustomUserModel.objects.get(pk=request.user.id)
        except CustomUserModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "user does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_serializer = CustomUserSerializers(instance=user_obj, many=False)
        return Response(balance_serializer.data, status=status.HTTP_200_OK)

    # create new user
    def post(self, request):
        serializer = RegisterNewUserSerializer(data=request.data)
        if not serializer.is_valid():
            return (
                Response(serializer.errors, status=status.HTTP_409_CONFLICT)
                if serializer.errors.get("username")
                else Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserAuthorApi(APIView):
    # create new author
    def post(self, request):
        serializer = RegisterNewUserAuthorSerializer(data=request.data)
        if not serializer.is_valid():
            return (
                Response(serializer.errors, status=status.HTTP_409_CONFLICT)
                if serializer.errors.get("username")
                else Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserTypeList(APIView):
    # user type list
    def get(self, request):
        response = [i[0] for i in UserTypesModel.choices]
        return Response(response, status=status.HTTP_200_OK)


class UserAuthApi(APIView):
    # auth user
    def post(self, request):
        balance_serializer = AuthValidationSerializer(data=request.data)

        if not balance_serializer.is_valid():
            return Response(
                balance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = balance_serializer.validated_data["username"]
        password = balance_serializer.validated_data["password"]
        try:
            user_obj = CustomUserModel.objects.get(username=username, is_deleted=False)
        except CustomUserModel.DoesNotExist:
            return Response(
                {
                    "detail": "error",
                    "message": "invalid username or password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_obj.check_password(password):
            auth_obj = make_auth_obj(user_obj)
            return Response(auth_obj, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "detail": "error",
                    "message": "invalid username/email or password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
