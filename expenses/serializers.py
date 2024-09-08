from rest_framework import serializers
from django.contrib.auth import get_user_model

from authsystem.models import CustomUser
from .models import Expense

# Serializer for user registration
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

# Serializer for list and create expense
class ExpenseListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']  # Exclude user from the input fields

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user
        return super().create(validated_data)

# Serializer for retrieve, update, and delete expense
class ExpenseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']  # Do not include the user field here

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user
        return super().create(validated_data)
