from django import forms

class ArchiveReasonForm(forms.Form):
    archive_reason = forms.CharField(label='非表示理由', widget=forms.Textarea, required=True)