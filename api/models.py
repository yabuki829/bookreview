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
        user.is_active = True
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255,default="")
    # 作者が複数人いる場合は代表者一名のみ表示する
    author = models.CharField(max_length=255,default="None")
    description = models.TextField(default="") 
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



# TODO 今後実装予定の本のランキング

# class Ranking(models.Model):
#     name = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     books = models.ManyToManyField(Book, through='RankingEntry')

#     def __str__(self):
#         return self.name

# class RankingEntry(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)
    # 投票数を数字でなくuserにした方が良さそう?
#     votes = models.PositiveIntegerField(default=0)

#     class Meta:
#         unique_together = ('book', 'ranking')

#     def __str__(self):
#         return f"{self.book.title} in {self.ranking.name}"

# class Vote(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ranking_entry = models.ForeignKey(RankingEntry, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'ranking_entry')

#     def __str__(self):
#         return f"{self.user.username} voted for {self.ranking_entry.book.title}"


# TODO : unique_togetherについて記事を書く