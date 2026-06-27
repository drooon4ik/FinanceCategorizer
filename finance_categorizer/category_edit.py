"""
Add a keyword to a category.

Usage:
    python3 -m finance_categorizer.category_edit "keyword" Category
"""

import re
import sys
from pathlib import Path

CATEGORIES_FILE = Path(__file__).parent / "categories.py"

CATEGORY_TO_VAR = {
    'Grocery': 'GROCERY',
    'Car&Fuel': 'CAR_FUEL',
    'Rest': 'RESTAURANTS',
    'Development': 'DEVELOPMENT',
    'Gift': 'GIFT',
    'Clothes': 'CLOTHES',
}


def main():
    if len(sys.argv) != 3:
        print('Usage: financee "keyword" Category')
        print(f"Categories: {', '.join(CATEGORY_TO_VAR.keys())}")
        sys.exit(1)

    keyword = sys.argv[1].lower().strip()
    category = sys.argv[2]

    match = {k.lower(): k for k in CATEGORY_TO_VAR}
    if category.lower() not in match:
        print(f"❌ Unknown category: {category}")
        print(f"Available: {', '.join(CATEGORY_TO_VAR.keys())}")
        sys.exit(1)
    category = match[category.lower()]
    var_name = CATEGORY_TO_VAR[category]

    content = CATEGORIES_FILE.read_text()

    pattern = rf"^({var_name}\s*=\s*\[)(.*)(\])$"
    m = re.search(pattern, content, re.MULTILINE)
    if not m:
        print(f"❌ Could not find {var_name} in {CATEGORIES_FILE.name}")
        sys.exit(1)

    existing = [s.strip().strip("'\"") for s in m.group(2).split(',') if s.strip()]
    if keyword in existing:
        print(f"❌ '{keyword}' already exists in {category}")
        sys.exit(1)

    existing.append(keyword)
    new_list = ', '.join(f"'{k}'" for k in existing)
    new_line = f"{var_name} = [{new_list}]"
    content = content[:m.start()] + new_line + content[m.end():]
    CATEGORIES_FILE.write_text(content)
    print(f"✅ Added '{keyword}' → {category}")


if __name__ == "__main__":
    main()
