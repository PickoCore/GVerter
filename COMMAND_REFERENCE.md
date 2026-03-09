# GVerterx - Command Reference Card

Quick reference untuk semua command penting.

---

## 🚀 Quick Start (Copy-Paste)

### Windows/macOS/Linux
```bash
# 1. Clone
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx

# 2. Install
pip install -r requirements.txt

# 3. Run
python main.py
```

### Termux (Android)
```bash
# 1. Setup
pkg update && pkg upgrade -y
pkg install python git ffmpeg build-essential -y
termux-setup-storage

# 2. Clone
cd ~/storage/downloads
git clone https://github.com/PickoCore/GVerterx.git
cd GVerterx

# 3. Install
pip install -r requirements.txt

# 4. Run
python main.py
```

---

## 📂 File Management

```bash
# List input packs
ls input/

# List output packs
ls output/

# Copy pack to input
cp ~/Downloads/MyPack.zip input/

# Copy converted pack
cp -r output/MyPack ~/Desktop/

# Check pack size
du -sh input/MyPack
du -sh output/MyPack_bedrock

# Delete old pack
rm -rf input/OldPack

# Clean temp files
rm -rf temp/*
```

---

## ▶️ Running Converter

```bash
# Interactive mode (RECOMMENDED)
python main.py

# Verbose logging
python main.py -v

# Specific pack
python main.py MyPack

# Convert zip file
python main.py pack.zip

# Skip Geyser mapping
python main.py --no-geyser
```

---

## 🔧 Configuration

```bash
# Edit config
nano converter/config.py
vim converter/config.py

# Edit Geyser mappings
nano converter/core/geyser_mapper.py

# View current config
cat converter/config.py

# Check texture mappings
grep -n "TEXTURE_MAPPINGS" converter/config.py
```

---

## 📊 Monitoring & Logging

```bash
# View recent logs
tail -20 logs/converter.log

# Follow logs real-time
tail -f logs/converter.log

# See all logs
cat logs/converter.log

# Search in logs
grep "ERROR" logs/converter.log
grep "Texture" logs/converter.log

# Count conversions
wc -l logs/converter.log
```

---

## 🐛 Troubleshooting Commands

```bash
# Check Python version
python --version

# Check pip packages
pip list

# Check FFmpeg
ffmpeg -version

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Upgrade all packages
pip install --upgrade -r requirements.txt

# Create clean environment
python -m venv venv
source venv/bin/activate  # Linux/macOS/Termux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 📁 Navigation (Termux)

```bash
# Navigate to project
cd ~/storage/downloads/GVerterx

# Go to input folder
cd input/

# Go to output folder
cd output/

# Back to project root
cd ..

# Home directory
cd ~

# Downloads
cd ~/storage/downloads

# List current folder
ls -la
```

---

## 🔄 Git Commands

```bash
# Update from GitHub
git pull origin main

# Check status
git status

# View commit history
git log --oneline

# Create new branch (untuk eksperimen)
git checkout -b my-feature

# Switch back to main
git checkout main
```

---

## 📦 Package Management

```bash
# Install package
pip install <package-name>

# Uninstall package
pip uninstall <package-name>

# Check package version
pip show <package-name>

# Upgrade package
pip install --upgrade <package-name>

# Install exact version
pip install <package-name>==1.2.3

# Reinstall all
pip install -r requirements.txt --force-reinstall
```

---

## 🎯 Common Workflows

### Convert Single Pack
```bash
cd GVerterx
cp ~/Downloads/MyPack.zip input/
python main.py
# Select option 1
# Wait
# Check output/
```

### Convert Multiple Packs
```bash
cd GVerterx
cp ~/Downloads/Pack1.zip input/
cp ~/Downloads/Pack2.zip input/
cp ~/Downloads/Pack3.zip input/
python main.py
# Select option 1 (Convert All)
```

### Deploy to Server
```bash
cd GVerterx/output
zip -r MyPack.zip MyPack_bedrock/
scp MyPack.zip user@server:/plugins/geyser/packs/
# Server reload geyser
```

### Share with Friends
```bash
cd GVerterx/output
zip -r MyPack.zip MyPack_bedrock/
cp MyPack.zip ~/Downloads/
# Share MyPack.zip
```

### Customize Config
```bash
nano GVerterx/converter/config.py
# Edit SOUND_QUALITY, TEXTURE_SCALE, etc.
# Save and exit
python main.py
```

---

## 🔌 Environment Variables

```bash
# Set temp directory
export TMPDIR=/tmp

# Increase memory limit
export MALLOC_TRIM_THRESHOLD_=128000

# Disable GPU acceleration
export CUDA_VISIBLE_DEVICES=

# Set Python options
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
```

---

## 📱 Termux Specific

```bash
# Check storage access
ls ~/storage/downloads/

# Re-setup storage
termux-setup-storage

# Check available space
df -h

# Kill long-running process
ps aux
kill <PID>

# Install missing tool
apt search <tool-name>
pkg install <tool-name>

# Clear cache
pkg clean
rm -rf ~/.cache/pip
```

---

## 📊 Performance Tweaks

```bash
# Lower texture quality (faster)
# Edit converter/config.py:
TEXTURE_SCALE = 0.5

# Lower sound quality (faster)
SOUND_QUALITY = 50

# Skip Geyser mapping (faster)
ENABLE_GEYSER_MAPPING = False

# Use single thread
export OMP_NUM_THREADS=1
```

---

## 🆘 Emergency Commands

```bash
# Check if converter running
ps aux | grep main.py

# Kill stuck process
pkill -f "python main.py"

# Clear all temp files
rm -rf temp/*

# Reset to clean state
git checkout converter/config.py

# Full clean install
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Help Commands

```bash
# View this reference
cat COMMAND_REFERENCE.md

# View main readme
cat README.md

# View quick start
cat QUICKSTART.md

# View examples
cat EXAMPLES.md

# View architecture
cat ARCHITECTURE.md

# View Termux setup
cat TERMUX_SETUP.md
```

---

## 💡 Pro Tips

### Tip 1: Alias untuk command panjang
```bash
# Add to ~/.bashrc or ~/.zshrc
alias gverter="cd ~/storage/downloads/GVerterx && python main.py"

# Then just type:
gverter
```

### Tip 2: Batch convert script
```bash
#!/bin/bash
cd ~/storage/downloads/GVerterx
for pack in input/*.zip; do
    python main.py "$pack"
done
```

### Tip 3: Monitor multiple terminals
```bash
# Terminal 1: Run converter
python main.py

# Terminal 2: Monitor logs
tail -f logs/converter.log

# Terminal 3: Check progress
ls -lah output/
```

### Tip 4: Backup before editing config
```bash
cp converter/config.py converter/config.py.backup
# Edit config.py
# If problems:
cp converter/config.py.backup converter/config.py
```

### Tip 5: Check what changed
```bash
git diff converter/config.py
# See changes before they're committed
```

---

**Happy Converting! 🎉**

For more help, read the full documentation in README.md or EXAMPLES.md
