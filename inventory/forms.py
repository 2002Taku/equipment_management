from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'image', 'tags', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.CheckboxSelectMultiple,
        }

class EquipmentSearchForm(forms.Form):
    query = forms.CharField(label='検索', max_length=100, required=False)

class EquipmentLendingForm(forms.Form):
    equipment_id = forms.IntegerField(widget=forms.HiddenInput())
    borrower_name = forms.CharField(label='借用者名', max_length=100)
    return_date = forms.DateField(label='返却予定日', widget=forms.SelectDateWidget())