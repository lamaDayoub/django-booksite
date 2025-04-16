
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, default="")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager() 
    
    def __str__(self):
        return self.email
    
class UserPasswordHistory(models.Model):
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='password_history')
    hashed_password=models.CharField(max_length=128)
    created_at=models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering=['-created_at']
        verbose_name = 'User Password History'
        verbose_name_plural = 'User Password Histories'
            
    def __str__(self):
        return f"Password history for {self.user.email} at {self.created_at}"
        