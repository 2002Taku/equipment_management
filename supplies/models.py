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
            "文房具類",         # 例：ボールペン、ホッチキス、ノート、付箋、テープ、はさみ
            "事務機器",         # 例：プリンター、コピー機、シュレッダー、FAX、プロジェクター
            "家具類",           # 例：デスク、チェア、キャビネット、書庫、ロッカー
            "パソコン・周辺機器", # 例：ノートPC、デスクトップPC、モニター、マウス、キーボード、ルーター
            "通信機器",         # 例：電話機、ビジネスフォン、無線LAN機器
            "清掃・衛生用品",   # 例：掃除機、モップ、消毒液、ゴミ箱、ティッシュ、トイレットペーパー
            "飲食関連用品",     # 例：電気ポット、冷蔵庫、紙コップ、食器、コーヒーメーカー
            "防災用品",         # 例：消火器、非常食、懐中電灯、救急箱、ヘルメット
            "名札・識別用品",   # 例：名札ケース、社員証ホルダー、腕章
            "会議・プレゼン用品" # 例：ホワイトボード、マーカー、プロジェクタースクリーン、レーザーポインター
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

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='equipment_images/')
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Review(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, f'★{i}') for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.user} - ★{self.rating}"

class Archive(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f'Archive for {self.equipment.name}'

class Permission(models.Model):
    user = models.CharField(max_length=100)
    permission_level = models.CharField(max_length=50)

    def __str__(self):
        return f'Permission for {self.user}'

class Lending(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    borrower = models.CharField(max_length=100)
    due_date = models.DateField()

    def __str__(self):
        return f'Lending of {self.equipment.name} to {self.borrower}'

class Search(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword