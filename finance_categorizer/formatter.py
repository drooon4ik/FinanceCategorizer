"""
Format transactions from xlsx into categorized daily table.

Usage:
    python3 -m finance_categorizer.formatter [start_day]
    python3 -m finance_categorizer.formatter -p          # previous month

Copies result to clipboard (macOS).
"""

import calendar
import subprocess
import sys
from datetime import timedelta

import pandas as pd

from finance_categorizer.categories import (
    CATEGORY_RULES, COLS,
    EXCLUDE_KEYWORDS, EXCLUDE_AMOUNTS, EXCLUDE_KEYWORD_AMOUNT, EXCLUDE_ACCOUNTS
)
from finance_categorizer.temp_rules import get_category_rules, get_ignore_rules

XLSX_PATH = '/Users/apochynok/Downloads/1.xlsx'


def categorize(description, odbiorca, amount):
    desc = description.lower()
    odb = str(odbiorca).lower() if pd.notna(odbiorca) else ''
    all_rules = get_category_rules() + CATEGORY_RULES
    for category, rules in all_rules:
        for rule in rules:
            if isinstance(rule, tuple):
                keyword, rule_amount = rule
                if (keyword in desc or keyword in odb) and round(amount, 2) == rule_amount:
                    return category
            else:
                if rule in desc:
                    return category
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
        matches_keyword = (
            df['Description'].str.lower().str.contains(keyword, na=False) |
            df['Odbiorca'].str.lower().str.contains(keyword, na=False)
        )
        df = df[~(matches_keyword & (df['Amount'].round(2) == -amount))]
    for amount in EXCLUDE_AMOUNTS:
        df = df[df['Amount'].round(2) != -amount]
    # Apply temp ignore rules
    for rule in get_ignore_rules():
        keyword = rule["keyword"]
        matches_keyword = (
            df['Description'].str.lower().str.contains(keyword, na=False) |
            df['Odbiorca'].str.lower().str.contains(keyword, na=False)
        )
        if "amount" in rule:
            df = df[~(matches_keyword & (df['Amount'].round(2) == -rule["amount"]))]
        else:
            df = df[~matches_keyword]
    df['Amount'] = df['Amount'] * -1
    df['Category'] = df.apply(lambda r: categorize(r['Description'], r['Odbiorca'], r['Amount']), axis=1)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    last_date = df['Date'].max()
    prev_month = '-p' in sys.argv
    start_day = 1
    for arg in sys.argv[1:]:
        if arg.isdigit() and 1 <= int(arg) <= 31:
            start_day = int(arg)
            break

    if prev_month:
        first_of_current = last_date.replace(day=1)
        end_of_prev = first_of_current - timedelta(days=1)
        start_date = end_of_prev.replace(day=start_day)
        end_date = end_of_prev
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    else:
        start_date = last_date.replace(day=start_day)
        end_date = last_date
        df = df[df['Date'] >= start_date]
    date_range = pd.date_range(start_date, end_date, freq='D').date

    pivot = df.groupby(['Date', 'Category'])['Amount'].apply(make_formula).unstack(fill_value='')
    pivot = pivot.reindex(date_range, fill_value='')
    for col in COLS:
        if col not in pivot.columns:
            pivot[col] = ''
    pivot = pivot[COLS]
    result = pivot.to_csv(sep='\t', index=False)

    # Display with day numbers, aligned columns
    display_pivot = pivot.copy()
    display_pivot.insert(0, 'Day', [d.day for d in display_pivot.index])
    col_widths = {col: max(len(col), display_pivot[col].astype(str).str.len().max()) for col in display_pivot.columns}
    header = '  '.join(col.ljust(col_widths[col]) for col in display_pivot.columns)
    print(header)
    for _, row in display_pivot.iterrows():
        line = '  '.join(str(row[col]).ljust(col_widths[col]) for col in display_pivot.columns)
        print(line)

    data_without_header = '\n'.join(result.split('\n')[1:])
    subprocess.run('pbcopy', input=data_without_header.encode(), check=True)
    print('\n✅ Copied to clipboard!')


if __name__ == "__main__":
    main()
