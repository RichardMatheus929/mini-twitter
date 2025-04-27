from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from twitter.posts.models import Post
from twitter.posts.serializers import PostSerializer

class PostView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        content = request.data.get('content')
        user = request.user

        if not content or content == "":
            return Response({'error': 'O conteúdo não deve ser nulo'}, status=400)

        post = Post.objects.create(user=user, content=content)
        serializer = PostSerializer(post)

        return Response(serializer.data, status=201)