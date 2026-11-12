from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserSerializer, UserReadSerializer

class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    @swagger_auto_schema(responses={200: UserReadSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: UserReadSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(responses={201: UserReadSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: UserReadSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: UserReadSerializer()})
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='Consultar mis datos personales', responses={200: UserReadSerializer()})
    def get(self, request):
        return Response(UserReadSerializer(request.user).data)
