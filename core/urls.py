from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('expenses/', views.expense_list_view, name='expenses'),
    path('expenses/edit/<int:id>/', views.edit_expense_view, name='edit_expense'),
    path('expenses/delete/<int:id>/', views.delete_expense_view, name='delete_expense'),

    path('debts/', views.debt_list_view, name='debts'),
    path('debts/edit/<int:id>/', views.edit_debt_view, name='edit_debt'),
    path('debts/delete/<int:id>/', views.delete_debt_view, name='delete_debt'),

    path('mood-tracker/', views.mood_tracker_view, name='mood_tracker'),
    path('mood-tracker/edit/<int:id>/', views.edit_mood_view, name='edit_mood'),
    path('mood-tracker/delete/<int:id>/', views.delete_mood_view, name='delete_mood'),

    path('ai-advisor/', views.ai_advisor_view, name='ai_advisor'),
    path('ai-advisor/delete/<int:id>/', views.delete_advice_view, name='delete_advice'),

    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('delete-account/', views.delete_expense_view, name='delete_account'),
]
