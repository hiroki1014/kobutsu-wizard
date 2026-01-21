import { useCallback } from 'react';
import { Input, Select, Checkbox } from '../ui';
import { PREFECTURES } from '../../lib/constants';
import type { FormData } from '../../types/form';
import { Oaza } from 'jp-zipcode-lookup';

interface OfficeStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean) => void;
}

export function OfficeStep({ formData, updateField }: OfficeStepProps) {
  const handlePostalCodeChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      updateField('officePostalCode', value);

      const cleaned = value.replace(/-/g, '');
      if (cleaned.length === 7 && /^\d{7}$/.test(cleaned)) {
        try {
          const results = Oaza.byZipcode(cleaned);
          if (results && results.length > 0) {
            const result = results[0];
            updateField('officePrefecture', result.pref?.name || '');
            updateField('officeCity', (result.city?.name || '') + (result.name || ''));
          }
        } catch {
          // 住所が見つからない場合は何もしない
        }
      }
    },
    [updateField]
  );

  return (
    <div>
      <h2 className="text-xl font-bold mb-6">主たる営業所</h2>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
        <p className="text-sm text-blue-800">
          <strong>営業所名称について:</strong> ○○商店、○○屋など自由に設定できます。決まらない場合は個人名でもOK
        </p>
      </div>

      {/* 営業所名称（漢字）→（フリガナ）の順 */}
      <Input
        label="営業所名称（漢字）"
        required
        placeholder="山田商店"
        value={formData.officeNameKanji}
        onChange={(e) => updateField('officeNameKanji', e.target.value)}
      />

      <Input
        label="営業所名称（フリガナ）"
        required
        placeholder="ヤマダショウテン"
        value={formData.officeNameKana}
        onChange={(e) => updateField('officeNameKana', e.target.value)}
        help="全角カタカナで入力"
      />

      <Checkbox
        label="営業所の所在地は住所と同じ"
        checked={formData.officeSameAsAddress}
        onChange={(v) => updateField('officeSameAsAddress', v)}
      />

      {!formData.officeSameAsAddress && (
        <div className="border-l-4 border-blue-500 pl-4 mt-4">
          <h3 className="font-medium mb-4">営業所所在地</h3>
          <Input
            label="郵便番号"
            placeholder="123-4567"
            value={formData.officePostalCode}
            onChange={handlePostalCodeChange}
            help="入力すると住所が自動入力されます"
          />
          <Select
            label="都道府県"
            required
            options={PREFECTURES}
            value={formData.officePrefecture}
            onChange={(v) => updateField('officePrefecture', v)}
          />
          <Input
            label="市区町村"
            required
            placeholder="○○市△△区"
            value={formData.officeCity}
            onChange={(e) => updateField('officeCity', e.target.value)}
          />
          <Input
            label="番地・建物名"
            required
            placeholder="1-2-3 ○○ビル101"
            value={formData.officeStreet}
            onChange={(e) => updateField('officeStreet', e.target.value)}
          />
          <Input
            label="電話番号"
            required
            placeholder="03-1234-5678"
            value={formData.officePhone}
            onChange={(e) => updateField('officePhone', e.target.value)}
          />
        </div>
      )}
    </div>
  );
}
