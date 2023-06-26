from accounts.serializers import UserSerializer, UserRegisterSerializer
from rest_framework import status, generics, viewsets, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import upload_to_s3_task
from .models import User
from safari.paginations import SafariPagination


class UserView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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

        headers = self.get_success_headers(serializer.data)
        tokens = RefreshToken.for_user(user)
        return Response({'refresh': str(tokens), 'access': str(tokens.access_token)}, status.HTTP_201_CREATED, headers=headers)


class UserAllView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]