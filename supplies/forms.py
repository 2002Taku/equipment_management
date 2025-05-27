from django import forms
from .models import Item, Review

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # 'tags'と'is_active'を除外
        fields = ['name', 'description', 'category', 'image', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.Select(),  # モデルのchoicesが自動で反映されます
        }