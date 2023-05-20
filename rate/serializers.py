from rest_framework import serializers
from .models import Rating as RatingModel


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingModel
        fields = ["id", "post", "user", "value"]
