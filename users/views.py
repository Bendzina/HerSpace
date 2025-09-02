from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes

logger = logging.getLogger(__name__)
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Registration attempt with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User created successfully: {user.username}")
            return Response(
                {'message': 'User created successfully', 'user_id': user.id},
                status=status.HTTP_201_CREATED
            )
        else:
            logger.error(f"Registration validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ განახლებული user_profile ფუნქცია - GET და PATCH support
@api_view(['GET', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Current user-ის ინფორმაცია და განახლება"""
    try:
        if request.method == 'GET':
            # GET request - user info დაბრუნება
            user_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'displayName': request.user.first_name or request.user.username,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':
            # PATCH request - user profile განახლება
            user = request.user
            
            if 'displayName' in request.data:
                user.first_name = request.data['displayName']
                user.save()
                logger.info(f"User {user.username} updated displayName to: {request.data['displayName']}")
            
            # განახლებული user data დაბრუნება
            updated_user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'displayName': user.first_name or user.username,
            }
            return Response(updated_user_data, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"User profile error: {str(e)}")
        return Response(
            {'error': 'Failed to process user profile request'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ✅ შენი class-based view კარგია, მაგრამ URL-ში არ იყენებ - შეძლებ წაშალო ან დატოვო backup-ისთვის
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile info"""
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'displayName': user.first_name or user.username,
        })
    
    def patch(self, request):
        """Update user profile"""
        user = request.user
        
        if 'displayName' in request.data:
            user.first_name = request.data['displayName']
            user.save()
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'displayName': user.first_name or user.username,
        })