"""
Unified CLI entry point for FinanceCategorizer.

Usage:
    finance [start_day] [-p] [-f]         # сводная таблица (default)
    finance -d [day] [Category] [-p]      # детальный просмотр
    finance -e "keyword" Category         # редактирование категорий
    finance -i "keyword" [amount]         # временное игнорирование
"""

import sys


def main():
    args = sys.argv[1:]

    # Auto-cleanup old temp rules on every run
    from finance_categorizer.temp_rules import cleanup
    removed = cleanup()
    if removed:
        print(f"🧹 Removed {removed} expired temp rule(s)")

    if '-h' in args or '--help' in args:
        print("""📊 FinanceCategorizer

  finance [day] [-p] [-f]          сводная таблица (с кешем xlsx 3ч)
  finance 15                       с 15-го числа
  finance -f                       принудительно перекачать xlsx
  finance -p                       за предыдущий месяц
  finance -p 10                    за предыдущий месяц с 10-го

  finance -d [day] [Category] [-p] детальный просмотр транзакций
  finance -d 15                    все транзакции за 15-е
  finance -d Grocery               все Grocery за текущий месяц
  finance -d 15 Grocery            Grocery за 15-е
  finance -d -p                    все за предыдущий месяц

  finance -e "keyword" Category    добавить keyword в категорию (temp, 2 мес)
  finance -e "keyword" 5.00 Cat    с привязкой к сумме

  finance -i "keyword"             игнорировать транзакции (temp, 2 мес)
  finance -i "keyword" 5.00        игнорировать по keyword + сумме

  finance -h                       эта справка""")
        return

    if '-ep' in args:
        args.remove('-ep')
        sys.argv = ['finance_categorizer.perm_edit'] + args
        from finance_categorizer.perm_edit import main as perm_edit_main
        perm_edit_main()
    elif '-i' in args:
        args.remove('-i')
        sys.argv = ['finance_categorizer.ignore_edit'] + args
        from finance_categorizer.ignore_edit import main as ignore_edit_main
        ignore_edit_main()
    elif '-e' in args:
        args.remove('-e')
        sys.argv = ['finance_categorizer.category_edit'] + args
        from finance_categorizer.category_edit import main as edit_main
        edit_main()
    elif '-d' in args:
        args.remove('-d')
        sys.argv = ['finance_categorizer.detail'] + args
        from finance_categorizer.crawler import run, DOWNLOAD_PATH
        import time

        force = '-f' in args
        if force:
            args.remove('-f')
            sys.argv = ['finance_categorizer.detail'] + args

        if not force and DOWNLOAD_PATH.exists() and (time.time() - DOWNLOAD_PATH.stat().st_mtime) < 10800:
            print(f"📂 Using cached {DOWNLOAD_PATH} (less than 3h old)")
        else:
            run(headless=True)

        sys.argv = ['finance_categorizer.detail'] + args
        from finance_categorizer.detail import main as detail_main
        detail_main()
    else:
        # Default: crawler + formatter
        from finance_categorizer.crawler import run, DOWNLOAD_PATH
        import time

        force = '-f' in args
        debug = '--debug' in args

        crawler_args = [a for a in args if a in ('-f', '--force', '--debug')]
        formatter_args = [a for a in args if a not in ('-f', '--force', '--debug')]

        if not force and DOWNLOAD_PATH.exists() and (time.time() - DOWNLOAD_PATH.stat().st_mtime) < 10800:
            print(f"📂 Using cached {DOWNLOAD_PATH} (less than 3h old)")
        else:
            run(headless=not debug)

        sys.argv = ['finance_categorizer.formatter'] + formatter_args
        from finance_categorizer.formatter import main as formatter_main
        formatter_main()


if __name__ == "__main__":
    main()
