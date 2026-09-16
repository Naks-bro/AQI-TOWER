"""
Renders report.html → AQI_TOWER_STAKEHOLDER_REPORT.pdf
Run from repo root:  python reports/stakeholder_report/build_pdf.py
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
HTML = pathlib.Path(__file__).resolve().parent / "report.html"
OUT  = ROOT / "reports" / "AQI_TOWER_STAKEHOLDER_REPORT.pdf"

def main():
    if not HTML.exists():
        sys.exit(f"report.html not found at {HTML}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(OUT),
            width="297mm",
            height="210mm",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
    print(f"PDF written -> {OUT}")

if __name__ == "__main__":
    main()
