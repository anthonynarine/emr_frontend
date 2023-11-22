from rest_framework import serializers
from .models import CustomUser, PatientProfile
from django.core.validators import EmailValidator
from phonenumber_field.serializerfields import PhoneNumberField
import re

# Serializer for the User model registration will handle auth related request

class UserRegistrationSerializer(serializers.ModelSerializer):
    # This field is used for confirming password, it won't be stored in the database
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2",]
        # Ensures password is never read back in a response
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Use EmailValidator to validate the email field
    email = serializers.EmailField(
        validators=[EmailValidator(message="Invalid email format."),]
    )

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        """
        Check the validity of the password field.
        """
        # Check if password is too short
        if len(value) < 8:
            raise serializers.ValidationError("The password is too short.")

        # ADDITIONAL VALIDATIONS TO CONSIDER W/ REGULAR EXPRESSION
        # if not re.search("[a-zA-Z]", value):
        #     raise serializers.ValidationError("Password must include letters.")

        # if not re.search("[0-9]", value):
        #     raise serializers.ValidationError("Password must include numbers.")

        # if not re.search("[!@#$%^&*()_+]", value):
        #     raise serializers.ValidationError("Password must include special characters.")

        return value

    def validate(self, data):
        """
        Ensure that the passwords provided match.
        """
        password = data.get("password")
        password2 = data.pop("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user instance using the validated data.
        """
        user = CustomUser.objects.create_user(**validated_data)
        return user

# Serializer for the User profile will handle bio related data

class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()