from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# Custom manager for the User model
class UserManager(BaseUserManager):

    # Method to create a regular user
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_("Email cannot be empty"))  # Ensure email is provided
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields)  # Create a new user instance
        user.set_password(password)  
        user.save()  # Save the user to the database
        return user

    # Method to create a superuser
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)  # Superuser must have staff privileges
        extra_fields.setdefault("is_superuser", True)  # Superuser must have superuser privileges
        extra_fields.setdefault("is_active", True)  # Superuser must be active
        # extra_fields.setdefault("is_verified", True)  # Optionally mark the superuser as verified

        # Ensure that the required fields are correctly set for the superuser
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        # Call the create_user method to create the superuser
        return self.create_user(email, password, **extra_fields)


# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the unique identifier instead of a username.
    This model supports permission handling by extending PermissionsMixin.
    """
    first_name = models.CharField(max_length=255)  # User's first name
    last_name = models.CharField(max_length=255)  # User's last name
    photo = models.ImageField()  # User profile photo
    dob = models.DateField()  # Date of birth
    phone_number = models.CharField(max_length=20)  # Phone number (can store international numbers)
    email = models.EmailField(max_length=255, unique=True)  # Email is the unique identifier for the user
    is_superuser = models.BooleanField(default=False)  # Indicates if the user is a superuser
    is_staff = models.BooleanField(default=False)  # Determines if the user has staff privileges
    is_active = models.BooleanField(default=False)  # Active status for the user
    # is_verified = models.BooleanField(default=False)  # Whether the user's email has been verified
    reset_password_token = models.CharField(max_length=255)  # Token for password reset
    reset_password_token_expiry = models.DateTimeField()  # Expiry timestamp for the password reset token
    is_deleted = models.BooleanField(default=False)  # Soft delete flag to mark a user as deleted without removing data

    # Timestamps to track when the user was created and last updated
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the user is created
    updated_date = models.DateTimeField(auto_now=True)  # Automatically update the timestamp on each update

    # Set email as the field used for login instead of a username
    USERNAME_FIELD = "email"

    # Fields that should be required when creating a user
    # REQUIRED_FIELDS can be left empty if no other fields are mandatory besides the email and password
    REQUIRED_FIELDS = []  # Example: Add 'first_name', 'last_name' here if you want to enforce them as required fields.

    # Custom manager for the User model
    objects = UserManager()

    # String representation of the User model (used in the admin panel and for debugging)
    def __str__(self):
        return self.email  # Return the email as the string representation of the user
