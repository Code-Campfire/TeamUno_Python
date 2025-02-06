from api.models import Like, Post
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
    def list(self, request):
        posts = Post.objects.all().reverse()

        # paginator = Paginator(posts, 25)

        serializer = PostSerializer(posts, many=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)



# A backend route /api/posts is implemented to fetch posts from the database 
# in reverse chronological order.

# Pagination is supported to fetch posts in batches.

# The frontend displays posts retrieved from the API, including the post content,
# author, timestamp, and like count.
