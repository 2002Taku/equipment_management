from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.views import View
from lending.models import Lending
from .models import Item, Category, Tag, Review
from .forms import ItemForm, ReviewForm

def item_list(request):
    # 備品一覧ページ。全ての有効な備品を表示し、平均評価も付与
    items = Item.objects.filter(is_active=True).annotate(
        avg_rating=Avg('reviews__rating')
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    # 高評価TOP3を取得
    top_rated = (
        Item.objects.filter(is_active=True)
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating')[:3]
    )
    context = {
        'items': items,
        'categories': categories,
        'tags': tags,
        'top_rated': top_rated,
    }
    return render(request, 'supplies/list.html', context)

def item_detail(request, item_id):
    # 備品詳細ページ。レビューや平均評価、借用状態なども表示
    item = get_object_or_404(Item, id=item_id)
    reviews = item.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # ★1〜★5の件数リストを作成
    rating_counts = [reviews.filter(rating=i).count() for i in range(1, 6)]

    # ログインユーザーがこの備品を借りているか判定
    is_borrowed = False
    if request.user.is_authenticated:
        is_borrowed = Lending.objects.filter(item=item, user=request.user).exists()

    context = {
        'item': item,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_counts': rating_counts,
        'is_borrowed': is_borrowed,
    }
    return render(request, 'supplies/detail.html', context)

def item_create(request):
    # 備品新規登録ページ
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('supplies:list')
    else:
        form = ItemForm()
    return render(request, 'supplies/create.html', {'form': form})

def item_edit(request, item_id):
    # 備品編集ページ
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('supplies:detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'supplies/edit.html', {'form': form, 'item': item})

def item_delete(request, item_id):
    # 備品を論理削除（is_active=Falseにする）
    item = get_object_or_404(Item, id=item_id)
    item.is_active = False
    item.save()
    return redirect('supplies:list')

def review_list(request, item_id):
    """
    現在review_list.htmlは使用していないため、item_detailへリダイレクトする
    """
    return redirect('supplies:detail', item_id=item_id)

@login_required
def review_create(request, item_id):
    # レビュー新規作成ページ
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('supplies:detail', item_id=item.id)
    else:
        form = ReviewForm()
    return render(request, 'supplies/review_create.html', {'form': form, 'item': item})

class ReviewDeleteView(View):
    # レビュー削除（POSTのみ対応、確認画面は別関数で対応）
    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return redirect('supplies:detail', item_id=review.item.id)

@login_required
def review_delete_confirm(request, review_id):
    # レビュー削除確認画面と削除処理（本人のみ削除可）
    review = get_object_or_404(Review, id=review_id)
    # 本人以外は削除不可
    if review.user != request.user:
        return redirect('supplies:detail', item_id=review.item.id)
    if request.method == 'POST':
        review.delete()
        return redirect('supplies:detail', item_id=review.item.id)
    return render(request, 'supplies/review_delete_confirm.html', {'review': review})