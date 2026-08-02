import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

GROCERY = ['lidl', 'rossmann', 'juhas grzegorzek', 'auchan', 'przejscie podziemne', 'fh juhas grzego', 'trokos', 'kaufland', 'ukrainski smak', 'biedronka', 'biedro', 'carrefour', 'firma uslugowo-']
CAR_FUEL = ['orlen', 'stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'auto myjnia', 'balice', 'galeria krakowska park', 'bolt', 'automyjnia venu']
RESTAURANTS = ['mcdonalds', 'lunch', 'pastrami summer bbq', 'meatfellas', 'zalipianki', 'mercy brown', 'pijana wisnia', 'kebab', 'hankki', 'indain flame', 'restauracja', 'bilard', 'rimi food', 'nova klubowa', 'czeskie piwo sklep', 'my viet nam']
DEVELOPMENT = ['time building', 'licencji', 'perfect line', 'noblewings', 'exam for', 'licence issue', 'michal skowronski', 'xtremefitn']
GIFT = ['kwiatów', 'birthday', 'monika urban czarokwia']
CLOTHES = ['cloppenburg', 'reserved']
#internet, youtube, mobile
SUBSCRIPTIONS = [('apple.combill irl 38.99 pln', 38.99), 'orange flex']

# Ordered list of (category_name, rules).
# Each rule is either a string (keyword match) or a tuple (keyword, amount).
CATEGORY_RULES = [
    ('Grocery', GROCERY),
    ('Car&Fuel', CAR_FUEL),
    ('Hobby/Rest/Entertainment', RESTAURANTS),
    ('Clothes', CLOTHES),
    ('Development/Sport', DEVELOPMENT),
    ('Gift', GIFT),
    ('Subscriptions', SUBSCRIPTIONS),
]

# Column order for output (Other is the default category for unmatched transactions)
COLS = ['Grocery', 'Car&Fuel', 'Hobby/Rest/Entertainment', 'Other', 'Clothes', 'Development/Sport', 'Gift', 'Subscriptions']

# Filters to exclude transactions
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy']
EXCLUDE_ACCOUNTS = [os.environ["EXCLUDE_ACCOUNT"]]
EXCLUDE_AMOUNTS = []
EXCLUDE_KEYWORD_AMOUNT = [('pastelowa 8 60-198 poznan', 101.40)]
