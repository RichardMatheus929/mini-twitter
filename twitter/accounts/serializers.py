from rest_framework import serializers
from twitter.accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = (
            'id',
            'name',
            'username',
            'email'
        )