import { Input, Select } from './ui';
import { PREFECTURES } from '../lib/constants';
import type { FormData } from '../types/form';

interface AddressInputProps {
  prefix: string;
  formData: FormData;
  updateField: (field: keyof FormData, value: string) => void;
  showPhone?: boolean;
}

export function AddressInput({ prefix, formData, updateField, showPhone = true }: AddressInputProps) {
  const postalCodeKey = prefix ? `${prefix}PostalCode` as keyof FormData : 'postalCode';
  const prefectureKey = prefix ? `${prefix}Prefecture` as keyof FormData : 'prefecture';
  const cityKey = prefix ? `${prefix}City` as keyof FormData : 'city';
  const streetKey = prefix ? `${prefix}Street` as keyof FormData : 'street';
  const phoneKey = prefix ? `${prefix}Phone` as keyof FormData : 'phone';

  return (
    <>
      <Input
        label="郵便番号"
        placeholder="123-4567"
        value={formData[postalCodeKey] as string}
        onChange={(e) => updateField(postalCodeKey, e.target.value)}
      />
      <Select
        label="都道府県"
        required
        options={PREFECTURES}
        value={formData[prefectureKey] as string}
        onChange={(value) => updateField(prefectureKey, value)}
      />
      <Input
        label="市区町村"
        required
        placeholder="○○市△△区"
        value={formData[cityKey] as string}
        onChange={(e) => updateField(cityKey, e.target.value)}
      />
      <Input
        label="番地・建物名"
        required
        placeholder="1-2-3 ○○ビル101"
        value={formData[streetKey] as string}
        onChange={(e) => updateField(streetKey, e.target.value)}
      />
      {showPhone && (
        <Input
          label="電話番号"
          required
          placeholder="09012345678"
          value={formData[phoneKey] as string}
          onChange={(e) => updateField(phoneKey, e.target.value)}
          help="ハイフンなしで入力"
        />
      )}
    </>
  );
}
