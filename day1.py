transactions = [
    {"id": 1, "amount": 250.00, "status": "success", "merchant": "Walmart"},
    {"id": 2, "amount": 15200.00, "status": "failed", "merchant": "Amazon"},
    {"id": 3, "amount": 9800.00, "status": "success", "merchant": "Target"},
    {"id": 4, "amount": 430.00, "status": "success", "merchant": "Walmart"},
    {"id": 5, "amount": 11000.00, "status": "failed", "merchant": "BestBuy"},
]

# Task 1: Print all failed transactions
for transaction in transactions:
    if transaction["status"] == "failed":
        print(transaction)
# Task 2: Print total amount of successful transactions
total_success = sum(t["amount"] for t in transactions if t["status"] == "success")
print(f"Total amount of successful transactions: ${total_success:.2f}")
# Task 3: Flag any transaction over $10,000 as "high risk"
for transaction in transactions:
    if transaction["amount"] > 10000:
        risk_flag = {**transaction, "risk_level": "HIGH RISK"}
        print(f"Transaction {risk_flag['id']} - {risk_flag['merchant']} - ${risk_flag['amount']} - {risk_flag['risk_level']}")