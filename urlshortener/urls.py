from django.urls import path
from .views import ShortenURLView, RedirectURLView, URLStatsView

urlpatterns = [
    path("shorten", ShortenURLView.as_view()),
    path("stats/<str:code>", URLStatsView.as_view()),
    path("<str:code>", RedirectURLView.as_view()),
]
