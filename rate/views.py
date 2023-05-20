from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from user.permissions import method_permission_classes, IsLogginedUser
from .serializers import RatingSerializer
from .models import Rating as RatingModel
from blog.models import BlogPost as BlogPostModel


class RateApi(APIView):
    # add rate to blog post
    @method_permission_classes([IsLogginedUser])
    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.pk

        if RatingModel.objects.filter(post=data["post"], user=data["user"]).exists():
            return Response(
                {
                    "status": "error",
                    "message": "you have already rated this in the past. duplicate ratings are not allowed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rate_serializer = RatingSerializer(data=data)
        if not rate_serializer.is_valid():
            return Response(rate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        rate_serializer.save()
        return Response(rate_serializer.data, status=status.HTTP_201_CREATED)


class RateListApi(APIView):
    # get all rates
    @method_permission_classes([IsLogginedUser])
    def get(self, request):
        rate_obj = RatingModel.objects.all().order_by("id")

        # pagination
        paginator = Paginator(rate_obj, 50)
        rate_obj = paginator.page(request.GET.get("page", 1))

        rate_serializer = RatingSerializer(instance=rate_obj, many=True).data
        return Response(rate_serializer, status=status.HTTP_200_OK)


class TotalRatePostApi(APIView):
    # get blog post rate average
    def get(self, request, blog_post_id):
        if not BlogPostModel.objects.filter(pk=blog_post_id).exists():
            return Response(
                {"status": "error", "message": "the post could not be found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        rate_obj = RatingModel.objects.filter(post=blog_post_id).order_by("id")
        rate_serializer = RatingSerializer(instance=rate_obj, many=True).data
        total_rate = sum(rate["value"] for rate in rate_serializer)
        if total_rate > 0:
            total_rate = int(total_rate / len(rate_serializer))
        return Response(total_rate, status=status.HTTP_200_OK)
