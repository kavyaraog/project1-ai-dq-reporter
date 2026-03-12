# Day 1 - Pandas Data Quality Checks
# Concepts learned:
# - Creating a DataFrame from a dictionary
# - df.shape, df.dtypes, df.isnull().sum()
# - Filtering rows with conditions
# - Writing reusable functions
# - F-strings for formatted output
# - Building a DQ report from scratch

import pandas as pd

data = {
    "transaction_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "amount": [250.00, 15200.00, None, 9800.00, 11000.00, 430.00, None, 5600.00, 22000.00, 310.00],
    "status": ["success", "failed", "success", "success", "failed", "success", "failed", "success", "success", None],
    "merchant": ["Walmart", "Amazon", "Target", "Walmart", "BestBuy", "Amazon", "Target", None, "Walmart", "BestBuy"],
    "date": ["2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03", "2024-01-04", "2024-01-04", "2024-01-05", "2024-01-05", "2024-01-06"]
}

df = pd.DataFrame(data)

def run_dq_checks(df):
    print("=" * 40)
    print("DATA QUALITY REPORT")
    print("=" * 40)

    # Completeness
    total = len(df)
    complete = df.dropna().shape[0]
    print(f"\n✅ Completeness: {(complete/total)*100:.1f}%")
    print(f"   {total - complete} incomplete records found")

    # Null detail
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        print(f"\n⚠️  Null Counts:")
        for col, count in nulls.items():
            print(f"   {col}: {count} nulls")

    # High value transactions
    high_value = df[df["amount"] > 20000]
    print(f"\n🚨 High Value Transactions (>$20,000): {len(high_value)}")
    if not high_value.empty:
        for _, row in high_value.iterrows():
            print(f"   Transaction {row['transaction_id']} - {row['merchant']} - ${row['amount']}")

    # Duplicates
    dupes = df[df.duplicated(subset=["transaction_id"])]
    print(f"\n🔁 Duplicate IDs: {len(dupes)}")

    # Invalid amounts
    invalid = df[df["amount"] <= 0]
    print(f"\n❌ Invalid Amounts: {len(invalid)}")

    print("\n" + "=" * 40)
    print("END OF REPORT")
    print("=" * 40)

run_dq_checks(df)