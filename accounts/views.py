from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializer import UserSerializer
from rest_framework import status
from .models import User

import qrcode
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

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



class QRCodeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # token = request.auth.access
        # serializer = MyTokenObtainPairSerializer(data={'username': request.user.username, 'password': 'password'})
        # serializer.is_valid(raise_exception=True)
        # token = serializer.validated_data['access']
        token = AccessToken.for_user(request.user) 
        url = 'http://localhost:5174/Inscripci%C3%B3n/?auth='  + str(token) 
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type='image/png')
        img.save(response, 'PNG')

        return  response