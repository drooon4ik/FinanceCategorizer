GROCERY = ['lidl', 'rossmann', 'juhas grzegorzek', 'auchan', 'przejscie podziemne', 'fh juhas grzego', 'trokos']
CAR_FUEL = ['orlen', 'stacja paliw', 'parkowanie', 'parking', 'strefy platnego', 'brzeczkowice manual', 'auto myjnia', 'balice',  'galeria krakowska park']
RESTAURANTS = ['hotel', 'booking', 'ryanair', 'mcdonalds', 'lunch', 'hala centralna']
DEVELOPMENT = ['time building', 'licencji']
GIFT = ['kwiatów', 'birthday', 'monika urban czarokwia']
CLOTHES = ['peek cloppenburg', 'reserved']

# Filters to exclude transactions
EXCLUDE_KEYWORDS = ['pit-', 'urząd skarbowy', 'podatkowy', 'money transfer']
EXCLUDE_AMOUNTS = [270.6]  # Tax amounts to filter out
EXCLUDE_KEYWORD_AMOUNT = [('oplata z', 131.85)]  # (keyword, amount) pairs to filter
