from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserCreateSerializer
import firebase_admin
from firebase_admin import auth

@api_view(['POST'])
def register_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    token = request.data.get('token')
    if token:
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            return Response({'message': 'Login successful!', 'uid': uid}, status=status.HTTP_200_OK)
        except firebase_admin.auth.InvalidIdTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except firebase_admin.auth.ExpiredIdTokenError:
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
