from django.test import TestCase
from .models import CustomUser
from .serializers import UserRegistrationSerializer

#  cmd to runs test - python manage.py test

class UserRegistrationSerializerTest(TestCase):
    
    def test_successful_user_registration(self):
        # Define a set of valid data to be used for creating a new user.
        # This data should conform to the requirements of your UserRegistrationSerializer.
        valid_data = {
            "username": "testuser",
            "email": "testemail@aol.com",
            "password": "StrongPassword",
            "password2": "StrongPassword"
        }

        # Create an instance of the serializer with the valid data.
        # The data is passed to the serializer, which will then perform validation checks
        # based on the defined rules in the serializer.
        serializer = UserRegistrationSerializer(data=valid_data)

        # Assert that the serializer is valid. 
        # If the serializer is not valid, it means the provided data doesn't meet
        # the validation criteria specified in the serializer.
        self.assertTrue(serializer.is_valid())

        # Save the valid serializer to create a new user instance.
        # This step will invoke the 'create' method of the serializer,
        # resulting in the creation of a new CustomUser object in the database.
        user = serializer.save()

        # Assert that exactly one user is present in the database.
        # This checks if the user has been successfully created and saved in the database.
        self.assertEqual(CustomUser.objects.count(), 1)

        # Assert that the username and email of the created user match the provided data.
        # This ensures that the user data is correctly saved as per the provided input.
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testemail@aol.com")
