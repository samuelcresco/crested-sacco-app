from django.contrib import admin
from .models import Member, SavingsAccount, Transaction, Loan, LoanPayment

class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_number', 'user', 'phone_number']
    search_fields = ['member_number', 'user__username']

class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ['member', 'balance']
    search_fields = ['member__member_number']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'date_created']
    list_filter = ['transaction_type', 'date_created']
    search_fields = ['account__member__member_number']

class LoanAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'total_repayable', 'amount_paid', 'status', 'next_due_date']
    list_filter = ['status', 'date_taken']
    search_fields = ['member__member_number']

class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'penalty', 'date_paid', 'due_date']
    list_filter = ['date_paid']

admin.site.register(Member, MemberAdmin)
admin.site.register(SavingsAccount, SavingsAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanPayment, LoanPaymentAdmin)

admin.site.site_header = "Crested SS 2005 Class - Administration"
admin.site.site_title = "Crested SS 2005 Class"
admin.site.index_title = "🏦 Crested SS 2005 Class SACCO Management"