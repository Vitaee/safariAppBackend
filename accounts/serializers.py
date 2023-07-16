from rest_framework import serializers

from accounts.models import User, Favorites


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_image')

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "username","password"]
        extra_kwargs = {
            "username": {"required": True},
            "password": {"required": True}
        }

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data["email"])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserFavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'
    