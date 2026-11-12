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

    @swagger_auto_schema(tags=['Usuarios'], responses={200: UserReadSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'], responses={200: UserReadSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'], responses={201: UserReadSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'], responses={200: UserReadSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'], responses={200: UserReadSerializer()})
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuarios'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Datos personales'], operation_summary='Consultar mis datos personales', responses={200: UserReadSerializer()})
    def get(self, request):
        return Response(UserReadSerializer(request.user).data)

from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer
import zeep

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(tags=['Autenticación'], request_body=RegisterUserSerializer, responses={201: 'Usuario registrado exitosamente'})
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SoapCountryView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(tags=['Web Service SOAP'], operation_summary='Consumir servicio SOAP público de países')
    def get(self, request):
        code = request.query_params.get('code', 'MX').upper().strip()
        wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
        try:
            client = zeep.Client(wsdl=wsdl)
            country_info = client.service.FullCountryInfo(code)
            data = {
                'servicio_soap': 'CountryInfoService (WSDL)',
                'codigo_iso': code,
                'pais': country_info.sName,
                'capital': country_info.sCapitalCity,
                'moneda': country_info.sCurrencyISOCode,
                'prefijo_telefonico': country_info.sPhoneCode,
                'continente': country_info.sContinentCode,
                'bandera_url': country_info.sCountryFlag,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Error consumiendo servicio SOAP: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
