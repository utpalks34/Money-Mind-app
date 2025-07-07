from django.db import models
from django.contrib.auth.models import User
# django user with financial data 
class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     income =models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
     savings = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     

     def __str__(self):
        return f"{self.user.username}'s Profile"

#expenses by categories
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food','Food'),
        ('rent','rent'),
        ('travel','Travel'),
        ('medical','Medical'),
        ('utilities','Utilities'),
        ('other','Other'),

    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length= 50,choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField()
    receipt = models.FileField(upload_to='receipts/',blank = True,null = True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
      return f"{self.category} - ₹{self.amount}"
    


#track debts 
class Debt(models.Model):
    DEBT_TYPE_CHOICES = [
        ('loan', 'Loan'),
        ('emi', 'EMI'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=DEBT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} - ₹{self.amount}"



#mood
class MoodLog(models.Model):
    MOOD_CHOICES = [
      
      ('happy','Happy'),
      ('stressed','Stressed'),
      ('anxious','Anxious')
    ]

            
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mood = models.CharField(max_length=20,choices = MOOD_CHOICES)
    note = models.TextField(blank = True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -{self.mood} ({self.date})"
    
#ai interaction
class AIAdvice(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advice for {self.user.username} on {self.created_at.date()}"    