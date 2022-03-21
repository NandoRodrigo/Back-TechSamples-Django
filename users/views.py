from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsUserCreationOrList, IsUserUpdatePassword

from .models import User
from .serializers import UserSerializer, LoginSerializer


class UsersView(ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsUserCreationOrList]


class UpdatePasswordView(RetrieveUpdateAPIView):
  
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_url_kwarg = "user_id"

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsUserUpdatePassword]

class LoginView(APIView):
  def post(self, request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        self, email=request.data['email'], password=request.data['password'])

    if user is not None:

      token = Token.objects.get_or_create(user=user)[0]

      return Response({'token': token.key}, status=status.HTTP_200_OK)

    else:
      return Response({"error": [
          "Invalid email or password"
      ]}, status=status.HTTP_401_UNAUTHORIZED)

