from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.views import View  # ← これを追加
from .models import Item, Category, Tag, Review
from .forms import ItemForm, ReviewForm

def item_list(request):
    items = Item.objects.filter(is_active=True).annotate(
        avg_rating=Avg('reviews__rating')
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    # 高評価TOP3
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
    item = get_object_or_404(Item, id=item_id)
    reviews = item.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # ★1〜★5の件数リストを作成
    rating_counts = [reviews.filter(rating=i).count() for i in range(1, 6)]
    context = {
        'item': item,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_counts': rating_counts,  # ← 追加
    }
    return render(request, 'supplies/detail.html', context)

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('supplies:list')
    else:
        form = ItemForm()
    return render(request, 'supplies/create.html', {'form': form})

def item_edit(request, item_id):
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
    item = get_object_or_404(Item, id=item_id)
    item.is_active = False
    item.save()
    return redirect('supplies:list')

def review_list(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    reviews = Review.objects.filter(item=item).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = reviews.count()
    rating_counts = [reviews.filter(rating=i).count() for i in range(1, 6)]
    context = {
        'item': item,
        'reviews': reviews,
        'avg_rating': f"{avg_rating:.1f}" if avg_rating else "0.0",
        'review_count': review_count,
        'rating_counts': rating_counts,
    }
    return render(request, 'supplies/review_list.html', context)

@login_required
def review_create(request, item_id):
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
    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return redirect('supplies:detail', item_id=review.item.id)