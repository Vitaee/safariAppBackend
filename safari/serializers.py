from rest_framework import serializers

from safari.models import Safari, SafariRatings


class SafariCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safari
        fields = '__all__'

class SafariSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safari
        fields = '__all__'


class SafariRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafariRatings
        fields = '__all__'
        extra_kwargs = {
            "user": {"required": True},
        }

    