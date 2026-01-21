"""PDFテンプレートの座標を分析"""
import fitz
from pathlib import Path

# テンプレートPDFを開く
template_path = Path("/home/hirokiwsl/Projects/kobutsu-wizard/kobutsu-app/backend/templates/template.pdf")
doc = fitz.open(str(template_path))

page = doc[0]  # 1ページ目

# テキストブロックを取得して座標を表示
print("=== ページ1のテキスト位置 ===\n")
blocks = page.get_text("dict")["blocks"]

for block in blocks:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if text and any(keyword in text for keyword in ["個人", "昭和", "平成", "令和", "しない", "公安", "古物市場主"]):
                    bbox = span["bbox"]  # (x0, y0, x1, y1) - pdfplumber形式
                    print(f"'{text}': x={bbox[0]:.1f}-{bbox[2]:.1f}, y={bbox[1]:.1f}-{bbox[3]:.1f}")

doc.close()

# A4サイズ
print(f"\nA4サイズ: 595.27 x 841.89")
print("\nreportlab座標への変換: y_reportlab = 841.89 - y_pdfplumber")
