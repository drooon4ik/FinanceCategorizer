GROCERY = ['lidl', 'rossmann', 'juhas grzegorzek', 'auchan']
CAR_FUEL = ['orlen', 'stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'balice manual']
HOBBY_SPORT = ['hotel', 'booking', 'ryanair']
RESTAURANTS = ['mcdonalds', 'lunch']
DEVELOPMENT = ['time building', 'licencji']
GIFT = ['kwiatów', 'birthday']

# Filters to exclude transactions
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy', 'money transfer']
EXCLUDE_AMOUNTS = [270.6]  # Tax amounts to filter out
EXCLUDE_KEYWORD_AMOUNT = [('oplata z', 131.85)]  # (keyword, amount) pairs to filter
