from twitter.accounts.models import User
from twitter.posts.models import Post

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    likes_user = serializers.SerializerMethodField()

    def get_likes_user(self, obj):
        return obj.likes.all().values_list("user__id", flat=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'likes_user']