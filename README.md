# 古物商許可申請書 生成Webアプリ

ユーザーに質問形式で情報を入力してもらい、古物商許可申請書（PDF）を生成するWebアプリケーションです。

## 技術スタック

- **フロントエンド**: React + TypeScript + Tailwind CSS (Vite)
- **バックエンド**: Python FastAPI + reportlab + pypdf

## ディレクトリ構造

```
kobutsu-app/
├── frontend/          # フロントエンド（React + TypeScript）
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/       # 汎用UIコンポーネント
│   │   │   └── steps/    # 7つのステップコンポーネント
│   │   ├── lib/          # API、定数、バリデーション
│   │   ├── types/        # 型定義
│   │   └── App.tsx
│   └── package.json
├── backend/           # バックエンド（Python FastAPI）
│   ├── app/
│   │   ├── main.py           # FastAPIエンドポイント
│   │   ├── pdf_generator.py  # PDF生成ロジック
│   │   ├── coordinates.py    # 座標定義
│   │   └── schemas.py        # Pydanticスキーマ
│   ├── templates/
│   │   └── template.pdf      # テンプレートPDF
│   └── requirements.txt
└── README.md
```

## セットアップ

### 前提条件

- Node.js 18+
- Python 3.10+
- IPAゴシックフォント（Ubuntu: `sudo apt install fonts-ipafont-gothic`）

### フロントエンド

```bash
cd frontend
npm install
```

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 起動方法

### バックエンド

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### フロントエンド

```bash
cd frontend
npm run dev
```

ブラウザで http://localhost:5173 にアクセスしてください。

## API

### `GET /api/health`

ヘルスチェック

```json
{ "status": "ok" }
```

### `POST /api/generate-pdf`

PDF生成

- **Request**: JSON (FormData)
- **Response**: `application/pdf`

## 固定値（自動入力）

- 許可の種類: 古物商（古物市場主は二重線で消去）
- 行商: しない
- 営業所形態: 営業所あり
- 取扱品目: 02衣類、11皮革・ゴム製品類

## 入力ステップ

1. **申請者情報**: 氏名、生年月日、申請者種別
2. **住所**: 住所、電話番号
3. **営業所**: 営業所名称、所在地
4. **管理者**: 管理者情報（申請者と同じ場合は省略可）
5. **ホームページ**: URL（任意）
6. **申請情報**: 申請日、提出先公安委員会
7. **確認**: 入力内容の確認

## 開発

### フロントエンドのビルド

```bash
cd frontend
npm run build
```

### 型チェック

```bash
cd frontend
npm run type-check
```
