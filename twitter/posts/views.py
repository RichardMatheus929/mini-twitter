from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache

from twitter.posts.models import Post
from twitter.posts.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """
        listagem de posts.
        """
        
        queryset = self.get_queryset()

        cache_key = f'follows_data_user_{self.request.user.id}'

        # Retorna apenas post de quem o usuário segue, pega a informação do cache
        # se não tiver no cache, faz a query no banco
        if users_data := cache.get(cache_key):
            queryset = queryset.filter(user__in=users_data['following_users_id'])
        else:
            queryset = queryset.filter(
                likes__user__in=request.user.follower.all().values_list("following__id", flat=True)
            ).distinct()
        
        if self.request.GET.get('order') == "desc":
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at') 

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Definições personalizadas na criação de um post."""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """override no method delete."""
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'Você não tem permissão para deletar este post'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post)
