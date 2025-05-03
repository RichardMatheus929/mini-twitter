from twitter.accounts.models import User
from twitter.posts.models import Post

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at']