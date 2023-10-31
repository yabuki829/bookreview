from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import uuid
import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is must")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
  email = models.EmailField(max_length=100,unique=True)
  is_active = models.BooleanField(default=False) 
  is_staff = models.BooleanField(default=False)
  activation_token = models.UUIDField(default=uuid.uuid4, editable=False)

  objects = UserManager()
  USERNAME_FIELD = "email"
  
  def __str__(self):
      return self.email
  def user_id(self):
    return self.id.__str__()




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    def __str__(self):
      return self.name

class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    published_at = models.DateField()
    image = models.ImageField(upload_to='medias/books/images/')
    def __str__(self):
      return self.title

class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
      return self.content