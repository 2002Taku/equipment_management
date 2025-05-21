from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    stock = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)  # アーカイブ・非表示管理用

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
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'Review for {self.equipment.name}'

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