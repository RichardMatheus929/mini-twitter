from django.core.cache import cache
from twitter.posts.models import Post

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    likes_user = serializers.SerializerMethodField(read_only=True)

    def get_likes_user(self, obj):
        cache_key = f'post_likes_user_{obj.id}'
        likes_ids = cache.get(cache_key)

        if likes_ids is None:
            likes_ids = list(obj.likes.all().values_list("user__id", flat=True))
            cache.set(cache_key, likes_ids, timeout=60*5) # Mantendo o cache por 5 minutos

        return likes_ids

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'likes_user', 'image_content']