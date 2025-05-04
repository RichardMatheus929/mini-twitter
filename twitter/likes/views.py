from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twitter.likes.serializers import LikeCreateSerializer
from twitter.likes.models import Like

from django.core.cache import cache

# Create your views here.
class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Curtir um post
        """
        serializer = LikeCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        like = serializer.save()

        cache.delete(f'post_likes_user_{like.post.id}') # Remove a quantidade de likes do cache

        return Response({
            'user': like.user.username,
            'post_id': like.post.id,
            'liked_at': like.liked_at
        }, status.HTTP_201_CREATED)


    
    def destroy(self, request, pk=None):
        """
        Descurtir um post
        """

        cache_key = f'post_likes_user_{pk}'
        cache.delete(cache_key)

        user = request.user

        like_queryset = Like.objects.filter(user=user, post_id=pk)

        if not like_queryset.exists():
            return Response({'error': 'Você não curtiu este post ou o post não existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        like_queryset.delete()

        return Response({'message': 'Descurtido com sucesso'}, status=status.HTTP_204_NO_CONTENT)
