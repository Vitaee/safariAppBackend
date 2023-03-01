from rest_framework import serializers

from safari.models import Safari


class SafariCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safari
        fields = '__all__'

class SafariSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safari
        fields = ['tour_data']
