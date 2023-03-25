from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "username","password"]

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data["email"])
        user.set_password(validated_data['password'])
        user.save()
        return user