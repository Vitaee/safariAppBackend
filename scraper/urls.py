from django.urls import path
from .views import ScraperView

app_name = 'scraper'

urlpatterns = [
    path('run/', ScraperView.as_view(), name='scraper_view'),
]