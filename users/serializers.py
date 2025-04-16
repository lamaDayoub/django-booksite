from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer
)
from django.contrib.auth.password_validation import validate_password
User = get_user_model()

class CreateUserSerializer(BaseUserCreateSerializer):
    bio = serializers.CharField(required=False, write_only=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'bio')

class Phase1SignUpSerializer(CreateUserSerializer):
    class Meta(CreateUserSerializer.Meta):
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Ensure user is inactive until activation
        )
        return user

class ProfileCompletionSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('first_name', 'last_name', 'bio')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'bio': {'required': False}
        }


    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user)
        
        # Check against current password
        if user.check_password(value):
            raise serializers.ValidationError("New password cannot be the same as current password")
            
        # Check against last 6 passwords
        
        last_passwords = user.password_history.order_by('-created_at')[:6]
        for old_record in last_passwords:
            if check_password(value, old_record.hashed_password):
                raise serializers.ValidationError("You cannot reuse any of your last 6 passwords")
                
        return value