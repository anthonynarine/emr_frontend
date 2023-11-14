from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        # Check if the email is provided, if not, raise a ValueError
        if not email:
            raise ValueError(_("The Email must be set"))

        # Normalize the email address by lowercasing the domain part of it.
        email = self.normalize_email(email)

        # Create a new user instance with the normalized email and extra fields.
        user = self.model(email=email, **extra_fields)

        # Set the user's password. This handles hashing and other password security measures.
        user.set_password(password)

        # Save the user object to the database.
        user.save()

        # Return the created user instance.
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        # Set default values for superuser. A superuser has all permissions.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Check if the created user is marked as staff and superuser.
        # If not, raise a ValueError as these are required for superusers.
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        # Create and return a superuser using the create_user method.
        return self.create_user(email, password, **extra_fields)
