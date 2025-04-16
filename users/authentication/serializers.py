from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    """Adds custom user data to JWT tokens"""
    
    def validate(self, attrs):
        # Get the default token response
        data = super().validate(attrs)
        
        # Add simple user information
        data.update({
            'user_id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name or '',
            'last_name': self.user.last_name or '',
        })
        return data