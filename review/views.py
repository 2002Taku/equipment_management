from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Review
from .forms import ReviewForm
from inventory.models import Item
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required

def review_list(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    reviews = Review.objects.filter(item=item).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = reviews.count()
    # 評価点ごとの件数
    rating_counts = [reviews.filter(rating=i).count() for i in range(1, 6)]
    context = {
        'item': item,
        'reviews': reviews,
        'avg_rating': f"{avg_rating:.1f}" if avg_rating else "0.0",
        'review_count': review_count,
        'rating_counts': rating_counts,
    }
    return render(request, 'review/list.html', context)

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
            return redirect('review:list', item_id=item.id)
    else:
        form = ReviewForm()
    return render(request, 'review/create.html', {'form': form, 'item': item})

class ReviewDeleteView(View):
    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return redirect('review:list')