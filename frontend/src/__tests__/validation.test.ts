/**
 * バリデーション関数のテスト
 */
import { describe, it, expect } from 'vitest';
import {
  isKatakana,
  isValidPhone,
  isValidUrl,
  isValidPostalCode,
} from '../lib/validation';

describe('isKatakana', () => {
  it('test_isKatakana_valid: "ヤマダ タロウ" → true', () => {
    expect(isKatakana('ヤマダ タロウ')).toBe(true);
  });

  it('test_isKatakana_with_longvowel: "タナカ イチロー" → true', () => {
    expect(isKatakana('タナカ イチロー')).toBe(true);
  });

  it('test_isKatakana_hiragana: "やまだ" → false', () => {
    expect(isKatakana('やまだ')).toBe(false);
  });

  it('test_isKatakana_kanji: "山田" → false', () => {
    expect(isKatakana('山田')).toBe(false);
  });

  it('test_isKatakana_mixed: "ヤマダtaro" → false', () => {
    expect(isKatakana('ヤマダtaro')).toBe(false);
  });

  it('カタカナと中黒を許可する', () => {
    expect(isKatakana('ヤマダ・タロウ')).toBe(true);
  });

  it('全角スペースを許可する', () => {
    expect(isKatakana('ヤマダ　タロウ')).toBe(true);
  });

  it('数字を含む場合はfalse', () => {
    expect(isKatakana('ヤマダ123')).toBe(false);
  });
});

describe('isValidPhone', () => {
  it('test_isValidPhone_10digits: "0312345678" → true', () => {
    expect(isValidPhone('0312345678')).toBe(true);
  });

  it('test_isValidPhone_11digits: "09012345678" → true', () => {
    expect(isValidPhone('09012345678')).toBe(true);
  });

  it('test_isValidPhone_with_hyphen: "03-1234-5678" → true', () => {
    expect(isValidPhone('03-1234-5678')).toBe(true);
  });

  it('test_isValidPhone_too_short: "123456789" → false', () => {
    expect(isValidPhone('123456789')).toBe(false);
  });

  it('test_isValidPhone_with_letters: "03-abcd-5678" → false', () => {
    expect(isValidPhone('03-abcd-5678')).toBe(false);
  });

  it('12桁以上はfalse', () => {
    expect(isValidPhone('123456789012')).toBe(false);
  });

  it('スペースを含む電話番号も許可', () => {
    expect(isValidPhone('03 1234 5678')).toBe(true);
  });
});

describe('isValidUrl', () => {
  it('test_isValidUrl_https: "https://example.com" → true', () => {
    expect(isValidUrl('https://example.com')).toBe(true);
  });

  it('test_isValidUrl_http: "http://example.com" → true', () => {
    expect(isValidUrl('http://example.com')).toBe(true);
  });

  it('test_isValidUrl_invalid: "not-a-url" → false', () => {
    expect(isValidUrl('not-a-url')).toBe(false);
  });

  it('パス付きURL', () => {
    expect(isValidUrl('https://example.com/path/to/page')).toBe(true);
  });

  it('クエリパラメータ付きURL', () => {
    expect(isValidUrl('https://example.com?param=value')).toBe(true);
  });

  it('空文字列はfalse', () => {
    expect(isValidUrl('')).toBe(false);
  });

  it('プロトコルなしはfalse', () => {
    expect(isValidUrl('example.com')).toBe(false);
  });
});

describe('isValidPostalCode', () => {
  it('test_isValidPostalCode_with_hyphen: "123-4567" → true', () => {
    expect(isValidPostalCode('123-4567')).toBe(true);
  });

  it('test_isValidPostalCode_without_hyphen: "1234567" → true', () => {
    expect(isValidPostalCode('1234567')).toBe(true);
  });

  it('test_isValidPostalCode_invalid: "12-34567" → false', () => {
    expect(isValidPostalCode('12-34567')).toBe(false);
  });

  it('桁数不足はfalse', () => {
    expect(isValidPostalCode('123456')).toBe(false);
  });

  it('桁数過多はfalse', () => {
    expect(isValidPostalCode('12345678')).toBe(false);
  });

  it('文字を含む場合はfalse', () => {
    expect(isValidPostalCode('123-abcd')).toBe(false);
  });
});
