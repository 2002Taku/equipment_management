from django.shortcuts import render
from supplies.models import Item, Category

def search_result(request):
    q = request.GET.get('q', '')
    category_id = request.GET.get('category')
    items = Item.objects.filter(is_active=True)
    if q:
        items = items.filter(
            name__icontains=q
        ) | items.filter(
            description__icontains=q
        ) | items.filter(
            tags__name__icontains=q
        )
    if category_id:
        items = items.filter(category_id=category_id)
    items = items.distinct()
    context = {
        'results': items,
        'categories': Category.objects.all(),
        'q': q,
        'category_id': category_id,
    }
    return render(request, 'search/result.html', context)