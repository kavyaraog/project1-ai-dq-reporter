# Project 1 - AI Assisted Data Quality Reporter
# Concepts learned:
# - Returning structured data (dictionary) from a function
# - json.dumps() to convert dict to string
# - Calling the Claude API with anthropic library
# - Prompt engineering - giving Claude context + data
# - Writing AI output to a file
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import json
import anthropic
import markdown

# --- Sample fintech transaction data ---
data = {
    "transaction_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "amount": [250.00, 15200.00, None, 9800.00, 11000.00, 430.00, None, 5600.00, 22000.00, 310.00],
    "status": ["success", "failed", "success", "success", "failed", "success", "failed", "success", "success", None],
    "merchant": ["Walmart", "Amazon", "Target", "Walmart", "BestBuy", "Amazon", "Target", None, "Walmart", "BestBuy"],
    "date": ["2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03", "2024-01-04", "2024-01-04", "2024-01-05", "2024-01-05", "2024-01-06"]
}

df = pd.DataFrame(data)


# --- Step 1: Run DQ checks and RETURN a findings dictionary ---
def run_dq_checks(df):
    # Empty dictionary - we fill this as we run each check
    findings = {}

    # Completeness
    total = len(df)                          # total row count
    complete = df.dropna().shape[0]          # rows with zero nulls
    findings["completeness_pct"] = round((complete / total) * 100, 1)
    findings["incomplete_records"] = total - complete

    # Null counts per column
    nulls = df.isnull().sum()                # count nulls in each column
    nulls = nulls[nulls > 0]                 # keep only columns that have nulls
    findings["null_counts"] = nulls.to_dict()
    # .to_dict() converts pandas Series → plain Python dict
    # example: {"amount": 2, "status": 1, "merchant": 1}

    # High value transactions
    high_value = df[df["amount"] > 20000]
    findings["high_value_count"] = len(high_value)
    findings["high_value_transactions"] = high_value[["transaction_id", "amount", "merchant"]].to_dict(orient="records")
    # orient="records" converts each row into a dict
    # example: [{"transaction_id": 9, "amount": 22000.0, "merchant": "Walmart"}]

    # Duplicates
    dupes = df[df.duplicated(subset=["transaction_id"])]
    findings["duplicate_count"] = len(dupes)

    # Invalid amounts
    invalid = df[df["amount"] <= 0]
    findings["invalid_amount_count"] = len(invalid)

    return findings
    # return hands the findings dict back to whoever called this function


# --- Step 2: Send findings to Claude API and get plain-English report ---
def generate_ai_report(findings):
    # Convert the findings dictionary to a JSON string
    # Claude receives text, not Python objects - this is the bridge
    findings_str = json.dumps(findings, indent=2)

    # Build the prompt - this is prompt engineering
    # We give Claude: role, context, data, and exact instructions
    prompt = f"""You are a senior data quality engineer reviewing a fintech transaction dataset.

Here are the data quality findings from an automated pipeline check:

{findings_str}

Write a plain-English data quality report that includes:
1. An executive summary (2-3 sentences on overall data health)
2. Issues found - for each issue: severity (HIGH / MEDIUM / LOW), what it means, and likely cause
3. Recommended actions the data engineering team should take

Be specific, concise, and use fintech domain language. This report will be read by both engineers and business stakeholders."""

    # Initialize the Anthropic client
    # It automatically reads ANTHROPIC_API_KEY from your .env or environment
    client = anthropic.Anthropic()

    # Call the Claude API
    message = client.messages.create(
        model="claude-opus-4-6",         # model to use
        max_tokens=1024,                  # max length of response
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # message.content is a list of content blocks
    # [0] gets the first block, .text gets the text string
    return message.content[0].text


# --- Step 3: Run everything and save the report ---

# Capture the returned dictionary - this is what we practiced
findings = run_dq_checks(df)

# Print findings so you can see what we're sending to Claude
print("=" * 40)
print("FINDINGS BEING SENT TO CLAUDE:")
print("=" * 40)
print(json.dumps(findings, indent=2))

# Call Claude and get the AI-generated report
print("\n" + "=" * 40)
print("GENERATING AI REPORT...")
print("=" * 40)
ai_report = generate_ai_report(findings)

# Print to console
print(ai_report)

# Save to file
with open("dq_report.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>DQ Report</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        h1, h2, h3 { color: #2c3e50; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
""")
    f.write(markdown.markdown(ai_report, extensions=["tables"]))
    f.write("\n</body></html>")

print("\n✅ Report saved to dq_report.txt")
