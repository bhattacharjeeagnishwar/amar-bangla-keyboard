"""Tests for the conversion engine.  Pure-Python, no OS/GUI dependencies.

The engine is a plain case-sensitive key mapping - there is no stored word
list / dictionary and consecutive consonants are not joined automatically.

Run with:  python test_converter.py
"""

from converter import convert_word

CASES = {
    # --- single letters (case sensitive) ---------------------------------
    'k': 'ক',
    'K': 'খ',
    'g': 'গ',
    'G': 'ঘ',
    'c': 'চ',
    'C': 'ছ',
    'j': 'জ',
    'J': 'ঝ',
    't': 'ত',
    'T': 'থ',
    'd': 'দ',
    'D': 'ধ',
    'n': 'ন',
    'N': 'ণ',
    'p': 'প',
    'P': 'ফ',
    'b': 'ব',
    'B': 'ভ',
    'm': 'ম',
    'M': 'ং',
    'r': 'র',
    'R': 'ড়',
    'l': 'ল',
    'L': 'ঢ়',
    's': 'স',
    'S': 'শ',
    'h': 'হ',
    'H': 'ষ',
    'y': 'য',
    'Y': 'য়',
    'f': 'ট',
    'F': 'ঠ',
    'v': 'ড',
    'V': 'ঢ',
    'q': 'ঙ',
    'Q': 'ঞ',
    'x': 'ক্ষ',
    'X': 'জ্ঞ',
    'z': 'ৎ',
    'Z': 'ঁ',

    # --- vowels (context sensitive) --------------------------------------
    'a': 'অ',
    'A': 'আ',
    'i': 'ই',
    'I': 'ঈ',
    'u': 'উ',
    'U': 'ঊ',
    'e': 'এ',
    'E': 'ঐ',
    'o': 'ও',
    'O': 'ঔ',
    'ka': 'কা',
    'ki': 'কি',
    'ku': 'কু',
    'ke': 'কে',
    'ko': 'কো',
    'kA': 'কা',
    'kI': 'কী',

    # --- hasanta / bisarga / ri ------------------------------------------
    'k;': 'ক্',
    'k;t': 'ক্ত',
    'k:': 'কঃ',
    ':': 'ঃ',
    '.': '।',
    'kalo.': 'কালো।',
    '`': 'ঋ',
    'k`': 'কৃ',

    # --- digits ----------------------------------------------------------
    '1234': '১২৩৪',
    '0': '০',

    # --- whole words (plain letter-by-letter output) ---------------------
    'bangla': 'বানগলা',
    'ami': 'অমি',
    'desh': 'দেসহ',

    # --- edge cases ------------------------------------------------------
    '': '',
    'k!': 'ক!',
}


def main():
    failures = 0
    for roman, expected in CASES.items():
        got = convert_word(roman)
        ok = got == expected
        if not ok:
            failures += 1
        mark = 'ok  ' if ok else 'FAIL'
        print(f'[{mark}] {roman!r:10} -> {got!r}   expected {expected!r}')

    print()
    if failures:
        print(f'{failures} test(s) failed.')
        raise SystemExit(1)
    print(f'All {len(CASES)} tests passed.')


if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main()
