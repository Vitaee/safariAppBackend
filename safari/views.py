from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from safari.models import Safari
from safari.serializers import SafariCreateSerializer
from safari.paginations import SafariPagination
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

class CreateSafariView(APIView):
    serializer_class = SafariCreateSerializer

    def post(self, request):
        serializer = None
        data = request.data
        
        if isinstance(data, list) and len(data) > 1:
            serializer = SafariCreateSerializer(data=data, many=True)
        else:
            serializer = SafariCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Success!'} , status=status.HTTP_201_CREATED)

        return Response({'message': "Can't save safari data!"} , status=status.HTTP_400_BAD_REQUEST)

class GetAllSafariView(ModelViewSet):
    serializer_class = SafariCreateSerializer
    pagination_class = SafariPagination

    def get_object(self):
        return get_object_or_404(Safari)

    def get_queryset(self):
        return Safari.objects.all().order_by('id')
