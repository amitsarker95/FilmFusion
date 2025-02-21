from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
#MODELS & SERIALIZERS
from .serializers import RegistrationSerializer




class RegestrationView(APIView):
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                    'email' : str(user.email),
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                 }
            return Response(data, status=status.HTTP_200_OK)
    

class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "You have successfully logout from your account"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e) }, status=status.HTTP_400_BAD_REQUEST)