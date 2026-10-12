"""Amar Bangla Keyboard - system tray phonetic Bengali keyboard (Windows).

Type romanised Bengali in any application.  Keystrokes are captured with a
global low-level hook, accumulated into a word, converted as a whole and
re-rendered on screen so word hints and context-sensitive vowels work.

Toggle Bengali/English with Ctrl+Space.
"""

import os
import sys
import json
import ctypes
import threading

import keyboard
from pystray import MenuItem as Item
from pystray import Icon
from PIL import Image, ImageDraw, ImageFont

from converter import convert_word

VERSION = "1.1.0"
SUPPORT_EMAIL = "support@amarbangla.in"

MUTEX_NAME = 'AmarBanglaKeyboard_SingleInstance'

# Keep the mutex handle alive for the whole process lifetime.
_mutex_handle = None


def _config_dir():
    """Where config.json lives.

    In a PyInstaller one-file build ``__file__`` points inside the temporary
    _MEIxxxx folder, so the old code wrote config.json into a directory that is
    deleted on exit.  Use %APPDATA% instead.
    """
    base = os.environ.get('APPDATA') or os.path.expanduser('~')
    path = os.path.join(base, 'Amar Bangla Keyboard')
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        path = os.path.dirname(os.path.abspath(__file__))
    return path


CONFIG_FILE = os.path.join(_config_dir(), 'config.json')

# Characters that become part of the current Bengali token.
TOKEN_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    ";:`."
)

# Keys that must never commit/reset the current token on their own.
_MODIFIER_NAMES = {
    'shift', 'left shift', 'right shift',
    'ctrl', 'left ctrl', 'right ctrl',
    'alt', 'left alt', 'right alt', 'alt gr',
    'windows', 'left windows', 'right windows',
    'caps lock', 'num lock', 'scroll lock', 'menu', 'insert',
}

bengali_mode = False

# State of the word currently being typed.
_buffer = []          # raw ascii characters of the current token
_rendered_len = 0     # number of characters currently on screen for the token
_injecting = False    # True while we are synthesising events ourselves
_lock = threading.RLock()

_tray_icon = None

_config = {
    'start_minimized': False,
    'auto_start': False,
}


# --- Config ---------------------------------------------------------------

def _load_config():
    global _config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                _config.update(json.load(f))
    except Exception:
        pass


def _save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(_config, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# --- Tray icon ------------------------------------------------------------

def _load_bengali_font(size):
    """Return a font that can render Bengali, or None.

    PIL's built-in bitmap font cannot draw Bengali glyphs, which made the
    original tray icon show boxes instead of 'বা'.
    """
    for name in ('Nirmala.ttf', 'NirmalaUI.ttf', 'Vrinda.ttf', 'Shonar.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return None


def _create_image(label, fallback, bg_color):
    img = Image.new('RGB', (64, 64), color=(40, 40, 40))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 59, 59], radius=8, fill=bg_color,
                        outline='white', width=2)
    font = _load_bengali_font(34)
    try:
        if font is not None:
            d.text((32, 32), label, fill='white', anchor='mm', font=font)
        else:
            d.text((32, 32), fallback, fill='white', anchor='mm')
    except Exception:
        d.text((32, 32), fallback, fill='white', anchor='mm')
    return img


def _tray_image():
    if bengali_mode:
        return _create_image('বা', 'B', (0, 120, 215))
    return _create_image('EN', 'EN', (128, 128, 128))


def _create_menu():
    return (
        Item('বাংলা মোড: ' + ('চালু' if bengali_mode else 'বন্ধ'),
             lambda i, n: None, enabled=False),
        Item('English মোড: ' + ('বন্ধ' if bengali_mode else 'চালু'),
             lambda i, n: None, enabled=False),
        Item('---', lambda i, n: None, enabled=False),
        Item('সাহায্য (F1)', _show_help),
        Item('Email: ' + SUPPORT_EMAIL, lambda i, n: keyboard.write(SUPPORT_EMAIL)),
        Item('---', lambda i, n: None, enabled=False),
        Item('বন্ধ করুন', _quit),
    )


def _update_tray_icon():
    if _tray_icon is not None:
        _tray_icon.icon = _tray_image()
        _tray_icon.menu = _create_menu()


