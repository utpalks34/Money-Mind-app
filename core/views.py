from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm, ExpenseForm, DebtForm, MoodLogForm, ChangePasswordForm
from .models import Expense, Debt, MoodLog, AIAdvice, UserProfile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import AIAdvice
from .forms import AIAdviceForm
from datetime import date
from collections import defaultdict
import openai
from django.conf import settings
from django.db.models import Sum
from builtins import sum

from .utils import call_openai_function  # Your helper to call LLM





# Register a new user and create a profile
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, income=0, savings=0)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


# Login user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'core/login.html')


# Logout user
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Dashboard
@login_required
def dashboard_view(request):
    expenses = Expense.objects.filter(user=request.user)
    debts = Debt.objects.filter(user=request.user)
    moods = MoodLog.objects.filter(user=request.user).order_by('-date')[:5]
    advice = AIAdvice.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Fix 1: Only include current month's expenses
    current_month = date.today().month
    monthly_expenses = expenses.filter(date__month=current_month)
    total_monthly_expense = sum(e.amount for e in monthly_expenses)

    # Fix 2: Filter unpaid debts only
    total_debt = sum(d.amount for d in debts if not d.is_paid)

    # Fix 3: Prepare category-wise expense summary for doughnut chart
    category_expenses = defaultdict(float)
    for e in monthly_expenses:
        category_expenses[e.category] += float(e.amount)

    context = {
        'expenses': expenses,
        'debts': debts,
        'recent_moods': moods,
        'recent_advice': advice,
        'total_monthly_expense': total_monthly_expense,
        'total_debt': total_debt,
        'category_expenses': dict(category_expenses),
    }
    return render(request, 'core/dashboard.html', context)


# Expense list and form
@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user)
    expense_categories = Expense.CATEGORY_CHOICES  

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expenses')
    else:
        form = ExpenseForm()

    return render(request, 'core/expense_list.html', {
        'form': form,
        'expenses': expenses,
        'expense_categories': expense_categories  
    })



# Debt list and form
@login_required
def debt_list_view(request):
    debts = Debt.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user
            debt.save()
            messages.success(request, 'Debt saved!')
            return redirect('debts') 
    else:
        form = DebtForm()

    return render(request, 'core/debt_list.html', {
        'form': form,
        'debts': debts,
        'debt_categories': Debt.DEBT_TYPE_CHOICES  
    })

#edit debt
def edit_debt_view(request, id):
    debt = get_object_or_404(Debt, id=id, user=request.user)
    
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            messages.success(request, "Debt updated successfully.")
            return redirect('debts')
    else:
        form = DebtForm(instance=debt)
    
    return render(request, 'core/debt_edit.html', {'form': form, 'debt': debt})

#delete debt

@login_required
def delete_debt_view(request, id):
    debt = get_object_or_404(Debt, id=id, user=request.user)
    
    if request.method == 'POST':
        debt.delete()
        messages.success(request, "Debt deleted successfully.")
        return redirect('debts')
    
    return redirect('debts')






# Mood tracker
@login_required
def mood_tracker_view(request):
    moods = MoodLog.objects.filter(user=request.user).order_by('-date')
    mood_choices = MoodLog.MOOD_CHOICES
    if request.method == 'POST':
        form = MoodLogForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood logged!')
            return redirect('mood_tracker')
    else:
        form = MoodLogForm()
    return render(request, 'core/mood_tracker.html', {'form': form, 'moods': moods,'mood_choices': mood_choices})

#edit and delete 
 
@login_required
def edit_mood_view(request, id):
    mood = get_object_or_404(MoodLog, id=id, user=request.user)

    if request.method == 'POST':
        form = MoodLogForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mood updated successfully!')
            return redirect('mood_tracker')
    else:
        form = MoodLogForm(instance=mood)

    return render(request, 'core/mood_edit.html', {'form': form, 'mood': mood})

# Delete Mood View
@login_required
def delete_mood_view(request, id):
    mood = get_object_or_404(MoodLog, id=id, user=request.user)

    if request.method == 'POST':
        mood.delete()
        messages.success(request, 'Mood entry deleted!')
        return redirect('mood_tracker')

    return render(request, 'core/mood_confirm_delete.html', {'mood': mood})

#ai


@login_required
def ai_advisor_view(request):
    user = request.user

    # Ensure user has profile
    user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'income': 0, 'savings': 0})

    # Calculate totals
    advice_history = AIAdvice.objects.filter(user=user).order_by('-created_at')
    monthly_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_debt = Debt.objects.filter(user=user, is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0

    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            response = call_openai_function(question, user, monthly_expenses, total_debt)
            AIAdvice.objects.create(user=user, question=question, response=response)
            messages.success(request, "AI advice generated.")
            return redirect('ai_advisor')

    return render(request, 'core/ai_advisor.html', {
        'advice_history': advice_history,
        'monthly_expenses': monthly_expenses,
        'total_debt': total_debt,
        'user_profile': user_profile,
    })

@login_required
def delete_advice_view(request, id):
    advice = get_object_or_404(AIAdvice, id=id, user=request.user)
    if request.method == 'POST':
        advice.delete()
        messages.success(request, "Advice deleted.")
        return redirect('ai_advisor')





# Profile view
@login_required
def profile_view(request):
    profile = request.user.userprofile
    income = profile.income or 0
    savings = profile.savings or 0

    # Total expenses this month
    monthly_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_debt = Debt.objects.filter(user=request.user, is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0

    # Avoid division by zero
    expense_percentage = round((monthly_expenses / income) * 100, 1) if income > 0 else 0
    debt_percentage = round((total_debt / income) * 100, 1) if income > 0 else 0
    savings_rate = round((savings / income) * 100, 1) if income > 0 else 0

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'core/profile.html', {
        'form': form,
        'profile': profile,
        'monthly_expenses': monthly_expenses,
        'total_debt': total_debt,
        'expense_percentage': expense_percentage,
        'debt_percentage': debt_percentage,
        'savings_rate': savings_rate,
    })



# Change password view
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'core/change_password.html', {'form': form})


def edit_expense_view(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'core/expense_edit.html', {'form': form, 'expense': expense})


# Delete account
def delete_expense_view(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return redirect('expenses')




































    
        
