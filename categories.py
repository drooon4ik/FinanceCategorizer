GROCERY = ['lidl', 'rossmann', 'juhas grzegorzek', 'auchan', 'przejscie podziemne', 'fh juhas grzego', 'trokos', 'kaufland', 'ukrainski smak', 'biedronka', 'biedro']
CAR_FUEL = ['orlen', 'stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'auto myjnia', 'balice',  'galeria krakowska park', 'bolt']
RESTAURANTS = ['hotel', 'booking', 'airbnb', 'ryanair', 'mcdonalds', 'lunch', 'hala centralna', 'foreflight', 'skydemon', 'pastrami summer bbq', 'meatfellas', 'zalipianki', 'mercy brown']
DEVELOPMENT = ['time building', 'licencji', 'perfect line', 'noblewings']
GIFT = ['kwiatów', 'birthday', 'monika urban czarokwia']
CLOTHES = ['peek cloppenburg', 'reserved']

# Filters to exclude transactions
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy']
EXCLUDE_ACCOUNTS = ['77105014451000009145254786']
EXCLUDE_AMOUNTS = [270.6]  # Tax amounts to filter out
EXCLUDE_KEYWORD_AMOUNT = [('oplata z', 131.85)]  # (keyword, amount) pairs to filter
