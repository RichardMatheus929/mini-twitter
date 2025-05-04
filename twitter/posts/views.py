from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

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

    def perform_create(self, serializer):
        """Definições personalizadas na criação de um post."""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """override no method delete."""
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'Você não tem permissão para deletar este post'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post)
