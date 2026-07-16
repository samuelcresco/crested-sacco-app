from django.contrib import admin
from django import forms
from .models import Member, SavingsAccount, Transaction, Loan, LoanPayment, ShareType

@admin.register(ShareType)
class ShareTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_number', 'first_name', 'last_name', 'shares', 'share_balance', 'phone_number', 'user']
    search_fields = ['member_number', 'first_name', 'last_name']

@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ['member', 'balance']
    search_fields = ['member__member_number']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'date_created']
    list_filter = ['transaction_type', 'date_created']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'total_repayable', 'amount_paid', 'status', 'next_due_date']
    list_filter = ['status']

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'penalty', 'date_paid']

admin.site.site_header = "Crested SS 2005 Class - Banking System"
admin.site.site_title = "Crested SS 2005 Class"
admin.site.index_title = "Crested SS 2005 Class"