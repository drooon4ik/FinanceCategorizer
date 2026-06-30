import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

GROCERY = ['lidl', 'rossmann', 'juhas grzegorzek', 'auchan', 'przejscie podziemne', 'fh juhas grzego', 'trokos', 'kaufland', 'ukrainski smak', 'biedronka', 'biedro', 'carrefour']
CAR_FUEL = ['orlen', 'stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'auto myjnia', 'balice', 'galeria krakowska park', 'bolt']
RESTAURANTS = ['mcdonalds', 'lunch', 'pastrami summer bbq', 'meatfellas', 'zalipianki', 'mercy brown', 'pijana wisnia', 'kebab', 'hankki', 'indain flame', 'restauracja', 'bilard', 'rimi food']
DEVELOPMENT = ['time building', 'licencji', 'perfect line', 'noblewings', 'exam for', 'licence issue', 'michal skowronski']
GIFT = ['kwiatów', 'birthday', 'monika urban czarokwia']
CLOTHES = ['cloppenburg', 'reserved']

# Filters to exclude transactions
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy', 'orange flex']
EXCLUDE_ACCOUNTS = [os.environ["EXCLUDE_ACCOUNT"]]
EXCLUDE_AMOUNTS = [270.6]
EXCLUDE_KEYWORD_AMOUNT = []
