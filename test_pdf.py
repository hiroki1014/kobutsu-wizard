"""PDFを生成してページごとにスクリーンショットを撮る"""
from playwright.sync_api import sync_playwright
import subprocess
import time
from pathlib import Path

# PDF出力先
DOWNLOAD_DIR = Path("/tmp/kobutsu_test")
DOWNLOAD_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    # アプリにアクセス
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')

    # テストデータを読み込む
    page.click('text=[DEV] テストデータを読み込む')
    page.wait_for_timeout(500)

    # スクリーンショット（確認画面）
    page.screenshot(path=str(DOWNLOAD_DIR / 'confirm_screen.png'), full_page=True)
    print(f"確認画面スクリーンショット: {DOWNLOAD_DIR / 'confirm_screen.png'}")

    # PDFダウンロード
    with page.expect_download() as download_info:
        page.click('text=申請書をダウンロード')

    download = download_info.value
    pdf_path = DOWNLOAD_DIR / "test_output.pdf"
    download.save_as(str(pdf_path))
    print(f"PDF保存: {pdf_path}")

    browser.close()

# PDFをページごとに画像に変換
print("\nPDFを画像に変換中...")
subprocess.run([
    "pdftoppm", "-png", "-r", "150",
    str(pdf_path),
    str(DOWNLOAD_DIR / "page")
], check=True)

# 生成されたファイル一覧
print("\n生成されたファイル:")
for f in sorted(DOWNLOAD_DIR.glob("*")):
    print(f"  {f}")