# --- Mode + help ----------------------------------------------------------

def _toggle_mode(icon=None, item=None):
    global bengali_mode
    with _lock:
        bengali_mode = not bengali_mode
        _reset_token()
    _update_tray_icon()


def _show_help(icon=None, item=None):
    message = (
        'Amar Bangla Keyboard v' + VERSION + '\n'
        'Toggle Bengali/English: Ctrl+Space\n'
        'Help: F1\n'
        'Example: k -> ক, K -> খ, ka -> কা, k;t -> ক্ত\n'
        'Support: ' + SUPPORT_EMAIL
    )
    if _tray_icon is not None:
        try:
            _tray_icon.notify(message, 'Amar Bangla Keyboard')
            return
        except Exception:
            pass
    print(message)


def _quit(icon=None, item=None):
    _save_config()
    if _tray_icon is not None:
        _tray_icon.stop()


# --- Conversion / rendering ----------------------------------------------

def _reset_token():
    global _buffer, _rendered_len
    _buffer = []
    _rendered_len = 0


def _render(extra=0):
    """Rewrite the on-screen token for the current buffer.

    ``extra`` accounts for characters the OS already inserted that we did not
    count yet: +1 for a freshly typed letter, -1 for a backspace the OS already
    applied.
    """
    global _rendered_len, _injecting
    out = convert_word(''.join(_buffer))
    delete = _rendered_len + extra

    _injecting = True
    try:
        for _ in range(max(0, delete)):
            keyboard.send('backspace')
        if out:
            keyboard.write(out)
    finally:
        _injecting = False

    _rendered_len = len(out)


def _modifiers_held():
    for mod in ('ctrl', 'alt', 'windows'):
        try:
            if keyboard.is_pressed(mod):
                return True
        except Exception:
            pass
    return False


def _on_key_event(event):
    if event.event_type != 'down' or not bengali_mode or _injecting:
        return

    name = event.name
    if not name:
        return  # exotic key with no name; never crash the hook

    if name in _MODIFIER_NAMES:
        return

    # Never touch modifier combos: Ctrl+C, Alt+Tab, ... must keep working.
    if _modifiers_held():
        return

    if name == 'backspace':
        _handle_backspace()
        return

    if len(name) == 1 and name in TOKEN_CHARS:
        with _lock:
            _buffer.append(name)
            _render(extra=1)
    else:
        # Space, Enter, arrows, punctuation, ... commit the current token.
        with _lock:
            _reset_token()


def _handle_backspace():
    global _buffer
    if not _buffer:
        return  # nothing of ours on screen; let the OS backspace through
    with _lock:
        _buffer.pop()
        _render(extra=-1)


# --- Entry point ----------------------------------------------------------

def _acquire_single_instance():
    """Return True if this is the only running instance.

    Two copies would each install a global hook and double-convert every word.
    """
    global _mutex_handle
    try:
        kernel32 = ctypes.windll.kernel32
        _mutex_handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
        ERROR_ALREADY_EXISTS = 183
        return kernel32.GetLastError() != ERROR_ALREADY_EXISTS
    except Exception:
        return True


def main():
    global _tray_icon

    if not _acquire_single_instance():
        # Windowed build has no console, so tell the user with a message box.
        ctypes.windll.user32.MessageBoxW(
            0,
            'Amar Bangla Keyboard is already running.\n'
            'Look for the icon in the system tray.',
            'Amar Bangla Keyboard',
            0x40)  # MB_ICONINFORMATION
        return

    _load_config()

    _tray_icon = Icon(
        'Amar Bangla Keyboard',
        _tray_image(),
        'Amar Bangla Keyboard',
        menu=_create_menu(),
    )

    keyboard.add_hotkey('ctrl+space', _toggle_mode)
    keyboard.add_hotkey('f1', _show_help)
    keyboard.on_press(_on_key_event)

    print('Amar Bangla Keyboard v' + VERSION + ' started!')
    print('Ctrl+Space: toggle Bengali/English')

    try:
        _tray_icon.run()
    except Exception:
        # Fall back to a detached icon, keeping the process alive while the
        # global keyboard listener thread is running.
        _tray_icon.run_detached()
        keyboard.wait()


if __name__ == '__main__':
    main()
