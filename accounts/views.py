from accounts.serializers import UserSerializer, UserRegisterSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import upload_to_s3_task
from .models import User
from rest_framework.viewsets import ModelViewSet
from safari.paginations import SafariPagination

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
                file_data = {
                    'name': file_obj.name,
                    'content_type': file_obj.content_type,
                    'size': file_obj.size,
                    'chunks': list(file_obj.chunks()),
                }
                file_name = f"{user.username}_{file_obj.name}"
                upload_to_s3_task.delay(file_data, file_name, user.id)
            tokens = RefreshToken.for_user(user)
            return Response({'refresh': str(tokens), 'access': str(tokens.access_token)}, status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message': 'Unexpected error while registering you!'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserAllView(ModelViewSet):
    permission_classes = []
    serializer_class = UserSerializer
    pagination_class = SafariPagination

    def get_queryset(self):
        return User.objects.all().order_by('id')
     