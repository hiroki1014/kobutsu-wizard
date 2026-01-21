/**
 * カタカナのみかどうかをチェック
 */
export function isKatakana(text: string): boolean {
  // 全角カタカナ、長音記号、中黒、スペースを許可
  return /^[ァ-ヶー・\s　]+$/.test(text);
}

/**
 * 電話番号の形式をチェック
 */
export function isValidPhone(phone: string): boolean {
  // ハイフンあり/なし両対応
  const cleaned = phone.replace(/[-\s]/g, '');
  return /^[0-9]{10,11}$/.test(cleaned);
}

/**
 * URLの形式をチェック
 */
export function isValidUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * 郵便番号の形式をチェック
 */
export function isValidPostalCode(postalCode: string): boolean {
  return /^[0-9]{3}-?[0-9]{4}$/.test(postalCode);
}
