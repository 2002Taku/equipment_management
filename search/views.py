from django.shortcuts import render
from supplies.models import Item, Category, Tag
from django.db import models

def search_result(request):
    query = request.GET.get('q', '')         # キーワード
    category = request.GET.get('category', '')  # カテゴリ

    items = Item.objects.filter(is_active=True).annotate(
        avg_rating=models.Avg('reviews__rating')
    )  # まず有効な備品のみ

    if query:
        # 名前または説明文にキーワードが含まれるもの
        items = items.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )
    if category:
        # カテゴリでさらに絞り込み（AND条件になる）
        items = items.filter(category__name=category)

    categories = Category.objects.all()  # 追加
    tags = Tag.objects.all()
    # 高評価TOP3も一覧と同じように渡す
    top_rated = (
        Item.objects.filter(is_active=True)
        .annotate(avg_rating=models.Avg('reviews__rating'))
        .order_by('-avg_rating')[:3]
    )

    return render(request, 'supplies/list.html', {
        'items': items,
        'categories': categories,
        'tags': tags,
        'top_rated': top_rated,
        'search_mode': True,  # 検索結果であることをテンプレートで判別するため
        'query': query,
        'selected_category': category,
    })