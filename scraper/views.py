from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import trigger_scraper

class ScraperView(APIView):
    serializer_class = None
    
    def get(self, request):
        trigger_scraper.delay()
        data = {'message': 'Scraping complete!'}
        return Response(data)