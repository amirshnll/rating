from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.permissions import method_permission_classes, IsAuthor, IsLogginedUser
from .serializers import BlogPostSerializer
from .models import BlogPost as BlogPostModel


class StaticPageApi(APIView):
    @method_permission_classes([IsLogginedUser, IsAuthor])
    def post(self, request):
        blog_post_serializer = BlogPostSerializer(data=request.data)
        if not blog_post_serializer.is_valid():
            return Response(
                blog_post_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        blog_post_serializer.save()
        return Response(blog_post_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, blog_post_id):
        try:
            blog_post_obj = BlogPostModel.objects.get(pk=blog_post_id)
            blog_post_serializer = BlogPostModel(
                instance=blog_post_obj, many=False
            ).data
            return Response(blog_post_serializer, status=status.HTTP_200_OK)
        except BlogPostModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "the post could not be found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @method_permission_classes([IsLogginedUser])
    def put(self, request, blog_post_id):
        blog_post_obj = BlogPostModel.objects.get(pk=blog_post_id)

        blog_post_obj.title = request.data["title"] if "title" in request.data else ""
        blog_post_obj.content = (
            request.data["content"] if "content" in request.data else ""
        )
        blog_post_obj.save()

        blog_post_serializer = BlogPostSerializer(
            instance=blog_post_obj, many=False
        ).data

        return Response(blog_post_serializer, status=status.HTTP_200_OK)

    @method_permission_classes([IsLogginedUser, IsAuthor])
    def delete(self, request, blog_post_id):
        blog_post_obj = BlogPostModel.objects.get(pk=blog_post_id)
        blog_post_obj.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class BlogPostListApi(APIView):
    @method_permission_classes([IsLogginedUser])
    def get(self, request):
        blog_post_obj = BlogPostModel.objects.all().order_by("id")
        blog_post_serializer = BlogPostSerializer(
            instance=blog_post_obj, many=True
        ).data
        return Response(blog_post_serializer, status=status.HTTP_200_OK)
