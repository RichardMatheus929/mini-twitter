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

    def perform_create(self, serializer):
        """Definições personalizadas na criação de um post."""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """override no method delete."""
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'Você não tem permissão para deletar este post'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post)
