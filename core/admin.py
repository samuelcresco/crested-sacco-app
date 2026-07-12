from django.contrib import admin
from .models import Member, SavingsAccount, Transaction

admin.site.register(Member)
admin.site.register(SavingsAccount)
admin.site.register(Transaction)