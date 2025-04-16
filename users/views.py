from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import Phase1SignUpSerializer,ProfileCompletionSerializer,ChangePasswordSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from .models import UserPasswordHistory
from rest_framework import status
from drf_yasg import openapi
from djoser.conf import settings
from django.contrib.auth import get_user_model 
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .authentication.serializers import CustomTokenSerializer

# Create your views here.
User = get_user_model()
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
class SignUp(CreateAPIView):
    serializer_class = Phase1SignUpSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Create inactive user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)  # Force inactive
        
        # Send activation email to console
        context = {"user": user}
        to = [user.email]
        settings.EMAIL.activation(request, context).send(to)
        
        return Response({
            'email': user.email,
            'detail': 'Check console for activation email'
        }, status=status.HTTP_201_CREATED)
        
    @swagger_auto_schema(
        operation_description="Phase 1: Register with just email and password",
        request_body=Phase1SignUpSerializer,  # Directly reference the serializer
        responses={
            201: openapi.Response(
                description="Account created. Session started.",
                schema=Phase1SignUpSerializer
            ),
            400: openapi.Response(
                description="Invalid input",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                        'password': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    



class ProfileCompletionView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileCompletionSerializer
    http_method_names = ['get', 'patch']
    
    @swagger_auto_schema(
        operation_id="retrieve_profile",
        tags=['User Profile'],  # ← Must add tags
        operation_description="Retrieve current authenticated user's profile data",
        responses={
            200: ProfileCompletionSerializer,
            401: openapi.Response("Unauthorized")
        },
        security=[{"Bearer": []}]  # ← Explicit security declaration
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_id="update_profile",
        tags=['User Profile'],  # ← Same tag groups related endpoints
        operation_description="Update user profile (partial updates allowed)",
        request_body=ProfileCompletionSerializer,
        responses={
            200: ProfileCompletionSerializer,
            400: openapi.Response("Bad Request"),
            401: openapi.Response("Unauthorized")
        },
        security=[{"Bearer": []}]  # ← Required for authenticated endpoints
    )
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().patch(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user



class LoginView(TokenObtainPairView):
    authentication_classes=[JWTAuthentication]
    serializer_class = CustomTokenSerializer
    @swagger_auto_schema(
        operation_id="user_login",
        operation_description="Authenticate user and obtain JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='email',
                    description="User's registered email address",
                    example="user@example.com"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='password',
                    description="User's password",
                    example="securepassword123"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful authentication",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Access token for API authorization (valid 15 minutes)"
                        ),
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Refresh token for obtaining new access tokens (valid 7 days)"
                        ),
                        'user_id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Authenticated user's ID"
                        ),
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format='email',
                            description="User's email address"
                        ),
                        'first_name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's first name"
                        ),
                        'last_name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's last name"
                        ),
                        'is_active': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="Whether account is active"
                        ),
                    }
                ),
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "user_id": 42,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="Email validation errors"
                        ),
                        'password': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="Password validation errors"
                        )
                    }
                )
            ),
            401: openapi.Response(
                description="Invalid credentials",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="No active account found with the given credentials"
                        )
                    }
                )
            )
        },
        security=[],
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    


@swagger_auto_schema(
    method='post',
    operation_description="End current user session",
    responses={
        200: openapi.Response('Logout successful', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )),
        401: 'Unauthorized'
    }
)

@api_view(['POST'])    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail": "Successfully logged out."})

class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication] 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        new_password = serializer.validated_data['new_password']
        
        # Store current password in history before changing it
        UserPasswordHistory.objects.create(
            user=user,
            hashed_password=user.password  # Already hashed
        )
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Keep only last 6 passwords
        histories = user.password_history.order_by('-created_at')
        if histories.count() > 6:
            for history in histories[6:]:
                history.delete()
        
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)