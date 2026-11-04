import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const theme = readFileSync(new URL('../theme.xml', import.meta.url), 'utf8');
const script = (id) => {
  const match = theme.match(new RegExp(`<script\\b[^>]*\\bid=["']${id}["'][^>]*>([\\s\\S]*?)</script>`, 'i'));
  return match?.[1].replace(/^\s*\/\/<!\[CDATA\[\s*\n?|\n?\s*\/\/\]\]>\s*$/g, '') ?? '';
};
const evaluate = (code) => {
  const module = { exports: {} };
  new Function('module', code)(module);
  return module.exports;
};

export const T = { ...evaluate(script('atlas-head')), ...evaluate(script('atlas-js')) };
export { assert, test };

// --- tests ---
test('theme helpers export an object', () => assert.equal(typeof T, 'object'));
