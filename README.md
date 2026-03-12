# AI-Assisted Data Quality Reporter

An automated data quality pipeline for fintech transaction data, powered by Claude AI.

## What it does
- Runs automated DQ checks on transaction datasets using pandas
- Detects nulls, duplicates, invalid amounts, and high-value anomalies
- Sends structured findings to Claude API
- Generates a plain-English report with severity ratings, root cause analysis, and recommended actions
- Saves output as a rendered HTML report

## Tech Stack
- Python 3.x
- pandas
- Anthropic Claude API
- markdown

## How to run

1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt
3. Create a .env file in the root folder:
   ANTHROPIC_API_KEY=your_key_here
4. Run:
   python project1_ai_dq_reporter.py
5. Open dq_report.html in your browser

## Sample Output
The generated report includes:
- Executive summary of data health
- Per-issue breakdown with severity (HIGH / MEDIUM / LOW)
- Likely root causes using fintech domain language
- Recommended actions for the data engineering team

## Domain Context
Built with fintech transaction data patterns in mind — covers settlement gaps,
AML/BSA considerations, merchant attribution failures, and ingestion-layer anomalies.
```

