from django.contrib import admin
from .models import Member, SavingsAccount, Transaction, Loan, LoanPayment

# --- MEDIA CLASS FOR CUSTOM CSS ---
class AdminMixin:
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }

# --- REGISTER MODELS WITH CUSTOM CSS ---
@admin.register(Member)
class MemberAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['member_number', 'user', 'phone_number']
    search_fields = ['member_number', 'user__username']
    list_filter = ['user__is_active']

@admin.register(SavingsAccount)
class SavingsAccountAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['member', 'balance']
    search_fields = ['member__member_number', 'member__user__username']

@admin.register(Transaction)
class TransactionAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'date_created']
    list_filter = ['transaction_type', 'date_created']
    search_fields = ['account__member__member_number']

@admin.register(Loan)
class LoanAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['member', 'amount', 'total_repayable', 'status', 'next_due_date']
    list_filter = ['status', 'date_taken']
    search_fields = ['member__member_number']

@admin.register(LoanPayment)
class LoanPaymentAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ['loan', 'amount', 'penalty', 'date_paid']
    list_filter = ['date_paid']
    search_fields = ['loan__member__member_number']

# --- ADMIN SITE BRANDING ---
admin.site.site_header = "Crested SS 2005 Class - Banking System"
admin.site.site_title = "Crested SS 2005 Class"
admin.site.index_title = "🏦 Welcome to Crested SS 2005 Class SACCO Banking System"