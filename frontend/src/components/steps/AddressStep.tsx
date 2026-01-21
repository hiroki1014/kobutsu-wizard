import { useCallback } from 'react';
import { Input, Select } from '../ui';
import { PREFECTURES } from '../../lib/constants';
import type { FormData } from '../../types/form';
import { Oaza } from 'jp-zipcode-lookup';

interface AddressStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean) => void;
}

export function AddressStep({ formData, updateField }: AddressStepProps) {
  const handlePostalCodeChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      updateField('postalCode', value);

      // ハイフンを除去して7桁かチェック
      const cleaned = value.replace(/-/g, '');
      if (cleaned.length === 7 && /^\d{7}$/.test(cleaned)) {
        try {
          const results = Oaza.byZipcode(cleaned);
          if (results && results.length > 0) {
            const result = results[0];
            updateField('prefecture', result.pref?.name || '');
            updateField('city', (result.city?.name || '') + (result.name || ''));
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
      <h2 className="text-xl font-bold mb-6">住所</h2>

      <Input
        label="郵便番号"
        placeholder="123-4567 または 1234567"
        value={formData.postalCode}
        onChange={handlePostalCodeChange}
        help="入力すると住所が自動入力されます"
      />
      <Select
        label="都道府県"
        required
        options={PREFECTURES}
        value={formData.prefecture}
        onChange={(v) => updateField('prefecture', v)}
      />
      <Input
        label="市区町村"
        required
        placeholder="○○市△△区"
        value={formData.city}
        onChange={(e) => updateField('city', e.target.value)}
      />
      <Input
        label="番地・建物名"
        required
        placeholder="1-2-3 ○○ビル101"
        value={formData.street}
        onChange={(e) => updateField('street', e.target.value)}
      />
      <Input
        label="電話番号"
        required
        placeholder="03-1234-5678 または 0312345678"
        value={formData.phone}
        onChange={(e) => updateField('phone', e.target.value)}
        help="ハイフンあり・なしどちらでも可"
      />
    </div>
  );
}
