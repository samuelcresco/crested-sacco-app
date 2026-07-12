from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_number = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.member_number} - {self.user.username}"

class SavingsAccount(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.member.user.username} - Balance: {self.balance}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEP', 'Deposit'),
        ('WTH', 'Withdrawal'),
    ]
    account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount}"