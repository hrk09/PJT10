from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# usermodel customizing
class User(AbstractUser):
    # followers랑 user m:n
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # 역.참.조
        related_name='followings',
    )
