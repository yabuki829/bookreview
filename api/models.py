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

from django.db.models import Avg

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    subTitle = models.CharField(max_length=255,default="")
    # 作者が複数人いる場合は代表者一名のみ表示する
    author = models.CharField(max_length=255,default="None")
    description = models.TextField(default="") 
    published_at = models.DateField()
    # image = models.ImageField(upload_to='books/images/')
    image = models.ImageField(upload_to='books/images/')
    # 本の評価の平均
    average_rating = models.FloatField(default=0.0, blank=True)
    review_count = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.title
    # 本のレビューを追加したら再計算させる
    def update_ratings(self):
        average = self.reviews.aggregate(average=Avg('rating'))['average']
        self.average_rating = average if average is not None else 0.0
        self.review_count = self.reviews.count()
        self.save()

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import transaction

class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="1から5の範囲で評価をつけてください。",
        default=1,
    )

    def __str__(self):
        return "「" + self.book.title +"」："+ self.content
    # ... その他のフィールド ...

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with transaction.atomic():
            self.book.update_ratings()


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# TODO 投票機能
class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls')
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)  

    def __str__(self):
        return self.text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')

    def __str__(self):
        return f"{self.user.username} voted on {self.poll.question}"

        

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