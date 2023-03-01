from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from safari.models import Safari
from safari.serializers import SafariCreateSerializer, SafariSearchSerializer
from safari.paginations import SafariPagination
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


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

class SafariSearchView(generics.ListAPIView):
    serializer_class = SafariSearchSerializer

    def get_queryset(self):
        # a static search example looks on tour_data field.
        search_query = self.request.query_params.get('query', '')
        vector = SearchVector('tour_data')
        query = SearchQuery('mid-luxury accommodation')
        return Safari.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1)