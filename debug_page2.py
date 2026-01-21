"""2ページ目の座標を分析"""
import fitz
from pathlib import Path

template_path = Path("/home/hirokiwsl/Projects/kobutsu-wizard/kobutsu-app/backend/templates/template.pdf")
doc = fitz.open(str(template_path))

page = doc[1]  # 2ページ目

print("=== ページ2のテキスト位置 ===\n")
blocks = page.get_text("dict")["blocks"]

keywords = ["営業所", "名称", "フリガナ", "漢字", "所在地", "取り扱う", "02", "11", "衣", "皮革",
            "管理", "氏名", "生年月日", "昭和", "平成", "令和", "住所", "電話"]

for block in blocks:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if text and any(keyword in text for keyword in keywords):
                    bbox = span["bbox"]
                    print(f"'{text[:30]}': x={bbox[0]:.1f}-{bbox[2]:.1f}, y={bbox[1]:.1f}-{bbox[3]:.1f}")

doc.close()
print(f"\nA4サイズ: 595.27 x 841.89")
