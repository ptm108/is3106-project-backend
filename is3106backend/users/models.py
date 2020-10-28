from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import uuid

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)
# end def

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    # end def

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    # end def
# end class


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    profile_photo = models.ImageField(upload_to=user_directory_path, max_length=100, blank=True, null=True, default='/static/user-profile.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    # end def

    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj=obj)
    # end def

    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)
    # end def

    @property
    def is_staff(self):
        return self.is_admin
    # end def
    
# end class

class VendorUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=200, null=True, default='')
    is_vendor = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.vendor_name}'
    #end def

# end class

class DeliveryAddress(models.Model):
    add_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)

    # user's delivery address
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)

    address_list = models.Manager()

    def __str__(self):
        return f'{self.postal_code}'
    #end def

#end class
