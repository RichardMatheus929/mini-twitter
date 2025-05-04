from rest_framework import serializers
from twitter.likes.models import Like
from twitter.posts.models import Post

from django.core.cache import cache

class LikeCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ['post_id']

    def validate_post_id(self, post_id):
        user = self.context['request'].user

        if cache.get(f'post_likes_user_{post_id}'):
            print("possuia cache sim")
            cache.delete(f'post_likes_user_{post_id}') # Remove a quantidade de likes do cache
        else:
            print("não possuia cache")

        if not Post.objects.filter(id=post_id).exists():
            raise serializers.ValidationError("Post não encontrado.")

        if Like.objects.filter(user=user, post_id=post_id).exists():
            raise serializers.ValidationError("Você já curtiu este post.")

        return post_id

    def create(self, validated_data):
        user = self.context['request'].user
        post_id = validated_data['post_id']
        return Like.objects.create(user=user, post_id=post_id)
    