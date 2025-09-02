from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def validate_password(self, value):
        """Password validation"""
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate_username(self, value):
        """Username validation"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        """Email validation"""
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data.get('email', '')
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")