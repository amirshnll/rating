from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.permissions import method_permission_classes, IsAuthor, IsLogginedUser
from .serializers import BlogPostSerializer
from .models import BlogPost as BlogPostModel
from django.core.paginator import Paginator


class BlogPostApi(APIView):
    # add new blog post
    @method_permission_classes([IsLogginedUser, IsAuthor])
    def post(self, request):
        data = request.data.copy()
        data["author"] = request.user.pk
        blog_post_serializer = BlogPostSerializer(data=data)
        if not blog_post_serializer.is_valid():
            return Response(
                blog_post_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        blog_post_serializer.save()
        return Response(blog_post_serializer.data, status=status.HTTP_201_CREATED)

    # get single blog post data
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

    # update single blog post
    @method_permission_classes([IsLogginedUser])
    def put(self, request, blog_post_id):
        try:
            blog_post_obj = BlogPostModel.objects.get(pk=blog_post_id)
        except BlogPostModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "the post could not be found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        blog_post_obj.title = request.data["title"] if "title" in request.data else ""
        blog_post_obj.content = (
            request.data["content"] if "content" in request.data else ""
        )
        blog_post_obj.save()

        blog_post_serializer = BlogPostSerializer(
            instance=blog_post_obj, many=False
        ).data

        return Response(blog_post_serializer, status=status.HTTP_200_OK)

    # delete blog post data
    @method_permission_classes([IsLogginedUser, IsAuthor])
    def delete(self, request, blog_post_id):
        blog_post_obj = BlogPostModel.objects.get(pk=blog_post_id, user=request.user.pk)
        blog_post_obj.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class BlogPostListApi(APIView):
    # get all blog post
    @method_permission_classes([IsLogginedUser])
    def get(self, request):
        blog_post_obj = BlogPostModel.objects.all().order_by("id")

        # pagination
        paginator = Paginator(blog_post_obj, 50)
        blog_post_obj = paginator.page(request.GET.get("page", 1))

        blog_post_serializer = BlogPostSerializer(
            instance=blog_post_obj, many=True
        ).data
        return Response(blog_post_serializer, status=status.HTTP_200_OK)
