from django.shortcuts import render
from accounts.serializers import UserSerializer, UserRegisterSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import upload_file_to_s3
from .tasks import upload_to_s3_task

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    permission_classes = []
    serializer_class = UserRegisterSerializer

    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if 'profile_image' in request.FILES:
                file_obj = request.FILES['profile_image']
                file_name = f"{user.username}_{file_obj.name}"
                #upload_to_s3_task.delay(file_obj, file_name, user.id)
                url = upload_file_to_s3(file_obj, file_name)
                if url:
                    user.profile_image = url
                    user.save()
            tokens = RefreshToken.for_user(user)
            return Response({'refresh': str(tokens), 'access': str(tokens.access_token)}, status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message': 'Unexpected error while registering you!'}, status.HTTP_500_INTERNAL_SERVER_ERROR)