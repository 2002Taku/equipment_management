from django import forms
from .models import Lending

# 貸出申請用フォーム（現状は空。将来拡張用）
class BorrowForm(forms.Form):
    pass

# 返却申請用フォーム（現状は空。将来拡張用）
class ReturnForm(forms.Form):
    pass