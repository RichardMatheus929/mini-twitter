from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from twitter.follow.models import Follow
from twitter.accounts.serializers import UserSerializer
from twitter.accounts.models import User

# Create your views here.
class FollowViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retorna os seguidores e os seguindos do usuário que faz a request.
        """

        user = request.user

        if self.request.GET.get('users'):

            return Response({
            'user': UserSerializer(user).data,
            'followers': user.follower.all().values_list("id", flat=True),
            'following': user.following.all().values_list("id", flat=True)
        })

        return Response({
            'user': UserSerializer(user).data,
            'followers': user.follower.all().count(),
            'following': user.following.all().count()
        })

    def create(self, request):
        """
        Seguir um usuário.
        """
        
        data = request.data
        user = request.user

        user_to_follow = User.objects.filter(id=data.get('following')).first()

        if Follow.objects.filter(follower=user, following=user_to_follow).exists():
            return Response({'error': 'Você já está seguindo este usuário'}, status=400)

        follow = Follow.objects.create(follower=user, following=user_to_follow)
        return Response({
            'follower': UserSerializer(follow.follower).data,
            'following': UserSerializer(follow.following).data,
            'start_follow': follow.start_follow
        }, status=201)

    def destroy(self, request, pk=None):
        """
        Deixar de seguir um usuário.
        """

        user = request.user

        user_to_unfollow = User.ofollowerbjects.filter(id=pk).first()

        if not user_to_unfollow:
            return Response({'error': 'User not found'}, status=404)
        if not Follow.objects.filter(follower=user, following=user_to_unfollow).exists():
            return Response({'error': 'You do not following this user'}, status=400)
        
        Follow.objects.filter(follower=user, following=user_to_unfollow).delete()
        return Response({'message': 'Unfollow sucess'}, status=204)
