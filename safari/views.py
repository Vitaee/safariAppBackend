from rest_framework.response import Response
from rest_framework import status, generics, viewsets, views, permissions
from safari.models import Safari, SafariRatings
from safari.serializers import SafariCreateSerializer, SafariSearchSerializer, SafariRatingsSerializer
from safari.paginations import SafariPagination
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from django.utils.decorators import method_decorator
from elasticsearch_dsl import Q, Search, Nested
from elasticsearch_dsl.query import MultiMatch
from .documents import SafariDocument
from elasticsearch.helpers import scan
from accounts.models import User


class SafariCreateView(views.APIView):
    serializer_class = SafariCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)


class SafariAllView(generics.ListAPIView):
    serializer_class = SafariCreateSerializer
    pagination_class = SafariPagination

    @method_decorator(cache_page(60 * 15, key_prefix='safari')) # cache for 15 minutes
    def list(self, request, *args, **kwargs):
        results = SafariDocument.search().extra(size=100)
        safari_ids = [r['id'] for r in results]
        

        queryset = Safari.objects.filter(id__in=safari_ids).order_by('id')
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
        price_min = int(self.request.query_params.get('price_min', 0))
        price_max = int(self.request.query_params.get('price_max', 0))

        bool_query = Q()

        if search_query:
            nested_query = Q('nested', path='tour_data.*', query=Q('wildcard', **{'tour_data.*': f'*{search_query}*'}))
            bool_query |= nested_query

            nested_query = Q('nested', path='inclusions_data.inclusions.*', query=Q('wildcard', **{'inclusions_data.inclusions.*': f'*{search_query}*'}))
            bool_query |= nested_query

            nested_query = Q('nested', path='getting_there_data', query=Q('wildcard', **{'getting_there_data': f'*{search_query}*'}))
            bool_query |= nested_query

            nested_query = Q('nested', path='day_by_day.*', query=Q('wildcard', **{'day_by_day.*': f'*{search_query}*'}))
            bool_query |= nested_query

            nested_query = Q('nested', path='name',  query=Q('wildcard', **{'name' : f'*{search_query}*' }))
            bool_query |= nested_query

        if price_min > 0 or price_max > 0:
            Safari.validate_price_range(price_min, price_max)
            price_range = {'gte': price_min, 'lte': 1000}
            max_price_range = {'gte': 600, 'lte': price_max}
            price_query = Q('range', price=price_range) | Q('range', max_price=max_price_range)
            bool_query = bool_query & price_query

        result = SafariDocument.search().query(bool_query).execute()
        # meta.highlight.to_dict()
        safari_ids = [hit.meta.id for hit in result]

        return Safari.objects.filter(id__in=safari_ids)
    

class SafariRatingView(viewsets.ModelViewSet):
    serializer_class = SafariRatingsSerializer
    queryset = Safari.objects.all()
    permission_classes = [ permissions.AllowAny ]

    def create(self, request, *args, **kwargs):
        user = request.data['user']
        request.data['user'] = User.objects.get(id=user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)