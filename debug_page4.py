"""4ページ目の座標を分析"""
import fitz
from pathlib import Path

template_path = Path("/home/hirokiwsl/Projects/kobutsu-wizard/kobutsu-app/backend/templates/template.pdf")
doc = fitz.open(str(template_path))

page = doc[3]  # 4ページ目

print("=== ページ4のテキスト位置 ===\n")
blocks = page.get_text("dict")["blocks"]

for block in blocks:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if text and any(keyword in text for keyword in ["用いる", "用いない", "送信", "閲覧"]):
                    bbox = span["bbox"]
                    print(f"'{text[:40]}': x={bbox[0]:.1f}-{bbox[2]:.1f}, y={bbox[1]:.1f}-{bbox[3]:.1f}")

doc.close()
