from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import SavingsAccount, Transaction, Member
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string

# --- DASHBOARD VIEW ---
@login_required
def dashboard(request):
    try:
        member = request.user.member
        account = SavingsAccount.objects.get(member=member)
        transactions = Transaction.objects.filter(account=account).order_by('-date_created')[:5]
        
        # Build transaction rows
        transaction_rows = ""
        for t in transactions:
            transaction_rows += f"""
            <tr>
                <td>{t.date_created.strftime('%d %b %Y')}</td>
                <td>{t.get_transaction_type_display()}</td>
                <td>{t.amount}</td>
            </tr>
            """
        
        if not transaction_rows:
            transaction_rows = '<tr><td colspan="3">No transactions yet.</td></tr>'
        
        # Build the FULL HTML page with a GET logout link (no CSRF needed)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Crested SS 2005 Class - Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
                .card {{ max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .brand {{ color: #1a3a5c; margin-bottom: 0; font-size: 28px; }}
                .sub {{ font-size: 14px; color: #666; margin-top: 5px; }}
                .balance {{ font-size: 2.5em; color: #2c3e50; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background: #3498db; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .logout-link {{ float: right; color: red; text-decoration: none; font-size: 14px; }}
                .logout-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="card">
                <a href="/logout/" class="logout-link">Logout</a>
                <h1 class="brand">Crested SS 2005 Class</h1>
                <p class="sub">Welcome, {member.user.username}</p>
                <p>Member #: {member.member_number}</p>
                <hr>
                <h3>Current Balance</h3>
                <div class="balance">KES {account.balance}</div>
                
                <h3>Recent Transactions</h3>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Type</th>
                        <th>Amount</th>
                    </tr>
                    {transaction_rows}
                </table>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content)
        
    except Exception as e:
        return HttpResponse(f"<h1>Error</h1><p>{str(e)}</p>")


# --- CUSTOM LOGOUT VIEW ---
def custom_logout(request):
    logout(request)
    return redirect('login')


# --- REGISTRATION VIEW ---
def register(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        member_number = request.POST.get('member_number')
        
        try:
            member = Member.objects.get(member_number=member_number)
            
            if member.user:
                error_message = "This member number is already linked to an account. Please login."
            else:
                user = User.objects.create_user(username=username, password=password)
                member.user = user
                member.save()
                login(request, user)
                return redirect('dashboard')
                
        except Member.DoesNotExist:
            error_message = "Member number not found. Please check with the SACCO admin."
            
    return render(request, 'registration/register.html', {'error': error_message})


# --- PASSWORD RESET VIEW ---
def custom_password_reset(request):
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            user = User.objects.get(username=username)
            
            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset link
            current_site = get_current_site(request)
            reset_link = f"http://{current_site.domain}/reset/{uid}/{token}/"
            
            # Print to console
            print(f"\n========== PASSWORD RESET LINK ==========")
            print(f"Username: {user.username}")
            print(f"Reset Link: {reset_link}")
            print(f"=========================================\n")
            
            success_message = f"A password reset link has been generated for '{username}'. Check your Command Prompt!"
            
        except User.DoesNotExist:
            error_message = "No account found with this username."
    
    return render(request, 'registration/custom_password_reset.html', {
        'error': error_message,
        'success': success_message,
    })