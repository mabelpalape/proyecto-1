import random

def generate_explanation(customer_id, product_name, days_until_due, confidence, window):
    # In a real system, this would call Gemini.
    # For MVP without valid API key loop, we mock it or prepare the prompt.
    
    # Prompt Design as requested:
    # "Explanation prompt must include: last_purchase_date, consumption_cycle, recency..."
    
    base_reasons = [
        f"Customer usually buys {product_name} every few weeks.",
        f"Based on purchase history, {product_name} should be running low.",
        f"High frequency shopper for {product_name}. Good time to restock."
    ]
    
    reason = random.choice(base_reasons)
    
    if window == "Early Reminder":
        return f"Proactive: {reason} Expected need in {days_until_due} days."
    elif window == "Follow-up (Late)":
        return f"Missed Cycle: {reason} They are {abs(days_until_due)} days overdue."
    else:
        return f"Routine: {reason} Confidence is {confidence}."
