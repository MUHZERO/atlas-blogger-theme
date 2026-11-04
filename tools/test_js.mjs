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

test('splitBi splits on the first " | "', () => {
  assert.deepEqual(T.splitBi('Cuisine | مطبخ'), { fr: 'Cuisine', ar: 'مطبخ' });
  assert.deepEqual(T.splitBi('Atlas'), { fr: 'Atlas', ar: 'Atlas' });
  assert.deepEqual(T.splitBi('A | B | C'), { fr: 'A', ar: 'B | C' });
});

test('waUrl appends the encoded message to wa.me only', () => {
  assert.equal(T.waUrl('https://wa.me/212600000000', ['Nom: Sara', 'Msg: Salam']),
    'https://wa.me/212600000000?text=Nom%3A%20Sara%0AMsg%3A%20Salam');
  assert.equal(T.waUrl('#contact', ['x']), '#contact');
});

test('waUrl appends &text= to an api.whatsapp.com base', () => {
  assert.equal(T.waUrl('https://api.whatsapp.com/send?phone=212600000000', ['a b']),
    'https://api.whatsapp.com/send?phone=212600000000&text=a%20b');
});

test('buildLd adds telephone and PostalAddress from contact rows', () => {
  const base = { '@type': 'LocalBusiness', name: 'Atlas' };
  assert.deepEqual(T.buildLd(base, { phone: '+212 5 22 00 00 00', address: 'Maârif, Casablanca' }), {
    ...base, telephone: '+212 5 22 00 00 00',
    address: { '@type': 'PostalAddress', streetAddress: 'Maârif, Casablanca', addressCountry: 'MA' },
  });
  assert.deepEqual(T.buildLd(base, {}), base);
  assert.equal(T.buildLd(base, { address: 'Maârif | المعاريف' }).address.streetAddress, 'Maârif');
});

test('pickLang: stored fr/ar wins, else blog locale (ar* = ar, other = fr)', () => {
  assert.equal(T.pickLang(null, 'ar-MA'), 'ar');
  assert.equal(T.pickLang(null, 'fr'), 'fr');
  assert.equal(T.pickLang('ar', 'fr'), 'ar');
  assert.equal(T.pickLang('xx', 'fr'), 'fr');
  assert.equal(T.pickLang(null, null), 'fr');
});

test('setLang and applyBi are exported by atlas-js', () => {
  assert.equal(typeof T.setLang, 'function');
  assert.equal(typeof T.applyBi, 'function');
});

test('nextIndex wraps forward and back', () => {
  assert.equal(T.nextIndex(2, 3, 1), 0);
  assert.equal(T.nextIndex(0, 3, -1), 2);
  assert.equal(T.nextIndex(0, 1, 1), 0);
  assert.equal(T.nextIndex(1, 3, 1), 2);
});

test('scrollSign: ltr scrolls forward with +1, rtl with -1', () => {
  assert.equal(T.scrollSign('ltr'), 1);
  assert.equal(T.scrollSign('rtl'), -1);
  assert.equal(T.scrollSign(''), 1);
});

// the standalone split right after the post h1 (atlas-js is not defined yet at that point)
const inline = theme.match(/<h1 class='bi'><data:post\.title\/><\/h1>\s*<script>([\s\S]*?)<\/script>/)?.[1]
  .replace(/^\s*\/\/<!\[CDATA\[\s*\n?|\n?\s*\/\/\]\]>\s*$/g, '') ?? '';
const runInline = (text) => {
  const h1 = { textContent: text, attrs: {}, setAttribute(k, v) { this.attrs[k] = v; } };
  Object.defineProperty(h1, 'innerHTML', { set(v) { h1.html = v; h1.firstChild = { textContent: '' }; h1.lastChild = { textContent: '' }; } });
  new Function('document', inline)({ currentScript: { previousElementSibling: h1 } });
  return h1;
};

test('post h1 inline split: "FR | AR" becomes two spans, marked done', () => {
  const h1 = runInline('Riad Médina | رياض المدينة');
  assert.equal(h1.html, '<span lang="fr"></span><span lang="ar"></span>');
  assert.equal(h1.firstChild.textContent, 'Riad Médina');
  assert.equal(h1.lastChild.textContent, 'رياض المدينة');
  assert.ok('data-done' in h1.attrs);
});

test('post h1 inline split: a title without " | " stays once, unchanged', () => {
  const h1 = runInline('Atlas');
  assert.equal(h1.html, undefined);
  assert.equal(h1.textContent, 'Atlas');
  assert.ok('data-done' in h1.attrs);
});
