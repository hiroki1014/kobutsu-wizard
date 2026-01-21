import type { FormData } from '../types/form';

const API_BASE = 'http://localhost:8000';

export async function generatePdf(data: FormData): Promise<Blob> {
  const response = await fetch(`${API_BASE}/api/generate-pdf`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'PDF生成に失敗しました' }));
    throw new Error(error.detail || 'PDF生成に失敗しました');
  }

  return response.blob();
}

export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    return response.ok;
  } catch {
    return false;
  }
}
