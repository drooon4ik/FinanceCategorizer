"""
Unified CLI entry point for FinanceCategorizer.

Usage:
    finance [start_day] [-p] [-f]         # сводная таблица (default)
    finance -d [day] [Category] [-p]      # детальный просмотр
    finance -e "keyword" Category         # редактирование категорий
"""

import sys


def main():
    args = sys.argv[1:]

    if '-e' in args:
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
