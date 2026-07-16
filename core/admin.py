from django.contrib import admin
from django import forms
from .models import Member, SavingsAccount, Transaction, Loan, LoanPayment, ShareType
from datetime import datetime, timedelta
from django.db import models as db_models

class AdminMixin:
    class Media:
        css = {'all': ('admin/custom_admin.css',)}

@admin.register(ShareType)
class ShareTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']
    search_fields = ['name']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_number', 'first_name', 'last_name', 'shares', 'share_balance', 'phone_number', 'user']
    search_fields = ['member_number', 'first_name', 'last_name']
    fields = ['member_number', 'first_name', 'last_name', 'phone_number', 'user', 'shares', 'share_balance']

@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ['member', 'balance']
    search_fields = ['member__member_number']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'date_created']
    list_filter = ['transaction_type', 'date_created']

class LoanAdminForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {'next_due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    form = LoanAdminForm
    list_display = ['member', 'amount', 'total_repayable', 'amount_paid', 'status', 'next_due_date']
    list_filter = ['status']
    fields = ['member', 'amount', 'interest_rate', 'total_repayable', 'status', 'weekly_installment', 'total_weeks', 'weeks_paid', 'next_due_date']

    def save_model(self, request, obj, form, change):
        if not obj.total_repayable:
            obj.total_repayable = obj.amount + (obj.amount * obj.interest_rate / 100)
        if obj.total_weeks and obj.total_weeks > 0:
            obj.weekly_installment = obj.total_repayable / obj.total_weeks
        if not obj.next_due_date:
            obj.next_due_date = datetime.now() + timedelta(days=7)
        super().save_model(request, obj, form, change)

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'penalty', 'date_paid']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        total_paid = LoanPayment.objects.filter(loan=obj.loan).aggregate(db_models.Sum('amount'))['amount__sum'] or 0
        obj.loan.amount_paid = total_paid
        if obj.loan.amount_paid >= obj.loan.total_repayable:
            obj.loan.status = 'PAID'
        obj.loan.save()

admin.site.site_header = "Crested SS 2005 Class - Banking System"
admin.site.site_title = "Crested SS 2005 Class"
admin.site.index_title = "🏦 Welcome to Crested SS 2005 Class"sss