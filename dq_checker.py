import pandas as pd

df = pd.read_csv("transactions.csv")
print(df)

def run_dq_checks(df, filename):
    print("=" * 40)
    print(f"DATA QUALITY REPORT: {filename}")
    print("=" * 40)

    # 1. Shape of the data
    rows, cols = df.shape
    print(f"\n📊 Dataset: {rows} rows, {cols} columns")

    # 2. Completeness check
    total = len(df)
    complete = df.dropna().shape[0]
    incomplete = total - complete
    completeness_pct = (complete / total) * 100
    print(f"\n✅ Completeness: {completeness_pct:.1f}%")
    print(f"   {incomplete} incomplete records found")

    # 3. Null counts per column
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        print(f"\n⚠️  Null Counts:")
        for col, count in nulls.items():
            print(f"   {col}: {count} nulls")
    else:
        print(f"\n✅ No nulls found in any column")

    # 4. High value transaction check
    high_value_threshold = 20000
    high_value = df[df["amount"] > high_value_threshold]
    print(f"\n🚨 High Value Transactions (>${high_value_threshold:,}): {len(high_value)}")
    if not high_value.empty:
        for _, row in high_value.iterrows():
            print(f"   Transaction {row['transaction_id']} - {row['merchant']} - ${row['amount']:,.2f}")
    else:
        print(f"   None found")

    # 5. Duplicate transaction IDs
    dupes = df[df.duplicated(subset=["transaction_id"])]
    print(f"\n🔁 Duplicate Transaction IDs: {len(dupes)}")
    if not dupes.empty:
        for _, row in dupes.iterrows():
            print(f"   Transaction {row['transaction_id']}")
    else:
        print(f"   None found")

    # 6. Invalid amounts
    invalid = df[df["amount"] <= 0]
    print(f"\n❌ Invalid Amounts (zero or negative): {len(invalid)}")
    if not invalid.empty:
        for _, row in invalid.iterrows():
            print(f"   Transaction {row['transaction_id']} - ${row['amount']:,.2f}")
    else:
        print(f"   None found")

    print("\n" + "=" * 40)
    print("END OF REPORT")
    print("=" * 40)

run_dq_checks(df, "transactions.csv")   