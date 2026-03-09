# GitHub Setup & Installation Guide

Complete guide untuk clone dan setup GVerterx dari GitHub.

## 🚀 Quick Start (5 Menit)

```bash
# 1. Clone repository
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create input/output folders (auto-created on first run)
python3 main.py

# 4. Done! Letakkan Java pack di input/ dan jalankan lagi
```

---

## 📋 Prerequisites

### Windows/macOS/Linux
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/))
- **FFmpeg** (untuk audio conversion - optional tapi recommended)
- **2GB RAM** minimum

### Android (Termux)
- **Termux App** ([F-Droid](https://f-droid.org/packages/com.termux/) atau Google Play)
- **Internet connection**
- **~500MB storage** untuk project + dependencies

---

## 💻 Installation - All Platforms

### Step 1: Clone Repository

**Windows (PowerShell/CMD):**
```bash
cd Desktop
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx
```

**macOS/Linux:**
```bash
cd ~
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx
```

**Android (Termux):**
```bash
cd ~/storage/downloads
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx
```

### Step 2: Install Dependencies

**Option A - Using pip (Recommended):**
```bash
# Windows
python -m pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt

# Android (Termux)
pip install -r requirements.txt
```

**Option B - Using virtual environment (Advanced):**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux/Termux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install Optional Dependencies

**FFmpeg** (untuk audio conversion yang lebih baik):

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Manual):**
1. Download dari [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract ke `C:\ffmpeg`
3. Add ke PATH environment variable

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Termux (Android):**
```bash
pkg install ffmpeg
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version  # Should be 3.8+

# Check if dependencies installed
python -c "import rich; print('✓ Rich installed')"
python -c "import pydantic; print('✓ Pydantic installed')"

# Check FFmpeg (optional)
ffmpeg -version  # Should show version info

# Test converter
python main.py
# Should show interactive menu
```

---

## 📁 Project Structure

```
GVerterx/
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── converter/
│   ├── __init__.py
│   ├── config.py                    # Configuration & mappings
│   ├── core/
│   │   ├── base_converter.py        # Base class
│   │   ├── texture_converter.py     # Image conversion
│   │   ├── sound_converter.py       # Audio conversion
│   │   ├── model_converter.py       # 3D model conversion
│   │   ├── font_converter.py        # Font conversion
│   │   ├── geyser_mapper.py         # Geyser integration
│   │   └── resource_pack_converter.py # Master orchestrator
│   ├── ui/
│   │   └── cli.py                   # Rich CLI interface
│   └── utils/
│       ├── file_utils.py            # File operations
│       └── json_utils.py            # JSON handling
├── input/                           # Place Java packs here
├── output/                          # Bedrock output
├── temp/                            # Temporary files
├── logs/                            # Conversion logs
├── README.md                        # Full documentation
├── QUICKSTART.md                    # 5-minute guide
├── TERMUX_SETUP.md                  # Android specific
├── EXAMPLES.md                      # Usage examples
└── PROJECT_SUMMARY.md               # Technical overview
```

---

## 🎮 First Run - Convert Your First Pack

### Step 1: Prepare Java Pack

```bash
# Copy Java pack to input folder
cp ~/Downloads/YourPack.zip input/

# Or extract it first
unzip input/YourPack.zip -d input/YourPackName
```

### Step 2: Run Converter

```bash
python main.py
```

### Step 3: Select Options from Menu

```
╔════════════════════════════════════════╗
║  MINECRAFT RESOURCE PACK CONVERTER      ║
║  v1.0.0                                 ║
║  Java → Bedrock + GeyserMC              ║
╚════════════════════════════════════════╝

📁 Input packs found: 1
   └─ YourPackName

Available Options:
  1. Convert All Packs
  2. Select Specific Pack
  3. Advanced Options
  4. View History
  5. Exit

Choose option (1-5): [1]
```

### Step 4: Wait for Conversion

- Progress bar will show conversion status
- Detailed logs in `logs/converter.log`
- Output in `output/YourPackName/`

### Step 5: Find Your Converted Pack

```bash
ls output/
# YourPackName/
```

---

## 🔧 Configuration & Customization

### Edit Configuration

**File:** `converter/config.py`

```python
# Sound quality (0-100)
SOUND_QUALITY = 75

# Texture resolution scaling
TEXTURE_SCALE = 1.0  # 1.0 = no change, 0.5 = 50%, 2.0 = 200%

# Enable Geyser mapping
ENABLE_GEYSER_MAPPING = True

# Custom texture mappings
TEXTURE_MAPPINGS = {
    "stone": "stone",
    "custom_block": "stone"  # Map ke Bedrock equivalent
}

# Custom sound mappings
SOUND_MAPPINGS = {
    "ambient.cave": "ambient.cave",
    "entity.player.hurt": "damage.fallsmall"
}
```

### Custom Geyser Items

Edit `converter/core/geyser_mapper.py`:

```python
CUSTOM_GEYSER_ITEMS = {
    "your_custom_item": {
        "texture": "item/custom_item",
        "id": 9000,
        "max_stack_size": 64
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Python not found"**
```bash
# Install Python from python.org
# Or use: python3 instead of python
python3 main.py
```

**2. "ModuleNotFoundError"**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**3. "FFmpeg not found"**
```bash
# Install FFmpeg (see Step 3 above)
# Or skip - converter works without it but audio quality lower
```

**4. Permission denied (Linux/macOS/Termux)**
```bash
chmod +x main.py
# Then run
python3 main.py
```

**5. Output folder not created**
```bash
# Manually create
mkdir -p input output temp logs
python3 main.py
```

**6. Conversion very slow**
- Close other apps
- Reduce texture quality in config.py
- Use smaller pack for testing

**7. Out of memory error**
```bash
# Reduce texture scale in config.py
TEXTURE_SCALE = 0.5  # 50% resolution
```

### Termux Specific Issues

**1. Storage permission denied**
```bash
# Grant storage access
termux-setup-storage

# Use home directory
cd ~/storage/downloads
```

**2. Pip taking too long**
```bash
# Use --no-cache to speed up
pip install --no-cache-dir -r requirements.txt
```

**3. Build tools error**
```bash
# Install build tools
pkg install build-essential clang pkg-config

# Then retry
pip install -r requirements.txt
```

**4. Connection timeout**
```bash
# Retry with timeout
pip install --default-timeout=1000 -r requirements.txt
```

---

## 📚 Documentation

- **[README.md](README.md)** - Complete feature documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start
- **[TERMUX_SETUP.md](TERMUX_SETUP.md)** - Android/Termux guide
- **[EXAMPLES.md](EXAMPLES.md)** - 10+ usage examples
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical details
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design

---

## 🚀 Next Steps

### 1. Basic Usage
```bash
# Quick convert
python main.py
# Follow interactive menu
```

### 2. Advanced Usage
```bash
# Read examples
cat EXAMPLES.md

# Customize config
nano converter/config.py
```

### 3. Deploy to Server
```bash
# For GeyserMC
scp -r output/YourPack user@server:/plugins/geyser/packs/

# For Bedrock client
zip -r YourPack.mcpack output/YourPack/
# Transfer .mcpack to device
```

### 4. Extend & Customize
- Edit `converter/config.py` for mappings
- Edit `converter/core/geyser_mapper.py` for custom items
- Create your own converters extending `base_converter.py`

---

## 💡 Tips & Tricks

### Speed Up Conversion
```python
# In converter/config.py
SOUND_QUALITY = 50  # Lower quality = faster
TEXTURE_SCALE = 0.5  # Smaller = faster
ENABLE_GEYSER_MAPPING = False  # Skip if not needed
```

### Check Logs
```bash
# Real-time logs
tail -f logs/converter.log

# Full logs
cat logs/converter.log
```

### Batch Convert
```bash
# Place multiple packs in input/
ls input/
# Pack1/
# Pack2/
# Pack3/

# Select "Convert All Packs" from menu
python main.py
```

### Update Project
```bash
cd GVerterx
git pull origin main
pip install --upgrade -r requirements.txt
```

---

## 📞 Support

### Getting Help

1. Check [EXAMPLES.md](EXAMPLES.md) for similar use case
2. Check logs: `logs/converter.log`
3. Review [TROUBLESHOOTING section](#troubleshooting) above
4. Check GitHub issues
5. Create GitHub issue with:
   - Converter version: `python main.py --version`
   - Python version: `python --version`
   - Pack name & size
   - Error logs from `logs/converter.log`

### Report Bugs

Create GitHub issue with:
```
Title: [Bug] Descriptive title
Description:
- What you did
- What happened
- Expected behavior
- Error message (full)
- Logs (logs/converter.log)
- System info (Python version, OS)
```

---

## 📄 License

MIT License - See LICENSE file

---

## ✨ Changelog

### v1.0.0 (Initial Release)
- Full Java → Bedrock conversion
- GeyserMC support
- Rich CLI interface
- Comprehensive documentation
- Multi-platform support

---

**Happy Converting! 🎉**
