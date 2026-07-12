from django.contrib import admin
from .models import Member, SavingsAccount, Transaction

class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_number', 'user', 'phone_number']
    search_fields = ['member_number', 'user__username']

class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ['member', 'balance']
    search_fields = ['member__member_number', 'member__user__username']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'date_created']
    list_filter = ['transaction_type', 'date_created']
    search_fields = ['account__member__member_number']

admin.site.register(Member, MemberAdmin)
admin.site.register(SavingsAccount, SavingsAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)

# Customize admin site headers
admin.site.site_header = "Crested SS 2005 Class - Administration"
admin.site.site_title = "Crested SS 2005 Class"
admin.site.index_title = "Welcome to Crested SS 2005 Class SACCO"