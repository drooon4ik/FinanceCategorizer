GROCERY = ['lidl', 'rossmann', 'allegro']
CAR_FUEL = ['stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'balice manual']
HOBBY_SPORT = ['hotel', 'booking', 'ryanair']
RESTAURANTS = ['mcdonalds', 'lunch']
DEVELOPMENT = ['time building', 'licencji', 'apple.com']
GIFT = ['kwiatów', 'birthday']

# Filters to exclude transactions
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy', 'money transfer']
EXCLUDE_AMOUNTS = [270.6]  # Tax amounts to filter out
EXCLUDE_KEYWORD_AMOUNT = [('oplata z', 131.85)]  # (keyword, amount) pairs to filter
