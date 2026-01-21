"""古物商許可申請書 生成API"""

from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .schemas import FormData
from .pdf_generator import generate_kobutsu_pdf


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


@app.get("/api/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}


@app.post("/api/generate-pdf")
async def generate_pdf(data: FormData):
    """PDF生成エンドポイント"""
    if not TEMPLATE_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="テンプレートPDFが見つかりません"
        )

    try:
        pdf_bytes = generate_kobutsu_pdf(data, str(TEMPLATE_PATH))

        # ファイル名生成（RFC 5987に従ってURLエンコード）
        filename = f"古物商許可申請書_{data.nameKanji}.pdf"
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
