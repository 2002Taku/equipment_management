from django.db import models
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="カテゴリ名")

    def __str__(self):
        return self.name

# カテゴリ初期データを自動登録
@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    if sender.name == "supplies":
        initial_categories = [
            "文房具類",
            "事務機器",
            "家具類",
            "パソコン・周辺機器",
            "通信機器",
            "清掃・衛生用品",
            "飲食関連用品",
            "防災用品",
            "名札・識別用品",
            "会議・プレゼン用品"
        ]
        for name in initial_categories:
            Category.objects.get_or_create(name=name)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="タグ名")

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="備品名")
    description = models.TextField(blank=True, verbose_name="説明")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    tags = models.ManyToManyField(Tag, blank=True, related_name='items')
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=1, verbose_name="在庫数")
    is_active = models.BooleanField(default=True, verbose_name="表示中")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.user} - {dict(self.RATING_CHOICES).get(self.rating, '')}"