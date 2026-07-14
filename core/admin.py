from django.contrib import admin
from django import forms
from .models import Member, SavingsAccount, Transaction, Loan, LoanPayment
from datetime import datetime, timedelta

# --- MEDIA CLASS FOR CUSTOM CSS ---
class AdminMixin:
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }

# --- MEMBER ---
@admin.register(Member)
class MemberAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['member_number', 'first_name', 'last_name', 'phone_number', 'user']
    search_fields = ['member_number', 'first_name', 'last_name', 'user__username']
    list_filter = ['user__is_active']
    fields = ['member_number', 'first_name', 'last_name', 'phone_number', 'user']

# --- SAVINGS ACCOUNT ---
@admin.register(SavingsAccount)
class SavingsAccountAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['member', 'balance']
    search_fields = ['member__member_number', 'member__user__username']

# --- TRANSACTION ---
@admin.register(Transaction)
class TransactionAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'date_created']
    list_filter = ['transaction_type', 'date_created']
    search_fields = ['account__member__member_number']

# --- LOAN (With Custom Form to Auto-Fill Date) ---
class LoanAdminForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'next_due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

@admin.register(Loan)
class LoanAdmin(AdminMixin, admin.ModelAdmin):
    form = LoanAdminForm
    list_display = ['member', 'amount', 'total_repayable', 'amount_paid', 'remaining_balance', 'status', 'next_due_date']
    list_filter = ['status', 'date_taken']
    search_fields = ['member__member_number']
    fields = ['member', 'amount', 'interest_rate', 'total_repayable', 'amount_paid', 'status', 'weekly_installment', 'total_weeks', 'weeks_paid', 'next_due_date']

    def remaining_balance(self, obj):
        return obj.total_repayable - obj.amount_paid
    remaining_balance.short_description = 'Remaining Balance'

    def save_model(self, request, obj, form, change):
        # Auto-calculate total_repayable if not set
        if not obj.total_repayable:
            obj.total_repayable = obj.amount + (obj.amount * obj.interest_rate / 100)
        
        # Auto-calculate weekly installment
        if obj.total_weeks and obj.total_weeks > 0:
            obj.weekly_installment = obj.total_repayable / obj.total_weeks
        
        # Set next_due_date to 7 days from today if not set
        if not obj.next_due_date:
            obj.next_due_date = datetime.now() + timedelta(days=7)
        
        super().save_model(request, obj, form, change)

# --- LOAN PAYMENT (With Auto-Update Logic) ---
@admin.register(LoanPayment)
class LoanPaymentAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['loan', 'amount', 'penalty', 'date_paid']
    list_filter = ['date_paid']
    search_fields = ['loan__member__member_number']

    def save_model(self, request, obj, form, change):
        # Save the payment first
        super().save_model(request, obj, form, change)
        
        # Update the Loan's amount_paid by summing all payments
        total_paid = LoanPayment.objects.filter(loan=obj.loan).aggregate(models.Sum('amount'))['amount__sum'] or 0
        obj.loan.amount_paid = total_paid
        
        # Check if the loan is fully paid
        if obj.loan.amount_paid >= obj.loan.total_repayable:
            obj.loan.status = 'PAID'
        
        obj.loan.save()

    def delete_model(self, request, obj):
        loan = obj.loan
        obj.delete()
        # Recalculate after deletion
        total_paid = LoanPayment.objects.filter(loan=loan).aggregate(models.Sum('amount'))['amount__sum'] or 0
        loan.amount_paid = total_paid
        if loan.amount_paid >= loan.total_repayable:
            loan.status = 'PAID'
        else:
            loan.status = 'ACTIVE'
        loan.save()

# --- ADMIN BRANDING ---
admin.site.site_header = "Crested SS 2005 Class - Banking System"
admin.site.site_title = "Crested SS 2005 Class"
admin.site.index_title = "🏦 Welcome to Crested SS 2005 Class SACCO Banking System"