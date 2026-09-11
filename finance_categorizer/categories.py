import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

GROCERY = ['lidl', 'rossmann', 'juhas grzegorzek', 'auchan', 'przejscie podziemne', 'fh juhas grzego', 'trokos', 'kaufland', 'ukrainski smak', 'biedronka', 'biedro', 'carrefour', 'firma uslugowo-', 'wars automat vendingow', 'dino leszcze', 'hebe r pol', 'chelbo kawiarni', 'best market krakow']
CAR_FUEL = ['orlen', 'stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'auto myjnia', 'balice', 'galeria krakowska park', 'bolt', 'automyjnia venu', '/opt/x///// xx5601228913xx', 'mol sf803 k.3 kalinowa pl 51687', 'car park', 'jakdojade.pl', 'brzeczkowice  brzeczkowice pl', '/opt/x///// xx5629326976xx']
RESTAURANTS = ['mcdonalds', 'lunch', 'pastrami summer bbq', 'meatfellas', 'zalipianki', 'mercy brown', 'pijana wisnia', 'kebab', 'hankki', 'indain flame', 'restauracja', 'bilard', 'rimi food', 'nova klubowa', 'czeskie piwo sklep', 'my viet nam', 'pinczow camprest gacki', 'multikino', 'tommys pol', 'blik phone transfer', 'vilnius globaltips', 'kra saun pos']
DEVELOPMENT = ['time building', 'licencji', 'perfect line', 'noblewings', 'exam for', 'licence issue', 'michal skowronski', 'xtremefitn', ('w unicreditpl-inpost mob', 14.49), '/opt/x///// xx5633333406xx', '/opt/iu/bpid:a4ap7suypj///', 'zamówienie 9172661950', 'rezerwacja kortu']
GIFT = ['kwiatów', 'birthday', 'monika urban czarokwia']
CLOTHES = ['cloppenburg', 'reserved']
#internet, youtube, mobile
SUBSCRIPTIONS = [('pastelowa 8 60-198 poznan', 101.40), ('apple.com', 38.99), 'orange flex', 'miesieczna oplata za obsluge karty']

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
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy', 'dublin revolut']
EXCLUDE_ACCOUNTS = [os.environ["EXCLUDE_ACCOUNT"]]
EXCLUDE_AMOUNTS = []
EXCLUDE_KEYWORD_AMOUNT = [('depozyt', 3690.00),  ('to personal account', 94700)]
