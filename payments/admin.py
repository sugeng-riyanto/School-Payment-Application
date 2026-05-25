from django.contrib import admin
from .models import PaymentTransaction, PaymentProof


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('student', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('status', 'transaction_type')
    search_fields = ('student__full_name', 'midtrans_order_id')


@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ('student', 'is_verified', 'uploaded_at')
    list_filter = ('is_verified',)
