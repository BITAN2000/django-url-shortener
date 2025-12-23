from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import ShortURL


class ShortURLCreateSerializer(serializers.Serializer):
    long_url = serializers.URLField()
    custom_alias = serializers.CharField(required=False, max_length=8)
    expires_in_seconds = serializers.IntegerField(required=False, min_value=1)

    def validate_custom_alias(self, value):
        if ShortURL.objects.filter(code=value).exists():
            raise serializers.ValidationError("Alias already in use.")
        return value

    def create(self, validated_data):
        expires_at = None
        if "expires_in_seconds" in validated_data:
            expires_at = timezone.now() + timedelta(
                seconds=validated_data["expires_in_seconds"]
            )

        return ShortURL.objects.create(
            original_url=validated_data["long_url"],
            code=validated_data.get("custom_alias"),
            expires_at=expires_at,
        )


class ShortURLStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            "original_url",
            "code",
            "created_at",
            "last_accessed_at",
            "redirect_count",
            "expires_at",
        ]
