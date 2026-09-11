"""
Add a keyword to a category (stored as temporary rule).

Usage:
    finance -e "keyword" Category
    finance -e "keyword" 5.00 Category
"""

import sys

from finance_categorizer.categories import CATEGORY_RULES
from finance_categorizer.temp_rules import add

CATEGORIES = [cat for cat, _ in CATEGORY_RULES]


def main():
    args = sys.argv[1:]

    if len(args) < 2 or len(args) > 3:
        print('Usage: finance -e "keyword" Category')
        print('       finance -e "keyword" 5.00 Category')
        print(f"Categories: {', '.join(CATEGORIES)}")
        sys.exit(1)

    keyword = args[0].lower().strip()

    # Parse: "keyword" amount Category  OR  "keyword" Category
    if len(args) == 3:
        try:
            amount = float(args[1])
        except ValueError:
            print(f"❌ Invalid amount: {args[1]}")
            sys.exit(1)
        category_input = args[2]
    else:
        amount = None
        category_input = args[1]

    # Match category (case-insensitive)
    match = {c.lower(): c for c in CATEGORIES}
    if category_input.lower() not in match:
        print(f"❌ Unknown category: {category_input}")
        print(f"Available: {', '.join(CATEGORIES)}")
        sys.exit(1)
    category = match[category_input.lower()]

    ok, msg = add(keyword, category, amount)
    if ok:
        if amount is not None:
            print(f"✅ Added '{keyword}' ({amount}) → {category} [temp]")
        else:
            print(f"✅ Added '{keyword}' → {category} [temp]")
    else:
        print(f"❌ {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
