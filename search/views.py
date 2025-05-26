from django.shortcuts import render
from supplies.models import Item, Category
from django.db import models

def search_result(request):
    query = request.GET.get('q', '')         # キーワード
    category = request.GET.get('category', '')  # カテゴリ

    items = Item.objects.filter(is_active=True)  # まず有効な備品のみ

    if query:
        # 名前または説明文にキーワードが含まれるもの
        items = items.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )
    if category:
        # カテゴリでさらに絞り込み（AND条件になる）
        items = items.filter(category__name=category)

    categories = Category.objects.all()  # 追加

    return render(request, 'search/result.html', {
        'items': items,
        'query': query,
        'category': category,
        'categories': categories,  # 追加
    })