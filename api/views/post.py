from api.models import Like, Post
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework import response, serializers, status, viewsets

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username")
        model = User

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for a post model"""
    author = AuthorSerializer(source="author_id")
    like_count = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "author", "author_id", "content", "created_at", "like_count", "updated_at")
        model = Post
        # What is url and depth?

    def get_like_count(self, obj):
        content_type = ContentType.objects.get_for_model(Post)

        return Like.objects.filter(content_type=content_type, object_id=obj.id).count()

class PostViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data

        author_id = data.get("author_id")
        author = User.objects.get(id=author_id)
        content = data.get("content")

        post = Post.objects.create(
                author_id = author,
                content = content,
                created_at = datetime.now(),
                updated_at = datetime.now()
                )

        serializer = PostSerializer(post, many=False)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        page_number = request.GET.get("page")
        posts = Post.objects.all().order_by("created_at").reverse()

        if (page_number == None):
            serializer = PostSerializer(posts, many=True)

            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Once we know how many posts per page we change the 1 to however many we can view per page
        paginator = Paginator(posts, 1, error_messages={"no_results": "Page does not exists."})

        try:
            page = paginator.page(page_number)

            serializer = PostSerializer(page, many=True)

            return response.Response(serializer.data, status=status.HTTP_200_OK)

        except:

            return response.Response(status=status.HTTP_404_NOT_FOUND)
