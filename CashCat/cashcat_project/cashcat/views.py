from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if action == 'signup':
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, 'Account created successfully. Please log in.')
        elif action == 'login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth.html')

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = Transaction.objects.filter(user=request.user, transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=request.user, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    categories = Transaction.objects.filter(user=request.user).values('category').annotate(total_amount=Sum('amount')).order_by('category')
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'categories': categories,
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'transaction_to_delete': transaction})

@login_required
def logout_view(request):
    logout(request)
    return redirect('auth')