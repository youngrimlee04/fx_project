from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=50,
        verbose_name="환전소 이름",
    )
    contact = models.CharField(
        max_length=50,
        verbose_name="연락처",
    )
    address = models.CharField(
        max_length=200,
        verbose_name="주소",
    )
    description = models.TextField(
        verbose_name="상세 소개",
    )

class Menu(models.Model):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name="판매통화 이미지"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="판매통화명"
    )
    price = models.FloatField(
        verbose_name="통화 단위당 가격"
    )
