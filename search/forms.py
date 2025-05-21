from django import forms

class EquipmentSearchForm(forms.Form):
    query = forms.CharField(label='検索キーワード', max_length=100, required=True)
    category = forms.ChoiceField(label='カテゴリ', choices=[('all', 'すべて')] + [(category, category) for category in ['電子機器', '家具', '文房具']])
    available = forms.BooleanField(label='在庫あり', required=False)