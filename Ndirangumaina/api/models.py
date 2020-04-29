from django.db import models
from django.contrib.auth.models import AbstractBaseUser # standard baseclass to use when customizing or overriding default user model
from django.contrib.auth.models import PermissionsMixin # standard baseclass 2
from django.contrib.auth.models import BaseUserManager # default model manager to inherit from
from datetime import datetime
from estate import settings
from .validators import validate_file_extension, validate_file_extension2

# Create your models here.
# Custom user profile manager to make things work in django CLI
class UserProfileManager(BaseUserManager):
    """manager for user profiles"""
    def create_user(self, email, name, organization, bio, password=None): 
        """create new user profile"""
        if not email: 
            raise ValueError('User must have an email address')

        email = self.normalize_email(email) 
        user = self.model(email=email, name=name, organization=organization, bio=bio) 

        user.set_password(password) 
        user.save(using=self._db) 

        return user
    
    # this will use the create_user function but grant super user 
    def create_superuser(self, email, name, organization, bio, password):
        """create and save new super user"""
        user = self.create_user(email, name, organization, bio, password)
        user.is_superuser = True # automatically created by permissionsmixin
        user.admin = True

        user.is_staff = True # automatically created by permissionsmixin
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin): 
    """database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, default="org")
    
    bio = models.TextField(max_length=120, default="Bio")
    avatar = models.FileField(null=False, validators=[validate_file_extension])

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) 

    objects = UserProfileManager() 
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['name', 'organization', 'bio'] 

    def get_name(self):
        return self.name

    def __str__(self):
        return self.email


class UserProfileData(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        )
    
    title = models.CharField(max_length=50)
    image = models.FileField(null=False, validators=[validate_file_extension])

    video = models.FileField(null=False, validators=[validate_file_extension2])
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FeaturedData(models.Model):
    identification = models.CharField(max_length=120)
    featured = models.ForeignKey(UserProfileData, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.identification


