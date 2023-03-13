from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from safari.models import Safari
from safari.serializers import SafariCreateSerializer, SafariSearchSerializer
from safari.paginations import SafariPagination
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchVector
from psycopg2.extras import NumericRange
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes

class SafariCreateView(APIView):
    serializer_class = SafariCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)

class SafariAllView(ModelViewSet):
    serializer_class = SafariCreateSerializer
    pagination_class = SafariPagination

    def get_object(self):
        return get_object_or_404(Safari)

    def get_queryset(self):
        return Safari.objects.all().order_by('id')

@extend_schema_view(
    get=extend_schema(
        parameters=[
             OpenApiParameter(
                name='price_min',
                description='Enter minimum price default is 400',
                required=False,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name='price_max',
                description='Enter maximum price default is 1500',
                required=False,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(name='query', description='Enter text to made search', type=str)
        ]
    )
)
class SafariSearchView(generics.ListAPIView):
    serializer_class = SafariSearchSerializer
    
    def get_queryset(self):
        search_query = self.request.query_params.get('query', '')
        price_min = int(self.request.query_params.get('price_min', 400))
        price_max = int(self.request.query_params.get('price_max', 1500))
        
        if search_query:
            vector = SearchVector('tour_data', 'inclusions_data', 'getting_there_data', 'day_by_day')
            query = SearchQuery(search_query)
            return Safari.search_by_json_fields(vector=vector, query=query)

        if price_min or price_max:
            Safari.validate_price_range(price_min, price_max)
            price_range = (price_min, 1000)
            max_price_range = (600, price_max)

            return Safari.search_by_price_and_max_price(price_range, max_price_range)

        return Safari.objects.none()