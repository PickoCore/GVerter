# GVerterx - Complete Step-by-Step Guide

Panduan visual lengkap dari A-Z untuk menggunakan GVerterx.

---

## 🎯 What You'll Learn

By the end of this guide, you will:
- ✅ Clone GVerterx dari GitHub
- ✅ Install semua dependencies
- ✅ Convert Minecraft Java pack menjadi Bedrock
- ✅ Deploy ke server atau bagikan dengan teman

**Time needed: 30 menit total**
- Installation: 15 menit
- First conversion: 15 menit

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Device dengan OS (Windows, macOS, Linux, atau Android)
- [ ] Internet connection (untuk download ~200MB)
- [ ] GitHub account (optional, untuk update)
- [ ] Java resource pack (atau download sample)
- [ ] 1GB free disk space minimum

### Device-Specific Requirements

**Windows:**
- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Administrator access (for installation)

**macOS:**
- [ ] Python 3.8+ installed
- [ ] Homebrew (for installing tools)
- [ ] Git installed

**Linux:**
- [ ] Python 3.8+ installed
- [ ] apt/yum/pacman package manager
- [ ] Git installed

**Android (Termux):**
- [ ] Termux app installed from F-Droid
- [ ] 500MB+ free storage
- [ ] Internet connection

---

## ✅ Installation Guide

### PHASE 1: Prepare Your System (5 menit)

<details>
<summary>📱 Windows User? Click here</summary>

**Step 1: Install Python**
1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.10+ (latest version)
3. Run installer
4. ✅ **IMPORTANT: Check "Add Python to PATH"**
5. Click "Install Now"
6. Wait until "Setup was successful"

