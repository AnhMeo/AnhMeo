from django.shortcuts import render, redirect

# Create your views here.
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum

def dashboard(request):
    transactions = Transaction.objects.all()
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    categories = Transaction.objects.values('category').annotate(total_amount=Sum('amount')).order_by('category')
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'categories': categories,
    }
    return render(request, 'dashboard.html', context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})