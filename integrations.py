import requests
import random

class IntegrationLayer:
    def __init__(self):
        pass

    def get_weather(self, city: str):
        # Mock weather data
        conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Clear"]
        temp = random.randint(15, 35)
        return {
            "city": city,
            "temperature": f"{temp}°C",
            "condition": random.choice(conditions)
        }

    def process_payment(self, amount: float, currency: str = "USD"):
        # Mock payment processing
        tx_id = f"TXN_{random.randint(100000, 999999)}"
        return {
            "status": "success",
            "transaction_id": tx_id,
            "amount": amount,
            "currency": currency,
            "message": "Payment processed successfully via KAIN Payment Gateway"
        }

integrations = IntegrationLayer()
