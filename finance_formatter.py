import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from categories import GROCERY, CAR_FUEL, HOBBY_SPORT, RESTAURANTS, DEVELOPMENT, GIFT, EXCLUDE_KEYWORDS, EXCLUDE_AMOUNTS, EXCLUDE_KEYWORD_AMOUNT

def categorize(description):
    desc = description.lower()
    if any(k in desc for k in GROCERY):
        return 'Grocery'
    if any(k in desc for k in CAR_FUEL):
        return 'Car&Fuel'
    if any(k in desc for k in HOBBY_SPORT):
        return 'Hobby/sport/Rest/Entertaiment'
    if any(k in desc for k in RESTAURANTS):
        return 'Restorans'
    if any(k in desc for k in DEVELOPMENT):
        return 'Development'
    if any(k in desc for k in GIFT):
        return 'Gift'
    return 'Other'

df = pd.read_excel('/Users/apochynok/Downloads/1.xlsx')
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
min_date = df['Date'].min()
start_date = min_date.replace(day=1)
date_range = pd.date_range(start_date, df['Date'].max(), freq='D').date

def make_formula(amounts):
    amounts = [a for a in amounts if a != 0]
    if not amounts:
        return ''
    if len(amounts) == 1:
        return str(amounts[0]).replace('.', ',')
    return '=' + '+'.join(str(a).replace('.', ',') for a in amounts)

pivot = df.groupby(['Date', 'Category'])['Amount'].apply(make_formula).unstack(fill_value='')
pivot = pivot.reindex(date_range, fill_value='')
cols = ['Grocery', 'Car&Fuel', 'Hobby/sport/Rest/Entertaiment', 'Restorans', 'Other', 'Clothes', 'Development', 'Gift']
for col in cols:
    if col not in pivot.columns:
        pivot[col] = ''
pivot = pivot[cols]
print(pivot.to_csv(sep='\t', index=False))
