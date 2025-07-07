from django.contrib import admin

# Register your models here.
from django.contrib import admin 
from .models import UserProfile, Expense, Debt, MoodLog, AIAdvice


admin.site.register(UserProfile)
admin.site.register(Expense)
admin.site.register(Debt)
admin.site.register(MoodLog)
admin.site.register(AIAdvice)