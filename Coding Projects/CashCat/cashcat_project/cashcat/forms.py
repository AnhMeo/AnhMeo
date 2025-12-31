from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }