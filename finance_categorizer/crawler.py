"""
Crawl BNP Paribas GOonline and download transaction xlsx.

Usage:
    python3 -m finance_categorizer.crawler          # headless download
    python3 -m finance_categorizer.crawler --debug  # visible browser
    python3 -m finance_categorizer.crawler -f       # force re-download

Downloads to ~/Downloads/1.xlsx
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(Path(__file__).parent.parent / ".env")

LOGIN = os.environ["BANK_LOGIN"]
PASSWORD = os.environ["BANK_PASSWORD"]
DOWNLOAD_PATH = Path.home() / "Downloads" / "1.xlsx"


def run(headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto("https://goonline.bnpparibas.pl/login")

        # Dismiss cookie popup
        try:
            page.locator('button:has-text("Rozumiem")').click(timeout=10000)
        except:
            pass

        # Step 1: enter login
        page.locator("#id-username").wait_for(state="visible", timeout=15000)
        page.locator("#id-username").fill(LOGIN)
        page.locator('button[type="submit"]').first.click()

        # Step 2: enter password
        page.locator("#password-input").wait_for(state="visible", timeout=15000)
        page.locator("#password-input").fill(PASSWORD)
        page.locator('button[type="submit"]').first.click()

        # Dismiss "Ustaw przeglądarkę jako zaufaną" popup
        try:
            page.locator('button:has-text("Zamknij")').click(timeout=10000)
        except:
            pass

        # Navigate to Historia
        page.locator('a:has-text("Historia"), button:has-text("Historia")').first.wait_for(state="visible", timeout=15000)
        page.locator('a:has-text("Historia"), button:has-text("Historia")').first.click()

        # Download XLS
        download_btn = page.locator('button:has-text("Pobierz historię do pliku XLS")')
        download_btn.wait_for(state="visible", timeout=15000)
        with page.expect_download(timeout=30000) as download_info:
            download_btn.click()
        download = download_info.value
        download.save_as(DOWNLOAD_PATH)
        print(f"📥 Downloaded: {DOWNLOAD_PATH}")

        browser.close()


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    force = "-f" in sys.argv or "--force" in sys.argv
    if not force and DOWNLOAD_PATH.exists() and (time.time() - DOWNLOAD_PATH.stat().st_mtime) < 10800:
        print(f"📂 Using cached {DOWNLOAD_PATH} (less than 3h old)")
    else:
        run(headless=not debug)
