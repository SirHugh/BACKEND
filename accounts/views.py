from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializer import UserSerializer
from rest_framework import status
from .models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['nombre'] = user.nombre
        # ...

        return token

@api_view(['GET'])
def getRoutes(request):
    routes = [  
        '/auth/token',
        '/auth/token/refresh',
    ]
    return Response(routes)

@api_view(['POST'])
def login(request):
    
    return Response({})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        response = {'Usuario Creado Exitosamente!'}
        return Response(data=response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def test_token(request):
    name= 'hugo soy yo'
    return Response({name})