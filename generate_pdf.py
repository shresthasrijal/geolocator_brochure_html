import sys
import os

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright is required to run this script.")
    print("Please install it by running:")
    print("    pip install playwright")
    print("    playwright install chromium")
    sys.exit(1)


def generate_pdfs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Create pdf folder if it doesn't exist
        pdf_dir = os.path.join(current_dir, "pdf")
        os.makedirs(pdf_dir, exist_ok=True)

        # Paths to the HTML files
        front_url = f"file:///{os.path.join(current_dir, 'page_front.html').replace(os.sep, '/')}"
        back_url = f"file:///{os.path.join(current_dir, 'page_back.html').replace(os.sep, '/')}"

        # Output PDF paths
        front_pdf_path = os.path.join(pdf_dir, "page_front.pdf")
        back_pdf_path = os.path.join(pdf_dir, "page_back.pdf")

        print("Loading Front Page...")
        page.goto(front_url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")

        print(f"Generating {front_pdf_path} ...")
        page.pdf(
            path=front_pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        print("Loading Back Page...")
        page.goto(back_url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")

        print(f"Generating {back_pdf_path} ...")
        page.pdf(
            path=back_pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        browser.close()
        print("Success! PDFs saved in /pdf folder (existing files replaced).")


if __name__ == "__main__":
    generate_pdfs()
