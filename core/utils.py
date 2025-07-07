import openai
from django.conf import settings

def call_openai_function(question, user, monthly_expenses, total_debt):
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""
    User's Financial Overview:
    - Monthly Income: ₹{user.userprofile.income}
    - Current Savings: ₹{user.userprofile.savings}
    - Monthly Expenses: ₹{monthly_expenses}
    - Total Debt: ₹{total_debt}

    Question: {question}

    Give a helpful financial suggestion or insight.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial advisor bot."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error fetching response: {e}"
