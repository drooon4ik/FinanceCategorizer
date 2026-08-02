"""
Show detailed transactions for a specific day and/or category.

Usage:
    python3 -m finance_categorizer.detail 15
    python3 -m finance_categorizer.detail Grocery
    python3 -m finance_categorizer.detail 15 Grocery
    python3 -m finance_categorizer.detail -p          # previous month
    python3 -m finance_categorizer.detail -p Grocery  # previous month, category
"""

import subprocess
import sys
from datetime import date, timedelta

import pandas as pd

from finance_categorizer.categories import (
    CATEGORY_RULES, COLS,
    EXCLUDE_KEYWORDS, EXCLUDE_AMOUNTS, EXCLUDE_KEYWORD_AMOUNT, EXCLUDE_ACCOUNTS
)

XLSX_PATH = '/Users/apochynok/Downloads/1.xlsx'
CATEGORIES = COLS


def categorize(description, odbiorca, amount):
    desc = description.lower()
    odb = str(odbiorca).lower() if pd.notna(odbiorca) else ''
    for category, rules in CATEGORY_RULES:
        for rule in rules:
            if isinstance(rule, tuple):
                keyword, rule_amount = rule
                if (keyword in desc or keyword in odb) and round(amount, 2) == rule_amount:
                    return category
            else:
                if rule in desc:
                    return category
    return 'Other'


def main():
    prev_month = '-p' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    day = None
    category = None
    for a in args:
        if a.isdigit() and 1 <= int(a) <= 31:
            day = int(a)
        elif a in CATEGORIES:
            category = a
        else:
            match = [c for c in CATEGORIES if c.lower() == a.lower()]
            if match:
                category = match[0]
            else:
                print(f"Unknown argument: {a}")
                print(f"Categories: {', '.join(CATEGORIES)}")
                sys.exit(1)

    print(f"📂 Reading: {XLSX_PATH}")
    df = pd.read_excel(XLSX_PATH)
    df = df[~df['Produkt'].str.contains('78160014621736641320000007', na=False)]
    df = df[~df['Odbiorca'].str.contains('|'.join(EXCLUDE_ACCOUNTS), na=False)]
    df = df[~(df['Nadawca'].str.contains('16160014621736641340000001', na=False) & df['Odbiorca'].str.contains('46160014621736641320000001', na=False))]
    df = df.rename(columns={'Data transakcji': 'Date', 'Opis': 'Description', 'Kwota': 'Amount'})
    df['Description'] = df['Description'].str.strip()
    df['Amount'] = pd.to_numeric(df['Amount'])
    df = df[~df['Description'].str.lower().str.contains('|'.join(EXCLUDE_KEYWORDS), na=False)]
    for keyword, amount in EXCLUDE_KEYWORD_AMOUNT:
        matches_keyword = (
            df['Description'].str.lower().str.contains(keyword, na=False) |
            df['Odbiorca'].str.lower().str.contains(keyword, na=False)
        )
        df = df[~(matches_keyword & (df['Amount'].round(2) == -amount))]
    for amount in EXCLUDE_AMOUNTS:
        df = df[df['Amount'].round(2) != -amount]
    df['Amount'] = df['Amount'] * -1
    df['Category'] = df.apply(lambda r: categorize(r['Description'], r['Odbiorca'], r['Amount']), axis=1)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    last_date = df['Date'].max()

    if prev_month:
        # Previous month: first_day is 1st of previous month, last day is end of previous month
        first_of_current = last_date.replace(day=1)
        end_of_prev = first_of_current - timedelta(days=1)
        start_date = end_of_prev.replace(day=1)
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_of_prev)]
    else:
        start_date = last_date.replace(day=1)
        df = df[df['Date'] >= start_date]

    if day:
        if prev_month:
            target_date = start_date.replace(day=day)
        else:
            target_date = last_date.replace(day=day)
        df = df[df['Date'] == target_date]
    if category:
        df = df[df['Category'] == category]

    if df.empty:
        print("No transactions found.")
        return

    df = df.sort_values('Date')
    total = df['Amount'].sum()
    period = "previous month" if prev_month else "current month"
    print(f"📅 Period: {period}")
    print(f"{'Date':<12} {'Amount':>8}  {'Category':<12} Description")
    print("-" * 70)
    lines = []
    for _, r in df.iterrows():
        desc = r['Description'][:80]
        line = f"{r['Date']}  {r['Amount']:>7.2f}  {r['Category']:<12} {desc}"
        print(line)
        lines.append(line)
    print("-" * 70)
    print(f"{'Total:':<12} {total:>7.2f}  ({len(df)} transactions)")

    clipboard_text = '\n'.join(lines)
    subprocess.run('pbcopy', input=clipboard_text.encode(), check=True)
    print('\n✅ Copied to clipboard!')


if __name__ == "__main__":
    main()
