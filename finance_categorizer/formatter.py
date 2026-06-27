"""
Format transactions from xlsx into categorized daily table.

Usage:
    python3 -m finance_categorizer.formatter [start_day]

Copies result to clipboard (macOS).
"""

import calendar
import subprocess
import sys

import pandas as pd

from finance_categorizer.categories import (
    GROCERY, CAR_FUEL, RESTAURANTS, DEVELOPMENT, GIFT, CLOTHES,
    EXCLUDE_KEYWORDS, EXCLUDE_AMOUNTS, EXCLUDE_KEYWORD_AMOUNT, EXCLUDE_ACCOUNTS
)

XLSX_PATH = '/Users/apochynok/Downloads/1.xlsx'
COLS = ['Grocery', 'Car&Fuel', 'Rest', 'Other', 'Clothes', 'Development', 'Gift']


def categorize(description):
    desc = description.lower()
    if any(k in desc for k in GROCERY): return 'Grocery'
    if any(k in desc for k in CAR_FUEL): return 'Car&Fuel'
    if any(k in desc for k in RESTAURANTS): return 'Rest'
    if any(k in desc for k in DEVELOPMENT): return 'Development'
    if any(k in desc for k in GIFT): return 'Gift'
    if any(k in desc for k in CLOTHES): return 'Clothes'
    return 'Other'


def make_formula(amounts):
    amounts = [a for a in amounts if a != 0]
    if not amounts:
        return ''
    if len(amounts) == 1:
        return str(amounts[0]).replace('.', ',')
    return '=' + '+'.join(str(a).replace('.', ',') for a in amounts)


def main():
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
    start_day = 1
    for arg in sys.argv[1:]:
        if arg.isdigit() and 1 <= int(arg) <= 31:
            start_day = int(arg)
            break

    start_date = last_date.replace(day=start_day)
    end_date = last_date.replace(day=calendar.monthrange(last_date.year, last_date.month)[1])
    df = df[df['Date'] >= start_date]
    date_range = pd.date_range(start_date, end_date, freq='D').date

    pivot = df.groupby(['Date', 'Category'])['Amount'].apply(make_formula).unstack(fill_value='')
    pivot = pivot.reindex(date_range, fill_value='')
    for col in COLS:
        if col not in pivot.columns:
            pivot[col] = ''
    pivot = pivot[COLS]
    result = pivot.to_csv(sep='\t', index=False)

    # Display with day numbers
    display_pivot = pivot.copy()
    display_pivot.insert(0, 'Day', [d.day for d in display_pivot.index])
    print(display_pivot.to_csv(sep='\t', index=False))

    data_without_header = '\n'.join(result.split('\n')[1:])
    subprocess.run('pbcopy', input=data_without_header.encode(), check=True)
    print('\n✅ Copied to clipboard!')


if __name__ == "__main__":
    main()
