"""Bengali conversion engine for Amar Bangla Keyboard.

Simple case-sensitive letter mapping (the original "chhoto-hather" scheme):
  - every key maps to one Bengali letter; upper case is a different letter
      k=ক   K=খ      g=গ   G=ঘ      c=চ   C=ছ      j=জ   J=ঝ
      t=ত   T=থ      d=দ   D=ধ      n=ন   N=ণ      p=প   P=ফ
      b=ব   B=ভ      m=ম   M=ং      r=র   R=ড়      l=ল   L=ঢ়
      s=স   S=শ      h=হ   H=ষ      y=য   Y=য়      f=ট   F=ঠ
      v=ড   V=ঢ      q=ঙ   Q=ঞ      x=ক্ষ  X=জ্ঞ     z=ৎ   Z=ঁ
  - vowels are context sensitive: word-initial form vs the matra used after
    a consonant (a=অ/া, i=ই/ি, u=উ/ু, e=এ/ে, o=ও/ো, ...)
  - ';' joins two letters:  k;t -> ক্ত
  - ';' before a vowel is a break, giving the independent vowel:
      b;i -> ব + ই = বই  (so বই, নই, ... can be typed)
  - ':' -> ঃ (bisarga),  '.' -> । (দাঁড়ি),  '`' -> ঋ / ৃ (ri)

The engine is purely a key mapping: there is no stored word list or dictionary,
and consecutive consonants are NOT joined automatically (use ';' for that).

This module has no OS / GUI dependency so it can be unit-tested anywhere.
"""

# --- Key tables -----------------------------------------------------------

# Case-sensitive single letter -> Bengali letter.
CONSONANTS = {
    'k': 'ক', 'K': 'খ',
    'g': 'গ', 'G': 'ঘ',
    'c': 'চ', 'C': 'ছ',
    'j': 'জ', 'J': 'ঝ',
    't': 'ত', 'T': 'থ',
    'd': 'দ', 'D': 'ধ',
    'n': 'ন', 'N': 'ণ',
    'p': 'প', 'P': 'ফ',
    'b': 'ব', 'B': 'ভ',
    'm': 'ম', 'M': 'ং',
    'r': 'র', 'R': 'ড়',
    'l': 'ল', 'L': 'ঢ়',
    's': 'স', 'S': 'শ',
    'h': 'হ', 'H': 'ষ',
    'y': 'য', 'Y': 'য়',
    'f': 'ট', 'F': 'ঠ',
    'v': 'ড', 'V': 'ঢ',
    'q': 'ঙ', 'Q': 'ঞ',
    'x': 'ক্ষ', 'X': 'জ্ঞ',
    'z': 'ৎ', 'Z': 'ঁ',
}

# Vowel key -> (independent form, matra form).
VOWELS = {
    'a': ('অ', 'া'), 'A': ('আ', 'া'),
    'i': ('ই', 'ি'), 'I': ('ঈ', 'ী'),
    'u': ('উ', 'ু'), 'U': ('ঊ', 'ূ'),
    'e': ('এ', 'ে'), 'E': ('ঐ', 'ৈ'),
    'o': ('ও', 'ো'), 'O': ('ঔ', 'ৌ'),
    'w': ('ও', 'ো'), 'W': ('ঔ', 'ৌ'),
}

# Letters that end a syllable (a following vowel stays independent).
_NON_JOINING = {'M', 'Z'}

_VIRAMA = '\u09cd'

_digits = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')


def convert_word(text):
    """Convert one romanised token to Bengali.  Empty in, empty out."""
    if not text:
        return ''

    out = []
    prev_consonant = False
    pending_virama = False
    for ch in text:
        # A ';' immediately followed by a vowel is a *break*, not a hasant:
        # the vowel keeps its independent form so words like বই / নই work
        # (b;i -> বই).  Before a consonant ';' is still the conjunct hasant.
        if pending_virama and ch in VOWELS:
            indep, _matra = VOWELS[ch]
            out.append(indep)
            prev_consonant = False
            pending_virama = False
            continue

        if pending_virama:
            out.append(_VIRAMA)
            pending_virama = False

        if ch in CONSONANTS:
            out.append(CONSONANTS[ch])
            prev_consonant = ch not in _NON_JOINING
        elif ch in VOWELS:
            indep, matra = VOWELS[ch]
            out.append(matra if prev_consonant else indep)
            prev_consonant = False
        elif ch == ';':
            pending_virama = True
            prev_consonant = False
        elif ch == ':':
            out.append('ঃ')
            prev_consonant = False
        elif ch == '.':
            out.append('।')          # দাঁড়ি (Bengali full stop)
            prev_consonant = False
        elif ch == '`':
            out.append('ৃ' if prev_consonant else 'ঋ')
            prev_consonant = False
        elif ch.isdigit():
            out.append(ch.translate(_digits))
            prev_consonant = False
        else:
            out.append(ch)
            prev_consonant = False

    if pending_virama:
        out.append(_VIRAMA)

    return ''.join(out)


if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    for word in ('k', 'K', 'f', 'v', 'k;t', 'bangla', 'ami', 'desh',
                 'ka', 'ki', 'katu', '1234', 'k:'):
        print(f'{word:8} -> {convert_word(word)}')
