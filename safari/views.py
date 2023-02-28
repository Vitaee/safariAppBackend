from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from safari.models import Safari
from safari.serializers import SafariCreateSerializer

class CreateSafariView(APIView):
    serializer_class = SafariCreateSerializer

    def post(self, request):
        serializer = SafariCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Success!'} , status=status.HTTP_201_CREATED)

        return Response({'message': "Can't save safari data!"} , status=status.HTTP_400_BAD_REQUEST)

class GetAllSafariView(APIView):
    serializer_class = SafariCreateSerializer

    def get(self, request):
        safari = list(Safari.objects.all().values())
        return JsonResponse({'data': safari}, safe=False, status=status.HTTP_200_OK)
