from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

from ...models import Profile
from utils.book_service import BookService
User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("--------------------------------------------------------------------------")
        print("1. スーパーユーザを作成するコマンドです")
        print("--------------------------------------------------------------------------")
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            print("--------------------------------------------------------------------------")
            print("2. スーパーユーザーを作成します。")
            print("--------------------------------------------------------------------------")
            user = User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            print("--------------------------------------------------------------------------")
            print("3. スーパーユーザー作成が完了しました。")
            print("--------------------------------------------------------------------------")
            # profileを作成する
            print("プロフィールを作成します")
            servise = BookService()

            profile = Profile.objects.create(
                id = servise.create_id(22),
                user=user,name="sho",bio="ツギヨム開発者です"
                )
            profile.save()
            print("プロフィールの作成が完了しました。")
            print("--------------------------------------------------------------------------")
           
        
        else:
            print("--------------------------------------------------------------------------")
            print("2.作成済みです")
            print("--------------------------------------------------------------------------")