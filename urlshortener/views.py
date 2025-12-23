from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURL
from .serializers import (
    ShortURLCreateSerializer,
    ShortURLStatsSerializer,
)


class ShortenURLView(APIView):
    def post(self, request):
        serializer = ShortURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = serializer.save()

        return Response(
            {
                "short_code": short_url.code,
                "short_url": request.build_absolute_uri(f"/{short_url.code}")
            },
            status=status.HTTP_201_CREATED,
        )


class RedirectURLView(APIView):
    def get(self, request, code):
        url = get_object_or_404(ShortURL, code=code)

        if url.is_expired():
            return Response(
                {"detail": "URL has expired"},
                status=status.HTTP_410_GONE,
            )

        url.redirect_count += 1
        url.last_accessed_at = timezone.now()
        url.save(update_fields=["redirect_count", "last_accessed_at"])

        return redirect(url.original_url)


class URLStatsView(APIView):
    def get(self, request, code):
        url = get_object_or_404(ShortURL, code=code)
        serializer = ShortURLStatsSerializer(url)
        return Response(serializer.data)
