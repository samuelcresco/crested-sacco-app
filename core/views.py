
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import SavingsAccount, Transaction, Member, Loan, ShareType
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Sum

# --- DASHBOARD VIEW ---
@login_required
def dashboard(request):
    try:
        member = request.user.member
        account = SavingsAccount.objects.get(member=member)
        transactions = Transaction.objects.filter(account=account).order_by('-date_created')[:10]
        
        total_deposits = Transaction.objects.filter(account=account, transaction_type='DEP').aggregate(Sum('amount'))['amount__sum'] or 0
        total_withdrawals = Transaction.objects.filter(account=account, transaction_type='WTH').aggregate(Sum('amount'))['amount__sum'] or 0
        total_transactions = Transaction.objects.filter(account=account).count()
        
        transaction_rows = ""
        for t in transactions:
            transaction_rows += f"""
            <tr>
                <td>{t.date_created.strftime('%d %b %Y')}</td>
                <td>{t.get_transaction_type_display()}</td>
                <td>UGX {t.amount:,.2f}</td>
            </tr>
            """
        
        if not transaction_rows:
            transaction_rows = '<tr><td colspan="3">No transactions yet.</td></tr>'
        
        full_name = f"{member.first_name} {member.last_name}".strip() or member.user.get_full_name() or member.user.username
        
        share_type = member.shares.name if member.shares else "No Share Type"
        share_count = member.share_balance
        share_value = member.share_balance * member.shares.price if member.shares else 0
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Crested SS 2005 Class - Dashboard</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: Arial, sans-serif; background: #f4f6f9; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; }}
                .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-bottom: 20px; }}
                .header {{ display: flex; justify-content: space-between; align-items: center; }}
                .logout-link {{ color: red; text-decoration: none; font-weight: bold; }}
                .brand {{ color: #1a3a5c; margin-bottom: 0; font-size: 28px; }}
                .sub {{ font-size: 18px; color: #333; margin-top: 5px; font-weight: 500; }}
                .member-id {{ font-size: 14px; color: #888; margin-top: 5px; }}
                .balance-box {{ background: linear-gradient(135deg, #1a3a5c, #2d6a9f); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .balance-box .label {{ font-size: 14px; opacity: 0.8; }}
                .balance-box .amount {{ font-size: 2.5em; font-weight: bold; }}
                .report-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 15px 0; }}
                .report-card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
                .report-card .num {{ font-size: 22px; font-weight: bold; color: #1a3a5c; }}
                .report-card .label {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th {{ background: #e9ecef; color: #333; padding: 10px; text-align: left; font-weight: 600; }}
                td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
                .share-card {{ background: #e8f4fd; padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #1a3a5c; }}
                @media (max-width: 600px) {{
                    .report-grid {{ grid-template-columns: 1fr 1fr; }}
                    .balance-box .amount {{ font-size: 1.8em; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <div class="header">
                        <h1 class="brand">🏦 Crested SS 2005 Class</h1>
                        <a href="/logout/" class="logout-link">Logout</a>
                    </div>
                    <p class="sub">👋 Welcome, {full_name}</p>
                    <p class="member-id">Member #: {member.member_number}</p>
                </div>
                
                <div class="card balance-box">
                    <div class="label">Current Savings Balance</div>
                    <div class="amount">UGX {account.balance:,.2f}</div>
                </div>
                
                <div class="card">
                    <h3 style="color: #1a3a5c; margin-bottom: 10px;">📈 Your Shares</h3>
                    <div class="share-card">
                        <p><strong>Share Type:</strong> {share_type}</p>
                        <p><strong>Shares Owned:</strong> {share_count}</p>
                        <p><strong>Total Share Value:</strong> UGX {share_value:,.2f}</p>
                    </div>
                </div>
                
                <div class="card">
                    <h3 style="color: #1a3a5c; margin-bottom: 10px;">📊 Your Savings Report</h3>
                    <div class="report-grid">
                        <div class="report-card">
                            <div class="num">UGX {total_deposits:,.2f}</div>
                            <div class="label">Total Deposits</div>
                        </div>
                        <div class="report-card">
                            <div class="num">UGX {total_withdrawals:,.2f}</div>
                            <div class="label">Total Withdrawals</div>
                        </div>
                        <div class="report-card">
                            <div class="num">{total_transactions}</div>
                            <div class="label">Total Transactions</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3 style="color: #1a3a5c; margin-bottom: 10px;">🕒 Recent Transactions</h3>
                    <table>
                        <tr><th>Date</th><th>Type</th><th>Amount</th></tr>
                        {transaction_rows}
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content)
        
    except Exception as e:
        return HttpResponse(f"<h1>Error</h1><p>{str(e)}</p>")

def custom_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        member_number = request.POST.get('member_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Debug: print what we received
        print(f"Signup attempt: member_number={member_number}, username={username}")
        
        if not member_number:
            error_message = "Member number is required. Please enter your member number."
        else:
            try:
                member = Member.objects.get(member_number=member_number)
                if member.user:
                    error_message = "This member number is already linked to an account. Please login."
                else:
                    user = User.objects.create_user(username=username, password=password)
                    member.user = user
                    member.first_name = first_name
                    member.last_name = last_name
                    member.save()
                    login(request, user)
                    return redirect('dashboard')
            except Member.DoesNotExist:
                error_message = f"Member number '{member_number}' not found. Please check with the SACCO admin."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
    
    return render(request, 'registration/register.html', {'error': error_message})

def custom_password_reset(request):
    error_message = None
    success_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            reset_link = f"http://{current_site.domain}/reset/{uid}/{token}/"
            print(f"\n========== PASSWORD RESET LINK ==========")
            print(f"Username: {user.username}")
            print(f"Reset Link: {reset_link}")
            print(f"=========================================\n")
            success_message = f"A password reset link has been generated for '{username}'. Check your Command Prompt!"
        except User.DoesNotExist:
            error_message = "No account found with this username."
    return render(request, 'registration/custom_password_reset.html', {'error': error_message, 'success': success_message})

@login_required
def loans(request):
    try:
        member = request.user.member
        account = SavingsAccount.objects.get(member=member)
        loan_limit = account.balance * 3
        active_loans = Loan.objects.filter(member=member, status='ACTIVE').order_by('next_due_date')
        loan_history = Loan.objects.filter(member=member).order_by('-date_taken')
        context = {
            'member': member,
            'account': account,
            'loan_limit': loan_limit,
            'active_loans': active_loans,
            'loan_history': loan_history,
        }
        return render(request, 'loans.html', context)
    except Exception as e:
        return HttpResponse(f"<h1>Error</h1><p>{str(e)}</p>")