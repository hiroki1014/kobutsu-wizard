"""テストデータでPDFを生成してページ画像を作成"""
import json
from pathlib import Path
import urllib.request

# テストデータ（全フィールド入力）
test_data = {
    "applicantType": "individual",
    "corporationType": "",
    "lastNameKanji": "山田",
    "firstNameKanji": "太郎",
    "lastNameKana": "ヤマダ",
    "firstNameKana": "タロウ",
    "corporationName": "",
    "birthEra": "seireki",
    "birthYear": "1980",
    "birthMonth": "03",
    "birthDay": "15",
    "postalCode": "545-0053",
    "prefecture": "大阪府",
    "city": "大阪市阿倍野区松崎町",
    "street": "2-3-37-412",
    "phone": "090-4906-9060",
    "officeSameAsAddress": False,
    "officeNameKanji": "山田商店",
    "officeNameKana": "ヤマダショウテン",
    "officePostalCode": "530-0001",
    "officePrefecture": "大阪府",
    "officeCity": "大阪市北区梅田",
    "officeStreet": "1-2-3",
    "officePhone": "06-1234-5678",
    "managerSameAsApplicant": False,
    "managerLastNameKanji": "鈴木",
    "managerFirstNameKanji": "花子",
    "managerLastNameKana": "スズキ",
    "managerFirstNameKana": "ハナコ",
    "managerBirthEra": "seireki",
    "managerBirthYear": "1990",
    "managerBirthMonth": "07",
    "managerBirthDay": "25",
    "managerPostalCode": "550-0002",
    "managerPrefecture": "大阪府",
    "managerCity": "大阪市西区江戸堀",
    "managerStreet": "4-5-6",
    "managerPhone": "080-9876-5432",
    "representativeType": "1",
    "representativeLastNameKanji": "田中",
    "representativeFirstNameKanji": "一郎",
    "representativeLastNameKana": "タナカ",
    "representativeFirstNameKana": "イチロウ",
    "representativeBirthEra": "seireki",
    "representativeBirthYear": "1965",
    "representativeBirthMonth": "11",
    "representativeBirthDay": "03",
    "representativePostalCode": "542-0081",
    "representativePrefecture": "大阪府",
    "representativeCity": "大阪市中央区南船場",
    "representativeStreet": "7-8-9",
    "representativePhone": "06-5555-1234",
    "hasWebsite": False,
    "websiteUrl": "https://www.example-shop.co.jp",
    "submissionPrefecture": "大阪府",
}

OUTPUT_DIR = Path("/tmp/kobutsu_test")
OUTPUT_DIR.mkdir(exist_ok=True)

# APIでPDF生成
print("PDFを生成中...")
req = urllib.request.Request(
    "http://localhost:8000/api/generate-pdf",
    data=json.dumps(test_data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req) as response:
    pdf_data = response.read()

pdf_path = OUTPUT_DIR / "test_output.pdf"
pdf_path.write_bytes(pdf_data)
print(f"PDF保存完了: {pdf_path}")

# PyMuPDFでPDFを画像に変換
print("\nPDFを画像に変換中...")
import fitz  # PyMuPDF

doc = fitz.open(str(pdf_path))
for i, page in enumerate(doc):
    # 150 DPIで画像化
    mat = fitz.Matrix(150/72, 150/72)
    pix = page.get_pixmap(matrix=mat)
    output_path = OUTPUT_DIR / f"page-{i+1}.png"
    pix.save(str(output_path))
    print(f"  {output_path}")

doc.close()
print("\n完了!")
