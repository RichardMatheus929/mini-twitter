from twitter.accounts.models import User
from twitter.posts.models import Post

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'updated_at']