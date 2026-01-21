import { Input, Select } from './ui';
import { ERA_OPTIONS } from '../lib/constants';
import type { FormData } from '../types/form';

interface BirthDateInputProps {
  prefix: string;
  formData: FormData;
  updateField: (field: keyof FormData, value: string) => void;
}

export function BirthDateInput({ prefix, formData, updateField }: BirthDateInputProps) {
  const eraKey = `${prefix}Era` as keyof FormData;
  const yearKey = `${prefix}Year` as keyof FormData;
  const monthKey = `${prefix}Month` as keyof FormData;
  const dayKey = `${prefix}Day` as keyof FormData;

  return (
    <div className="grid grid-cols-4 gap-2">
      <Select
        label="元号"
        required
        options={ERA_OPTIONS}
        value={formData[eraKey] as string}
        onChange={(value) => updateField(eraKey, value)}
      />
      <Input
        label="年"
        required
        type="number"
        min={1}
        max={99}
        placeholder="1"
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
