from django.contrib import admin

# Register your models here.
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'category', 'amount', 'description', 'date')
    list_filter = ('transaction_type', 'category')
    search_fields = ('category', 'description')