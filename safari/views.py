from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from safari.models import Safari
from safari.serializers import SafariCreateSerializer, SafariSearchSerializer
from safari.paginations import SafariPagination
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from django.utils.decorators import method_decorator
from elasticsearch_dsl import Q, Search, Nested
from elasticsearch_dsl.query import MultiMatch


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

    @method_decorator(cache_page(60 * 15, key_prefix='safari')) # cache for 15 minutes
    def list(self, request, *args, **kwargs):
        queryset = Safari.objects.all().order_by('-id')
        page = self.paginate_queryset(queryset)
        serializer = SafariCreateSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    
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

        s = Search(index='safari')
        bool_query = Q()

        if search_query:
            multi_match_query = Q('multi_match', query=search_query, fields=['name', 'location', 'description'])
            bool_query &= multi_match_query

        if price_min or price_max:
            Safari.validate_price_range(price_min, price_max)
            price_range = {'gte': price_min, 'lte': 1000}
            max_price_range = {'gte': 600, 'lte': price_max}
            price_query = Q('range', price=price_range) | Q('range', max_price=max_price_range)
            bool_query = bool_query & price_query

        s = s.query(bool_query)
        response = s.execute()
        safari_ids = [hit.meta.id for hit in response]
        return Safari.objects.filter(id__in=safari_ids)