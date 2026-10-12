# Amar Bangla Keyboard (আমার বাংলা কীবোর্ড)

Bengali Phonetic Keyboard - Type in Bengali using English letters!

## Features

- **Simple Typing**: Type `k` → ক, `K` → খ, `ka` → কা
- **Quick Toggle**: Ctrl+Space to switch Bengali/English
- **System Tray**: Visual indicator (EN ↔ বা)
- **Portable**: Single .exe - no installation needed
- **Windows 10/11**: Works on all modern Windows

## Installation

### Option 1: Windows Installer (recommended)
1. Go to [Releases](https://github.com/bhattacharjeeagnishwar/amar-bangla-keyboard/releases)
2. Download `AmarBanglaKeyboard-Setup-1.0.0.exe`
3. Run it. **No admin rights needed** - it installs for the current user.
   The wizard lets you add a desktop icon and start the app with Windows.
4. Uninstall anytime from **Settings → Apps** (or the Start Menu shortcut).

### Option 2: Portable
1. Go to [Releases](https://github.com/bhattacharjeeagnishwar/amar-bangla-keyboard/releases)
2. Download `Amar Bangla Keyboard.exe`
3. Run the .exe (nothing is installed)

### Option 3: Build from Source
```bash
git clone https://github.com/bhattacharjeeagnishwar/amar-bangla-keyboard.git
cd amar-bangla-keyboard
pip install -r requirements.txt
```

- Build the app: `build.bat` → `dist\Amar Bangla Keyboard.exe`
- Build the installer (needs [Inno Setup 6](https://jrsoftware.org/isdl.php)):
  `build_installer.bat` → `installer\AmarBanglaKeyboard-Setup-1.0.0.exe`

Without Inno Setup you can also use the plain batch installer:
`install.bat` copies the app to `%LOCALAPPDATA%`, adds shortcuts and a
proper uninstall entry; `uninstall.bat` removes everything cleanly.

## Usage

| Action | Shortcut |
|--------|----------|
| Toggle Bengali/English | **Ctrl+Space** |
| Help | **F1** |
| Exit | Right-click tray → Quit |

**Tray Icon:**
- Blue (বা) = Bengali mode
- Grey (EN) = English mode

## Keyboard Mapping

A plain, case-sensitive key map: every key maps to one Bengali letter, and
upper case is a different letter (`k`=ক, `K`=খ, `f`=ট, `v`=ড, ...).
Consecutive consonants are **not** joined automatically — use `;` to write a
conjunct.

### Consonants
| Key | Bengali | Key | Bengali | Key | Bengali | Key | Bengali |
|-----|---------|-----|---------|-----|---------|-----|---------|
| k | ক | K | খ | g | গ | G | ঘ |
| c | চ | C | ছ | j | জ | J | ঝ |
| t | ত | T | থ | d | দ | D | ধ |
| n | ন | N | ণ | p | প | P | ফ |
| b | ব | B | ভ | m | ম | M | ং |
| r | র | R | ড় | l | ল | L | ঢ় |
| s | স | S | শ | h | হ | H | ষ |
| y | য | Y | য় | f | ট | F | ঠ |
| v | ড | V | ঢ | q | ঙ | Q | ঞ |
| x | ক্ষ | X | জ্ঞ | z | ৎ | Z | ঁ |

### Vowels
| Key | Word Start | After Consonant |
|-----|------------|-----------------|
| a | অ | া (কা) |
| A | আ | া (কা) |
| i | ই | ি (কি) |
| I | ঈ | ী (কী) |
| u | উ | ু (কু) |
| U | ঊ | ূ (কূ) |
| e | এ | ে (কে) |
| E | ঐ | ৈ (কৈ) |
| o | ও | ো (কো) |
| O | ঔ | ৌ (কৌ) |

### Special
| Key | Bengali | Description |
|-----|---------|-------------|
| ; | ্ | Hasant (joiner) — `k;t` → ক্ত |
| : | ঃ | Bisarg |
| . | । | দাঁড়ি (Bengali full stop) |
| ` | ঋ / ৃ | Ri (start), Ri matra (after a consonant) |

### Numbers
| Key | Bengali |
|-----|---------|
| 0-9 | ০-৯ |

## Examples

| Type | Bengali |
|------|---------|
| k | ক |
| K | খ |
| f | ট |
| v | ড |
| ka | কা |
| k;t | ক্ত |
| k: | কঃ |
| 1234 | ১২৩৪ |

> The engine is a plain **key mapping** — there is no stored word list or
> dictionary. It converts letter-by-letter, so type `;` where a conjunct or a
> final hasant is needed.

## Technology

- **Language**: Python 3
- **Libraries**: keyboard, pystray, PIL, pyinstaller
- **License**: MIT

## License

MIT License - Free to use and modify.

## Contact

**Email:** support@amarbangla.in

---

**Made with ❤️ for Bengali users**