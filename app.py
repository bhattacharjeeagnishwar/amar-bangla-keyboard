import keyboard
import os
import json
from pystray import MenuItem as Item
from pystray import Icon
from PIL import Image, ImageDraw

VERSION = "1.0.0"

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(WORKING_DIR, "config.json")

bengali_mode = False
_last_consonant = False

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
    'w': 'ও', 'W': 'ঔ',
}

VOWELS = {
    'a': ('অ', 'া'), 'A': ('আ', 'া'),
    'i': ('ই', 'ি'), 'I': ('ঈ', 'ী'),
    'u': ('উ', 'ু'), 'U': ('ঊ', 'ূ'),
    'e': ('এ', 'ে'), 'E': ('ঐ', 'ৈ'),
    'o': ('ও', 'ো'), 'O': ('ঔ', 'ৌ'),
}

SPECIAL = {
    ';': '্', ':': 'ঃ',
    '`': ('ঋ', 'ৃ'),
}

COMMON_WORDS = {
    'ami': 'আমি', 'tumi': 'তুমি', 'she': 'সে',
    'bangla': 'বাংলা', 'bash': 'বাংলা', ' desh': 'দেশ',
    'bharot': 'ভারত', 'bangladesh': 'বাংলাদেশ',
    'k': 'ক', 'kh': 'খ', 'g': 'গ', 'gh': 'ঘ',
    'c': 'চ', 'ch': 'ছ', 'j': 'জ', 'jh': 'ঝ',
    't': 'ত', 'th': 'থ', 'd': 'দ', 'dh': 'ধ',
    'n': 'ন', 'p': 'প', 'ph': 'ফ', 'b': 'ব', 'bh': 'ভ',
    'm': 'ম', 'r': 'র', 'l': 'ল', 's': 'স', 'sh': 'শ',
    'h': 'হ', 'y': 'য', 'n': 'ণ',
    'bidyaloy': 'বিদ্যালয়', 'shikkhito': 'শিক্ষিত',
    'chetona': 'চেতনা', 'muktir': 'মুক্তির',
    'shadhinota': 'স্বাধীনতা', 'desh': 'দেশ',
}

_digits = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')

_buffer = []
_tray_icon = None

_config = {
    'start_minimized': False,
    'auto_start': False,
}

def _load_config():
    global _config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                _config.update(json.load(f))
    except:
        pass

def _save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(_config, f, ensure_ascii=False, indent=2)
    except:
        pass

def _create_image(label, bg_color):
    img = Image.new('RGB', (64, 64), color=(40, 40, 40))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 59, 59], radius=8, fill=bg_color, outline='white', width=2)
    d.text((32, 32), label, fill='white', anchor='mm')
    return img

def _toggle_mode(icon, item):
    global bengali_mode
    bengali_mode = not bengali_mode
    _update_tray_icon()

def _update_tray_icon():
    global _tray_icon
    if _tray_icon:
        label = 'বা' if bengali_mode else 'EN'
        color = (0, 120, 215) if bengali_mode else (128, 128, 128)
        _tray_icon.icon = _create_image(label, color)
        _tray_icon.menu = _create_menu()

def _quit(icon, item):
    _save_config()
    icon.stop()

def _create_menu():
    return (
        Item('বাংলা মোড: ' + ('চালু' if bengali_mode else 'বন্ধ'), lambda i, n: None, enabled=False),
        Item('English মোড: ' + ('বন্ধ' if bengali_mode else 'চালু'), lambda i, n: None, enabled=False),
        Item('---', lambda i, n: None, enabled=False),
        Item('সাহায্য (F1)', lambda i, n: _show_help()),
        Item('---', lambda i, n: None, enabled=False),
        Item('বন্ধ করুন', _quit),
    )

def _show_help():
    keyboard.write('Amar Bangla Keyboard v' + VERSION + '\nToggle: Ctrl+Space\nExit: Right-click tray\nType phonetically: bangla -> বাংলা')

def _convert_char(char, last_consonant):
    if char in CONSONANTS:
        return CONSONANTS[char], True
    elif char in VOWELS:
        start, matra = VOWELS[char]
        if last_consonant:
            return matra, False
        else:
            return start, False
    elif char in SPECIAL:
        val = SPECIAL[char]
        if isinstance(val, tuple):
            if last_consonant:
                return val[1], False
            else:
                return val[0], False
        else:
            return val, False
    elif char.isdigit():
        return char.translate(_digits), False
    else:
        return char, False

def _convert_to_bengali(text):
    global _last_consonant
    result = ""
    for char in text:
        converted, _last_consonant = _convert_char(char, _last_consonant)
        result += converted
    return result

def _on_key_event(event):
    global bengali_mode, _buffer, _tray_icon
    
    if event.event_type != 'down' or not bengali_mode:
        return
    
    key = event.name
    
    if len(key) == 1 and key.isascii() and key.isprintable():
        _buffer.append(key)
        buffer_str = ''.join(_buffer)
        bengali = _convert_to_bengali(buffer_str)
        
        if bengali != buffer_str:
            for _ in range(len(buffer_str)):
                keyboard.send('backspace')
            keyboard.write(bengali)
            _buffer = []
        elif len(buffer_str) > 2:
            if buffer_str in COMMON_WORDS:
                for _ in range(len(buffer_str)):
                    keyboard.send('backspace')
                keyboard.write(COMMON_WORDS[buffer_str])
                _buffer = []

def _on_ctrl_space():
    global bengali_mode
    bengali_mode = not bengali_mode
    _update_tray_icon()

def _on_f1():
    _show_help()

def main():
    global _tray_icon, bengali_mode
    
    _load_config()
    
    _tray_icon = Icon(
        'Amar Bangla Keyboard',
        _create_image('EN', (128, 128, 128)),
        menu=_create_menu(),
    )
    
    keyboard.add_hotkey('ctrl+space', _on_ctrl_space)
    keyboard.add_hotkey('f1', _on_f1)
    keyboard.on_press(_on_key_event)
    
    title = "Amar Bangla Keyboard v" + VERSION
    print(title + " started!")
    print("Ctrl+Space: Toggle Bengali/English")

    _tray_icon.run_detached()

if __name__ == "__main__":
    main()