from django import forms 
from .models import UserProfile,Expense,Debt,MoodLog,AIAdvice
from django.contrib.auth.forms import PasswordChangeForm

#profile form 
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['income','savings']
#expense
class ExpenseForm(forms.ModelForm):
    class Meta:
        model =  Expense
        fields = ['category','amount','description','date','receipt']

#debt
class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['type','amount','due_date','is_paid']

#mood

class MoodLogForm(forms.ModelForm):
    class Meta:
        model = MoodLog
        fields = ['mood','note']

#ai
class AIAdviceForm(forms.ModelForm):
    class Meta:
        model = AIAdvice
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ask your financial question...'
            })
        }        


#pass change
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    