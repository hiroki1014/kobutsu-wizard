"""古物商許可申請書 生成API"""

from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .schemas import FormData, CareerEntry
from .pdf_generator import generate_kobutsu_pdf, generate_test_pdf, generate_full_application_pdf


app = FastAPI(
    title="古物商許可申請書 生成API",
    description="フォームデータからPDFを生成するAPI",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# テンプレートPDFのパス
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "template.pdf"
SEIYAKU_KOJIN_PATH = Path(__file__).parent.parent / "templates" / "r07_01_kobutsu_seiyakusho_kojin.pdf"
SEIYAKU_KANRISHA_PATH = Path(__file__).parent.parent / "templates" / "r07_03_kobutsu_seiyakusho_kanrisha.pdf"
RYAKUREKI_PATH = Path(__file__).parent.parent / "templates" / "r02_ryakurekisyo.pdf"


@app.get("/api/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}


@app.post("/api/generate-pdf")
async def generate_pdf(data: FormData):
    """PDF生成エンドポイント（全書類を含む）"""
    # テンプレートの存在確認
    templates = [
        (TEMPLATE_PATH, "許可申請書テンプレート"),
        (SEIYAKU_KOJIN_PATH, "誓約書（個人用）テンプレート"),
        (SEIYAKU_KANRISHA_PATH, "誓約書（管理者用）テンプレート"),
        (RYAKUREKI_PATH, "略歴書テンプレート"),
    ]
    for path, name in templates:
        if not path.exists():
            raise HTTPException(
                status_code=500,
                detail=f"{name}が見つかりません: {path}"
            )

    try:
        pdf_bytes = generate_full_application_pdf(
            data,
            str(TEMPLATE_PATH),
            str(SEIYAKU_KOJIN_PATH),
            str(SEIYAKU_KANRISHA_PATH),
            str(RYAKUREKI_PATH),
        )

        # ファイル名生成（RFC 5987に従ってURLエンコード）
        filename = f"古物商許可申請書一式_{data.nameKanji}.pdf"
        encoded_filename = quote(filename, safe='')

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF生成に失敗しました: {str(e)}"
        )


@app.get("/api/test-pdf")
async def test_pdf(grid: bool = False):
    """テストPDF生成

    Args:
        grid: True=ドットグリッド付き（座標調整用）
    """
    templates = [
        (TEMPLATE_PATH, "許可申請書テンプレート"),
        (SEIYAKU_KOJIN_PATH, "誓約書（個人用）テンプレート"),
        (SEIYAKU_KANRISHA_PATH, "誓約書（管理者用）テンプレート"),
        (RYAKUREKI_PATH, "略歴書テンプレート"),
    ]
    for path, name in templates:
        if not path.exists():
            raise HTTPException(
                status_code=500,
                detail=f"{name}が見つかりません: {path}"
            )

    try:
        # サンプルデータで全書類を生成
        sample_data = FormData(
            applicantType='individual',
            lastNameKanji='山田',
            firstNameKanji='太郎',
            lastNameKana='ヤマダ',
            firstNameKana='タロウ',
            birthEra='heisei',
            birthYear='5',
            birthMonth='3',
            birthDay='15',
            prefecture='大阪府',
            city='大阪市北区',
            street='梅田1-2-3',
            phone='06-1234-5678',
            officeSameAsAddress=True,
            officeNameKana='ヤマダショウテン',
            officeNameKanji='山田商店',
            managerSameAsApplicant=True,
            hasWebsite=False,
            submissionPrefecture='大阪府',
            careerHistory=[
                CareerEntry(year='2015', month='4', content='○○大学 入学'),
                CareerEntry(year='2019', month='3', content='同大学 卒業'),
                CareerEntry(year='2019', month='4', content='株式会社○○商事 入社'),
                CareerEntry(year='2021', month='9', content='同社 退職'),
                CareerEntry(year='2021', month='10', content='△△株式会社 入社'),
                CareerEntry(year='2023', month='3', content='同社 退職'),
            ],
        )
        pdf_bytes = generate_full_application_pdf(
            sample_data,
            str(TEMPLATE_PATH),
            str(SEIYAKU_KOJIN_PATH),
            str(SEIYAKU_KANRISHA_PATH),
            str(RYAKUREKI_PATH),
            with_grid=grid,
        )
        filename = "test_full_application_grid.pdf" if grid else "test_full_application.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF生成に失敗しました: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
