# Setup Guide - Termux (Android)

Panduan lengkap untuk menjalankan GVerterx di Termux Android.

## 📱 Prerequisites

- **Termux App** - Download dari [F-Droid](https://f-droid.org/packages/com.termux/) (Recommended) atau Google Play
- **Internet Connection** - Untuk download dependencies (~150MB)
- **Storage Access** - Folder untuk input/output packs
- **Minimal 500MB free storage** - Untuk project + dependencies

> **Tip:** F-Droid version lebih stabil. Hindari Google Play versi jika bisa.

---

## ⚙️ Installation Steps (15 Menit)

### Step 1: Update Termux Package Manager

```bash
pkg update
pkg upgrade -y
```

**Expected Output:**
```
Processing triggers for termux-tools ...
upgrade-gradle is already the newest version (7.5)
...
```

### Step 2: Install Required Packages

**Install Python & Tools:**
```bash
# Install Python 3 (3.10+)
pkg install python -y

# Install Git (untuk clone repository)
pkg install git -y

# Install FFmpeg (untuk audio conversion)
pkg install ffmpeg -y

# Install build tools (untuk compile packages)
pkg install build-essential -y

# Install pkg-config (untuk some packages)
pkg install pkg-config -y
```

**Total installation time: ~5-10 minutes** (tergantung kecepatan internet)

### Step 3: Grant Storage Permissions

```bash
# Setup Termux storage access
termux-setup-storage

# This will prompt to allow storage access
# - Tap "Allow" di popup
```

**Verify storage access:**
```bash
# Navigate to downloads folder
cd ~/storage/downloads
ls

# Should show your device files
```

### Step 4: Clone GitHub Repository

```bash
# Go to downloads folder
cd ~/storage/downloads

# Clone GVerterx repository
git clone https://github.com/PickoCore/GVerterx.git

# Enter folder
cd GVerterx
```

**Check clone successful:**
```bash
ls -la
# Should show: main.py, README.md, converter/, input/, output/, etc.
```

### Step 5: Upgrade Pip & Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**If slow, use this instead:**
```bash
# With longer timeout
pip install --default-timeout=1000 -r requirements.txt
```

**Expected time: ~3-5 minutes**

### Step 6: Verify Installation

```bash
# Check Python version
python --version
# Should output: Python 3.10.x or higher

# Check if converter works
python main.py

# Should show: 
# ╔════════════════════════════════════════╗
# ║  MINECRAFT RESOURCE PACK CONVERTER      ║
# ║  v1.0.0 - Java → Bedrock                ║
# ╚════════════════════════════════════════╝
```

---

## 📁 Folder Structure di Termux

```
~/storage/downloads/GVerterx/
├── main.py                          # Run this file
├── requirements.txt                 # Dependencies
├── converter/
│   ├── config.py                    # Configuration
│   ├── core/                        # Core converters
│   │   ├── texture_converter.py
│   │   ├── sound_converter.py
│   │   ├── model_converter.py
│   │   ├── font_converter.py
│   │   ├── geyser_mapper.py
│   │   └── resource_pack_converter.py
│   ├── ui/
│   │   └── cli.py                   # Beautiful interface
│   └── utils/
├── input/                           # Place Java packs here ⬅️
├── output/                          # Converted packs here ⬅️
├── logs/                            # Conversion logs
└── README.md                        # Full documentation
```

---

## 🚀 Running the Converter

### Step 1: Prepare Java Pack

```bash
# Navigate to project folder
cd ~/storage/downloads/GVerterx

# Copy Java pack to input folder
# Option A: From Downloads
cp ~/storage/downloads/YourPack.zip input/

# Option B: From specific folder
cp ~/storage/shared/MyResourcePack.zip input/

# Verify
ls input/
# Should show your pack
```

### Step 2: Run Converter (Interactive)

```bash
# From project folder
cd ~/storage/downloads/GVerterx

# Run the converter
python main.py
```

### Step 3: Follow Menu

```
╔════════════════════════════════════════╗
║  MINECRAFT RESOURCE PACK CONVERTER      ║
║  v1.0.0 - Java → Bedrock + GeyserMC    ║
╚════════════════════════════════════════╝

📁 Input packs found: 1
   └─ YourPack

Available Options:
  1. Convert All Packs
  2. Select Specific Pack
  3. Advanced Options
  4. View History
  5. Exit

Choose option (1-5): [1]
```

**Press 1 and Enter to start conversion**

### Step 4: Wait for Conversion

Progress bar akan menunjukkan:
```
Converting Textures... ████████████░░░░░░░░ 60%
Converting Sounds...  ██████░░░░░░░░░░░░░░ 30%
Converting Models...  ░░░░░░░░░░░░░░░░░░░░ 0%
```

Conversion time:
- Small pack (50MB): ~30 detik
- Medium pack (200MB): ~2 menit
- Large pack (500MB): ~5-10 menit

### Step 5: Check Output

```bash
# List converted packs
ls output/

# Check specific pack
ls output/YourPack_bedrock/

# Should show:
# ├── manifest.json
# ├── textures/
# ├── sounds/
# ├── models/
# └── fonts/
```

---

## 📤 Using Converted Packs

### Option 1: Use Locally on Phone

```bash
# Navigate to output
cd ~/storage/downloads/GVerterx/output

# Copy to Minecraft folder
cp -r YourPack_bedrock ~/storage/games/com.mojang/minecraftpe/resource_packs/

# Open Minecraft:
# 1. Settings → Resource Packs
# 2. Select your pack
# 3. Activate
# 4. Done!
```

### Option 2: Share with Others

```bash
# Create zip file for distribution
cd output
zip -r YourPack_bedrock.zip YourPack_bedrock/

# Copy to share folder
cp YourPack_bedrock.zip ~/storage/shared/

# Share via WhatsApp, Telegram, etc.
```

### Option 3: Use with GeyserMC Server

```bash
# If your server has GeyserMC:

# 1. Zip the converted pack
cd output
zip -r YourPack_bedrock.zip YourPack_bedrock/

# 2. Send to server admin
# Via email, Discord, Telegram, etc.

# 3. Server admin places in:
# /plugins/geyser/packs/YourPack_bedrock.zip

# 4. Restart GeyserMC
# 5. Bedrock players can connect!
```

---

## 🔧 Configuration & Customization

### Edit Configuration

```bash
# Open config file
nano converter/config.py

# Edit settings:
# - SOUND_QUALITY = 75 (0-100)
# - TEXTURE_SCALE = 1.0 (0.5 = half, 2.0 = double)
# - ENABLE_GEYSER_MAPPING = True

# Save: Ctrl+X, Y, Enter
```

### Custom Geyser Items

```bash
# Edit Geyser mapper
nano converter/core/geyser_mapper.py

# Add custom items:
CUSTOM_GEYSER_ITEMS = {
    "your_item": {
        "texture": "item/your_item",
        "id": 9000
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

**1. "command not found: git"**
```bash
# Install git
pkg install git -y

# Retry clone
git clone https://github.com/PickoCore/GVerterx.git
```

**2. "ModuleNotFoundError" saat run**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Retry
python main.py
```

**3. "Permission denied" error**
```bash
# Grant execute permission
chmod +x main.py

# Retry
python main.py
```

**4. "pip is slow" atau timeout**
```bash
# Gunakan dengan timeout yang lebih lama
pip install --default-timeout=1000 -r requirements.txt

# Atau gunakan faster index
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
```

**5. Conversion sangat lambat**
```bash
# Option A: Reduce texture quality
# Edit converter/config.py
TEXTURE_SCALE = 0.5  # 50% size

# Option B: Skip Geyser mapping
ENABLE_GEYSER_MAPPING = False

# Option C: Lower sound quality
SOUND_QUALITY = 50  # (dari 75)
```

**6. "No space left on device"**
```bash
# Check storage
df -h

# Clean up:
rm -rf ~/storage/downloads/GVerterx/temp/*
rm -rf ~/.cache/pip
pkg clean

# Retry
python main.py
```

**7. FFmpeg not found (untuk audio conversion)**
```bash
# Install FFmpeg
pkg install ffmpeg -y

# Retry conversion
python main.py
```

**8. Storage access error**
```bash
# Re-setup storage
termux-setup-storage

# Allow permissions when popup appears
# Retry conversion
```

---

## 💡 Tips & Tricks

### Speed Up Installation

```bash
# Use faster pip mirror
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# Or use tsinghua mirror
pip install -i https://pypi.tsinghua.edu.cn/simple -r requirements.txt
```

### Monitor Conversion in Real-Time

```bash
# Open second terminal, tail logs
tail -f logs/converter.log
```

### Batch Convert Multiple Packs

```bash
# Place all packs in input/ folder
cp ~/storage/downloads/Pack1.zip input/
cp ~/storage/downloads/Pack2.zip input/
cp ~/storage/downloads/Pack3.zip input/

# Run converter
python main.py

# Select "Convert All Packs"
# All akan convert otomatis
```

### Check Conversion History

```bash
# View log file
cat logs/converter.log

# Last 20 lines
tail -20 logs/converter.log

# Real-time monitoring
tail -f logs/converter.log
```

---

## 📚 More Documentation

- **[README.md](README.md)** - Complete feature list
- **[QUICKSTART.md](QUICKSTART.md)** - 5 minute guide
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - All platforms setup
- **[EXAMPLES.md](EXAMPLES.md)** - Usage examples

---

## 🔄 Updating Converter

```bash
# Navigate to project
cd ~/storage/downloads/GVerterx

# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run latest version
python main.py
```

---

## 📞 Help & Support

### If Something Doesn't Work

1. **Check logs:**
   ```bash
   tail logs/converter.log
   ```

2. **Check Python version:**
   ```bash
   python --version
   # Should be 3.10+
   ```

3. **Re-install dependencies:**
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

4. **Create fresh venv:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py
   ```

5. **Report issue on GitHub** dengan:
   - Deskripsi masalah
   - Error message lengkap
   - Python version
   - Pack name dan ukuran
   - Screenshot

---

## ✨ What's Next

After successful conversion:

1. **Test the pack** - Try it on your phone
2. **Share it** - Give to friends or servers
3. **Customize it** - Edit config for your needs
4. **Deploy** - Upload to GeyserMC servers
5. **Extend** - Add custom items/blocks

**Enjoy your converted resource packs! 🎉**