**Step 2: Install Git**
1. Go to [git-scm.com](https://git-scm.com/)
2. Download for Windows
3. Run installer
4. Follow defaults (click Next)
5. Finish installation

**Step 3: Verify Installation**
1. Open Command Prompt (Win+R, type `cmd`)
2. Type: `python --version`
3. Should show: `Python 3.10.x` or higher
4. Type: `git --version`
5. Should show: `git version 2.x.x`

</details>

<details>
<summary>🍎 macOS User? Click here</summary>

**Step 1: Install Homebrew**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install Python & Git**
```bash
brew install python@3.10
brew install git
brew install ffmpeg
```

**Step 3: Verify Installation**
```bash
python3 --version
git --version
ffmpeg -version
```

</details>

<details>
<summary>🐧 Linux User? Click here</summary>

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip git ffmpeg -y
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip git ffmpeg -y
```

**Arch:**
```bash
sudo pacman -Sy python git ffmpeg
```

**Verify:**
```bash
python3 --version
git --version
ffmpeg -version
```

</details>

<details>
<summary>🤖 Android (Termux) User? Click here</summary>

**Step 1: Open Termux App**
- Launch Termux from your app drawer

**Step 2: Update Package Manager**
```bash
pkg update
pkg upgrade -y
```

**Step 3: Install Tools**
```bash
pkg install python git ffmpeg build-essential pkg-config -y
```

**Time:** ~5-10 minutes (depending on internet)

**Step 4: Grant Storage Permission**
```bash
termux-setup-storage
```
- Tap "Allow" when popup appears

**Step 5: Verify Installation**
```bash
python --version
git --version
```

</details>

---

### PHASE 2: Clone Repository (2 menit)

<details>
<summary>Windows: Clone Repository</summary>

**Step 1: Open Command Prompt**
- Press Win+R
- Type: `cmd`
- Press Enter

**Step 2: Navigate to Downloads**
```bash
cd %USERPROFILE%\Downloads
```

**Step 3: Clone Repository**
```bash
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx
```

**Step 4: Verify**
```bash
dir
```
Should show: `converter/`, `main.py`, `README.md`, etc.

</details>

<details>
<summary>macOS/Linux: Clone Repository</summary>

**Step 1: Open Terminal**
- macOS: Cmd+Space, type "Terminal"
- Linux: Ctrl+Alt+T

**Step 2: Navigate to Downloads**
```bash
cd ~/Downloads
```

**Step 3: Clone Repository**
```bash
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx
```

**Step 4: Verify**
```bash
ls -la
```
Should show: `converter/`, `main.py`, `README.md`, etc.

</details>

<details>
<summary>Android (Termux): Clone Repository</summary>

```bash
# Navigate to downloads
cd ~/storage/downloads

# Clone repository
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx

# Verify
ls -la
# Should show all files
```

</details>

---

### PHASE 3: Install Dependencies (5 menit)

All platforms use same command:

```bash
# Navigate to GVerterx folder (if not already there)
cd GVerterx

# Install all required packages
pip install -r requirements.txt
```

**If slow, use this instead:**
```bash
pip install --default-timeout=1000 -r requirements.txt
```

**If very slow (Termux), use:**
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
```

**Expected output:**
```
Successfully installed rich-13.5.0 pillow-10.0.0 pydantic-2.0.0 ...
```

---

### PHASE 4: Verify Installation (1 menit)

```bash
# Check Python
python --version
# Should output: Python 3.8+

# Test converter startup
python main.py
# Should show beautiful menu (don't do anything yet)
```

If you see a beautiful menu, **Installation is successful!** ✅

---

## 🎮 Convert Your First Pack

### PHASE 5: Prepare Your Pack (2 menit)

**Option A: Use Your Own Pack**
1. Locate your Java resource pack (.zip file)
2. Copy to: `input/` folder inside GVerterx

**Option B: Download Sample Pack**
```bash
# Make sure you're in GVerterx folder
cd ~/Downloads/GVerterx  # or wherever you put it

# Create input folder
mkdir -p input

# Download sample pack (example)
# From: https://www.curseforge.com/ (download any small Java pack)
# Move to input/ folder
```

**Verify pack is there:**
```bash
ls input/
# Should show your pack file(s)
```

---

### PHASE 6: Run Converter (10-30 menit)

**Step 1: Start Converter**
```bash
# From GVerterx folder
python main.py
```

**You'll see:**
```
╔════════════════════════════════════════╗
║  MINECRAFT RESOURCE PACK CONVERTER      ║
║  v1.0.0 - Java → Bedrock + GeyserMC    ║
╚════════════════════════════════════════╝

📁 Input packs found: 1
   └─ MyResourcePack.zip

Available Options:
  1. Convert All Packs
  2. Select Specific Pack
  3. Advanced Options
  4. View History
  5. Exit

Choose option (1-5):
```

**Step 2: Select Option 1**
- Type: `1`
- Press: Enter

**Step 3: See Progress**
```
Converting Textures... ████████████░░░░░░░░ 60%
Converting Sounds...  ██████░░░░░░░░░░░░░░ 30%
Converting Models...  ░░░░░░░░░░░░░░░░░░░░ 0%

Status: Processing MyResourcePack
Elapsed: 2m 45s
```

**Step 4: Wait for Completion**
- Don't close terminal
- Don't close computer
- Time depends on pack size:
  - Small (50MB): ~30 seconds
  - Medium (200MB): ~2 minutes
  - Large (500MB+): ~5-10 minutes

**You'll see:**
```
✅ Conversion completed successfully!

📊 Statistics:
   Textures: 245 converted
   Sounds: 89 converted
   Models: 12 converted
   Fonts: 5 converted
   
📁 Output folder: output/MyResourcePack_bedrock/

Next steps:
   1. Check output/ folder
   2. Use on Bedrock client
   3. Deploy to GeyserMC server
```

---

## ✨ What You Got

After conversion, you'll find:

```
GVerterx/output/
└── MyResourcePack_bedrock/
    ├── manifest.json         # Bedrock metadata
    ├── textures/
    │   ├── blocks/           # Block textures
    │   └── items/            # Item textures
    ├── sounds/
    │   ├── ambient/
    │   ├── entity/
    │   └── records/
    ├── models/
    │   ├── entity/
    │   └── item/
    ├── ui/                   # UI textures
    ├── font/                 # Custom fonts
    └── geyser/               # Geyser custom items/blocks
        └── mapping.json
```

**This is your converted Bedrock pack! Ready to use.**

---

## 🚀 Next Steps - Use Your Converted Pack

### Option 1: Play on Your Phone (Bedrock)

**Step 1: Copy to Minecraft**
```bash
# Windows
xcopy /E output\MyResourcePack_bedrock "%AppData%\.minecraft\resourcepacks\"

# macOS
cp -r output/MyResourcePack_bedrock ~/Library/Application\ Support/minecraft/resourcepacks/

# Linux
cp -r output/MyResourcePack_bedrock ~/.minecraft/resourcepacks/

# Android (Termux)
cp -r output/MyResourcePack_bedrock ~/storage/games/com.mojang/minecraftpe/resource_packs/
```

**Step 2: Open Minecraft**
1. Launch Minecraft: Bedrock Edition
2. Go to: Settings → Resource Packs
3. Find: MyResourcePack_bedrock
4. Click "Activate"
5. Create world and enjoy!

### Option 2: Deploy to Server (GeyserMC)

**Step 1: Zip the pack**
```bash
cd output
zip -r MyResourcePack_bedrock.zip MyResourcePack_bedrock/
```

**Step 2: Send to server admin**
- Email the zip file
- Or upload to: Discord, Google Drive, etc.

**Step 3: Server admin**
1. Extract zip to: `/plugins/geyser/packs/`
2. Reload GeyserMC
3. Bedrock players auto-download pack

### Option 3: Share with Friends

**Step 1: Create shareable zip**
```bash
cd output
zip -r MyResourcePack_bedrock.zip MyResourcePack_bedrock/
```

**Step 2: Share via**
- WhatsApp / Telegram / Discord
- Google Drive / Dropbox / OneDrive
- Email
- AirDrop (macOS)
- Bluetooth (Android)

**Friends Step 3: Import**
1. Receive .zip file
2. Open in Minecraft: Bedrock Edition
3. Auto-imports as resource pack
4. Activate in settings

---

## 🔄 Convert More Packs

**Easy workflow for multiple packs:**

```bash
# Copy multiple packs to input/
cp ~/Downloads/Pack1.zip input/
cp ~/Downloads/Pack2.zip input/
cp ~/Downloads/Pack3.zip input/

# Run converter
python main.py

# Select option 1: Convert All Packs
# All convert automatically!

# Check results
ls output/
# Pack1_bedrock/
# Pack2_bedrock/
# Pack3_bedrock/
```

---

## 🔧 Customize Conversion

**Want to adjust settings?**

```bash
# Edit config
nano converter/config.py

# Options:
# - TEXTURE_SCALE = 0.5  (smaller files, faster)
# - SOUND_QUALITY = 50   (lower quality, faster)
# - ENABLE_GEYSER_MAPPING = False  (skip Geyser if not needed)

# Save and retry conversion
python main.py
```

---

## 📊 Check Conversion Log

**See what happened:**

```bash
# View last conversion
tail logs/converter.log

# Watch real-time
tail -f logs/converter.log

# Search for errors
grep ERROR logs/converter.log
```

---

## 🆘 Troubleshooting

**Converter won't start?**
```bash
python --version
# Should be 3.8+
```

**Command not found?**
```bash
# Reinstall git
# Then retry git clone
```

**Can't find output?**
```bash
ls output/
# Make sure conversion finished without errors
# Check logs/converter.log
```

**Very slow conversion?**
- Reduce TEXTURE_SCALE in config.py
- Reduce SOUND_QUALITY
- Close other apps
- Use SSD instead of microSD (if possible)

---

## 📚 Learn More

After this guide, read:
- **[README.md](README.md)** - Full documentation
- **[COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)** - All commands
- **[EXAMPLES.md](EXAMPLES.md)** - More examples
- **[TERMUX_SETUP.md](TERMUX_SETUP.md)** - Android specific

---

## ✅ Final Checklist

After completing this guide:

- [ ] Installed Python, Git, FFmpeg
- [ ] Cloned GVerterx repository
- [ ] Installed all dependencies
- [ ] Placed Java pack in input/
- [ ] Successfully converted to Bedrock
- [ ] Found converted pack in output/
- [ ] Know how to use the converted pack

**Congratulations! You've successfully used GVerterx! 🎉**

---

## 🎯 Common Next Questions

**Q: Can I convert 10 packs at once?**
A: Yes! Place all in input/, then select "Convert All Packs"

**Q: Can I customize the conversion?**
A: Yes! Edit converter/config.py for settings

**Q: How long does conversion take?**
A: 30 sec - 10 min depending on pack size

**Q: Does it work on mobile/Termux?**
A: Yes! Full support. See [TERMUX_SETUP.md](TERMUX_SETUP.md)

**Q: Can I use converted pack on Java edition servers?**
A: No, only for Bedrock or GeyserMC servers

**Q: Is my pack backed up?**
A: Yes! Original in input/, converted in output/

---

**You're all set! Happy converting! 🚀**
