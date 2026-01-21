import { Input } from './ui';
import type { FormData } from '../types/form';

interface BirthDateInputProps {
  prefix: string;
  formData: FormData;
  updateField: (field: keyof FormData, value: string) => void;
}

export function BirthDateInput({ prefix, formData, updateField }: BirthDateInputProps) {
  const yearKey = `${prefix}Year` as keyof FormData;
  const monthKey = `${prefix}Month` as keyof FormData;
  const dayKey = `${prefix}Day` as keyof FormData;

  return (
    <div className="grid grid-cols-4 gap-2">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          元号<span className="text-red-500 ml-1">*</span>
        </label>
        <div className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-700">
          西暦
        </div>
      </div>
      <Input
        label="年"
        required
        type="number"
        min={1900}
        max={2100}
        placeholder="1990"
        value={formData[yearKey] as string}
        onChange={(e) => updateField(yearKey, e.target.value)}
      />
      <Input
        label="月"
        required
        type="number"
        min={1}
        max={12}
        placeholder="1"
        value={formData[monthKey] as string}
        onChange={(e) => updateField(monthKey, e.target.value)}
      />
      <Input
        label="日"
        required
        type="number"
        min={1}
        max={31}
        placeholder="1"
        value={formData[dayKey] as string}
        onChange={(e) => updateField(dayKey, e.target.value)}
      />
    </div>
  );
}
