# Amar Bangla Keyboard (আমার বাংলা কীবোর্ড)

Bengali Phonetic Keyboard - Type in Bengali using English letters!

## Features

- **Phonetic Typing**: Type "bangla" → বাংলা
- **Quick Toggle**: Ctrl+Space to switch Bengali/English
- **System Tray**: Visual indicator (EN ↔ বা)
- **Portable**: Single .exe - no installation needed
- **Windows 10/11**: Works on all modern Windows

## Installation

### Option 1: Download Installer
1. Go to [Releases](https://github.com/bhattacharjeeagnishwar/amar-bangla-keyboard/releases)
2. Download `AmarBanglaKeyboard-Setup.exe`
3. Run and follow instructions

### Option 2: Portable
1. Go to [Releases](https://github.com/bhattacharjeeagnishwar/amar-bangla-keyboard/releases)
2. Download `Amar Bangla Keyboard.exe`
3. Run the .exe

### Option 3: Build from Source
```bash
git clone https://github.com/bhattacharjeeagnishwar/amar-bangla-keyboard.git
cd amar-bangla-keyboard
pip install -r requirements.txt
pyinstaller --onefile --windowed --icon assets/amar_bangla_keyboard_logo.ico --name "Amar Bangla Keyboard" app.py
```

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

### Consonants
| Key | Bengali | Key | Bengali |
|-----|---------|-----|---------|
| k | ক | K | খ |
| g | গ | G | ঘ |
| c | চ | C | ছ |
| j | জ | J | ঝ |
| t | ত | T | থ |
| d | দ | D | ধ |
| n | ন | N | ণ |
| p | প | P | ফ |
| b | ব | B | ভ |
| m | ম | M | ং |
| ... | ... | ... | ... |

### Vowels
| Key | Word Start | After Consonant |
|-----|------------|-----------------|
| a | অ | া (কা) |
| i | ই | ি (কি) |
| u | উ | ু (কু) |
| e | এ | ে (কে) |
| o | ও | ো (কো) |

### Special
| Key | Bengali | Description |
|-----|---------|-------------|
| ; | ্ | Hasant (joiner) |
| : | ঃ | Bisarg |
| ` | ঋ/ৃ | Ri (start), Ri (after consonant) |

### Numbers
| Key | Bengali |
|-----|---------|
| 0-9 | ০-৯ |

## Examples

| Type | Bengali |
|------|---------|
| bangla | বাংলা |
| ami | আমি |
| k;t | ক্ত |
| bidyaloy | বিদ্যালয় |
| 1234 | ১২৩৪ |

## Technology

- **Language**: Python 3
- **Libraries**: keyboard, pystray, PIL, pyinstaller
- **License**: MIT

## License

MIT License - Free to use and modify.

## Contact

Email: support@amarbangla.in

---

**Made with ❤️ for Bengali users**