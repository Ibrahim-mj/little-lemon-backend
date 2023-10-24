from cloudinary.models import CloudinaryField
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    A custom user manager to handle user creation and superuser creation.
    """

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to be saved for the user.

        Raises:
            ValueError: If email or password is not provided.

        Returns:
            User: The newly created user object.
        """
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValueError("Password required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        group = Group.objects.get(name="Customers")
        user = self._create_user(email, password, **extra_fields)
        user.groups.set([group])
        user.user_permissions.set(
            Permission.objects.filter(group__in=user.groups.all())
        )
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """
    A custom user model that extends the built-in Django User model.
    """

    username = None
    email = models.EmailField(_("email address"), max_length=225, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_pic = CloudinaryField(_("Profile picture"), blank=True, null=True)
    phone = models.CharField(_("phone number"), max_length=20, null=True, blank=True)
    # refresh_token = models.TextField(_("refresh token"), blank=True, null=True)
    # bank_number = models.CharField(
    #     _("bank number"), max_length=50, blank=True, null=True)
    # bank_code = models.CharField(
    #     _("bank code"), max_length=50, blank=True, null=True)
    # bank_name = models.CharField(
    #     _("bank name"), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(_("Date joined"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated date"), auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        related_name="users_groups",
        default="Customers",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="users_permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
