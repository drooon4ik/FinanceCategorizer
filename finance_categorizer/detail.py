"""
Show detailed transactions for a specific day and/or category.

Usage:
    python3 -m finance_categorizer.detail 15
    python3 -m finance_categorizer.detail Grocery
    python3 -m finance_categorizer.detail 15 Grocery
"""

import sys

import pandas as pd

from finance_categorizer.categories import (
    GROCERY, CAR_FUEL, RESTAURANTS, DEVELOPMENT, GIFT, CLOTHES,
    EXCLUDE_KEYWORDS, EXCLUDE_AMOUNTS, EXCLUDE_KEYWORD_AMOUNT, EXCLUDE_ACCOUNTS
)

XLSX_PATH = '/Users/apochynok/Downloads/1.xlsx'
CATEGORIES = ['Grocery', 'Car&Fuel', 'Rest', 'Other', 'Clothes', 'Development', 'Gift']


def categorize(description):
    desc = description.lower()
    if any(k in desc for k in GROCERY): return 'Grocery'
    if any(k in desc for k in CAR_FUEL): return 'Car&Fuel'
    if any(k in desc for k in RESTAURANTS): return 'Rest'
    if any(k in desc for k in DEVELOPMENT): return 'Development'
    if any(k in desc for k in GIFT): return 'Gift'
    if any(k in desc for k in CLOTHES): return 'Clothes'
    return 'Other'


def main():
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
        df = df[~((df['Description'].str.lower().str.contains(keyword, na=False)) & (df['Amount'].round(2) == -amount))]
    for amount in EXCLUDE_AMOUNTS:
        df = df[df['Amount'].round(2) != -amount]
    df['Amount'] = df['Amount'] * -1
    df['Category'] = df['Description'].apply(categorize)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    last_date = df['Date'].max()
    start_date = last_date.replace(day=1)
    df = df[df['Date'] >= start_date]

    if day:
        target_date = last_date.replace(day=day)
        df = df[df['Date'] == target_date]
    if category:
        df = df[df['Category'] == category]

    if df.empty:
        print("No transactions found.")
        return

    df = df.sort_values('Date')
    total = df['Amount'].sum()
    print(f"{'Date':<12} {'Amount':>8}  {'Category':<12} Description")
    print("-" * 70)
    for _, r in df.iterrows():
        desc = r['Description'][:80]
        print(f"{r['Date']}  {r['Amount']:>7.2f}  {r['Category']:<12} {desc}")
    print("-" * 70)
    print(f"{'Total:':<12} {total:>7.2f}  ({len(df)} transactions)")


if __name__ == "__main__":
    main()
