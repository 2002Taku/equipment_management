from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Category, Tag
from .forms import ItemForm
from django.db.models import Avg, Count
from review.models import Review  # レビュー平均・件数表示用
from django.contrib.auth.decorators import login_required, user_passes_test

def item_list(request):
    q = request.GET.get('q', '')
    category_id = request.GET.get('category')
    items = Item.objects.filter(is_active=True)
    if q:
        items = items.filter(name__icontains=q) | items.filter(description__icontains=q) | items.filter(tags__name__icontains=q)
    if category_id:
        items = items.filter(category_id=category_id)
    items = items.distinct()

    # 高評価備品TOP3
    top_rated = (
        Item.objects.filter(is_active=True)
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating')[:3]
    )

    context = {
        'supplies': items,
        'top_rated': top_rated,
        'categories': Category.objects.all(),
        'q': q,
        'category_id': category_id,
    }
    return render(request, 'inventory/list.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    avg_rating = Review.objects.filter(item=item).aggregate(Avg('rating'))['rating__avg']
    review_count = Review.objects.filter(item=item).count()
    context = {
        'item': item,
        'avg_rating': avg_rating,
        'review_count': review_count,
    }
    return render(request, 'inventory/detail.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory:list')
    else:
        form = ItemForm()
    return render(request, 'inventory/create.html', {'form': form})

@login_required
def item_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/edit.html', {'form': form, 'item': item})

@login_required
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory:list')
    return render(request, 'inventory/delete.html', {'item': item})

def item_search(request):
    q = request.GET.get('q', '')
    category_id = request.GET.get('category')
    items = Item.objects.filter(is_active=True)
    if q:
        items = items.filter(name__icontains=q) | items.filter(description__icontains=q) | items.filter(tags__name__icontains=q)
    if category_id:
        items = items.filter(category_id=category_id)
    items = items.distinct()
    context = {
        'results': items,
        'categories': Category.objects.all(),
        'q': q,
        'category_id': category_id,
    }
    return render(request, 'inventory/search.html', context)