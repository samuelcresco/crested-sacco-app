from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# --- MEMBER ---
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    member_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.member_number} - {self.user.username if self.user else 'No User'}"

# --- SAVINGS ACCOUNT ---
class SavingsAccount(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.member.member_number} - Balance: {self.balance}"

# --- TRANSACTION ---
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

# --- LOAN ---
class Loan(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAID', 'Paid'),
        ('DEFAULTED', 'Defaulted'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # Percentage (e.g., 10%)
    total_repayable = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    date_taken = models.DateTimeField(auto_now_add=True)
    weekly_installment = models.DecimalField(max_digits=12, decimal_places=2)
    total_weeks = models.IntegerField()  # Total weekly installments
    weeks_paid = models.IntegerField(default=0)
    next_due_date = models.DateTimeField()

    def __str__(self):
        return f"Loan for {self.member.member_number} - {self.amount}"

    def remaining_balance(self):
        return self.total_repayable - self.amount_paid

    def is_overdue(self):
        return self.status == 'ACTIVE' and datetime.now() > self.next_due_date

# --- LOAN PAYMENT ---
class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    penalty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_paid = models.DateTimeField(auto_now_add=True)
    is_penalty = models.BooleanField(default=False)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"Payment for {self.loan.member.member_number} - {self.amount}"