from rest_framework import serializers
from .models import FeatureDetection

class FeatureDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureDetection
        fields = '__all__'