from rest_framework import serializers
from twitter.likes.models import Like
from twitter.posts.models import Post

class LikeCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ['post_id']

    def validate_post_id(self, value):
        user = self.context['request'].user

        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError("Post não encontrado.")

        if Like.objects.filter(user=user, post_id=value).exists():
            raise serializers.ValidationError("Você já curtiu este post.")

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        post_id = validated_data['post_id']
        return Like.objects.create(user=user, post_id=post_id)
    