from rest_framework import serializers
from twitter.likes.models import Like
from twitter.posts.models import Post
from twitter.follow.models import Follow

from django.core.cache import cache

class LikeCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ['post_id']

    def validate_post_id(self, post_id):
        user = self.context['request'].user

        post = Post.objects.filter(id=post_id)

        if not post.exists():
            raise serializers.ValidationError("Post não encontrado.")
        
        if not Follow.objects.filter(follower=user, following=post.first().user).exists():
            raise serializers.ValidationError("Você não pode curtir este post, pois não segue o usuário.")  

        if Like.objects.filter(user=user, post_id=post_id).exists():
            raise serializers.ValidationError("Você já curtiu este post.")

        return post_id

    def create(self, validated_data):
        user = self.context['request'].user
        post_id = validated_data['post_id']
        return Like.objects.create(user=user, post_id=post_id)
    