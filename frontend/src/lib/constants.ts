export const PREFECTURES = [
  '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
  '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
  '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
  '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
  '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
  '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
  '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
] as const;

export const ERA_OPTIONS = [
  { value: 'seireki', label: '西暦' },
  { value: 'showa', label: '昭和' },
  { value: 'heisei', label: '平成' },
  { value: 'reiwa', label: '令和' },
] as const;

export const CORPORATION_TYPES = [
  { value: 'kabushiki', label: '株式会社' },
  { value: 'yugen', label: '有限会社' },
  { value: 'gomei', label: '合名会社' },
  { value: 'goshi', label: '合資会社' },
  { value: 'other', label: 'その他法人' },
] as const;

export const STEPS = [
  { id: 'applicant', title: '申請者情報' },
  { id: 'address', title: '住所' },
  { id: 'career', title: '職歴' },
  { id: 'office', title: '営業所' },
  { id: 'manager', title: '管理者' },
  { id: 'website', title: 'ホームページ' },
  { id: 'submission', title: '申請情報' },
  { id: 'confirm', title: '確認' },
] as const;
