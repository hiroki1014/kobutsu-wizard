interface Option {
  value: string;
  label: string;
}

interface RadioGroupProps {
  label: string;
  name: string;
  options: readonly Option[];
  value: string;
  onChange: (value: string) => void;
}

export function RadioGroup({ label, name, options, value, onChange }: RadioGroupProps) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">{label}</label>
      <div className="flex gap-4">
        {options.map((opt) => (
          <label key={opt.value} className="flex items-center cursor-pointer">
            <input
              type="radio"
              name={name}
              value={opt.value}
              checked={value === opt.value}
              onChange={(e) => onChange(e.target.value)}
              className="w-4 h-4 text-blue-600"
            />
            <span className="ml-2 text-gray-700">{opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
