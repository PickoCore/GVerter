# Setup Guide - Termux (Android)

Guide lengkap untuk menjalankan Minecraft Resource Pack Converter di Termux.

## 📱 Prerequisites

1. **Termux App** - Download dari F-Droid atau Google Play
2. **Internet Connection** - Untuk download dependencies
3. **Storage Access** - Enable storage permissions

## ⚙️ Installation Steps

### 1. Update Termux Package Manager
```bash
pkg update
pkg upgrade -y
```

### 2. Install Python & Dependencies
```bash
# Install Python 3
pkg install python -y

# Install build tools (untuk compile some packages)
pkg install build-essential -y

# Install ffmpeg (untuk audio conversion)
pkg install ffmpeg -y

# Install git (optional, untuk clone repo)
pkg install git -y
```

### 3. Setup Storage Access
```bash
# Grant storage permission
termux-setup-storage

# Navigate to shared storage
cd ~/storage/downloads
# atau
cd ~/storage/shared
```

### 4. Clone atau Download Project

**Option A - Clone from GitHub:**
```bash
cd ~/storage/downloads
git clone <repo-url> minecraft-converter
cd minecraft-converter
```

**Option B - Manual Transfer:**
1. Download converter files ke Windows/Mac
2. Transfer via FTP atau copy ke Termux storage
3. `cd` ke folder project

### 5. Install Python Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Atau gunakan UV jika tersedia
# uv install
```

## 🚀 Running the Converter

### Interactive Mode (Recommended)
```bash
# Navigate to project directory
cd ~/path/to/minecraft-converter

# Run converter
python3 main.py
```

**Follow the menu:**
1. Place Java resource pack di folder `input/`
2. Run `python3 main.py`
3. Select pack dari list
4. Configure options
5. Wait for conversion
6. Output di `output/` folder

### Command Line Mode
```bash
# Basic conversion
python3 main.py my_pack

# With verbose logging
python3 main.py my_pack -v

# Convert .zip file
python3 main.py pack.zip
```

## 📁 Folder Structure di Termux

```
~/storage/downloads/minecraft-converter/
├── main.py
├── converter/
│   ├── config.py
│   ├── core/
│   └── ui/
├── input/                    # Put your Java packs here
├── output/                   # Converted Bedrock packs here
├── logs/                     # Conversion logs
└── README.md
```

## 📤 Using Converted Packs

### Option 1: Local Bedrock (Phone)
```bash
# After conversion, copy output pack
cp -r output/my_pack_bedrock ~/storage/downloads/

# Import into Minecraft:
# 1. Open Minecraft
# 2. Settings → Resource Packs
# 3. Import folder → select converted pack
# 4. Activate
```

### Option 2: GeyserMC Server (Remote)
```bash
# Copy Geyser mapping files
cd output/my_pack_bedrock

# Transfer ke server via:
# - SCP/SFTP
# - Cloud storage (Google Drive, Dropbox)
# - USB cable

# Server admin puts in GeyserMC/packs/ folder
```

### Option 3: Share with Others
```bash
# Create zip for distribution
cd output
zip -r my_pack_bedrock.zip my_pack_bedrock/

# Share zip file dengan teman/server admin
```

## 🔧 Environment Setup

### Increase Python Memory (jika conversion lambat)
```bash
# Before running converter
export PYTHONHASHSEED=0
export MALLOC_TRIM_THRESHOLD_=128000
export MALLOC_MMAP_THRESHOLD_=131072

python3 main.py my_pack
```

### Create Termux Shortcut
```bash
# Create startup script
nano ~/start-converter.sh

# Paste:
#!/bin/bash
cd ~/storage/downloads/minecraft-converter
python3 main.py

# Save: Ctrl+X, Y, Enter

# Make executable
chmod +x ~/start-converter.sh

# Run:
bash ~/start-converter.sh
```

## ⚠️ Troubleshooting

### "Permission Denied"
```bash
# Grant execute permission
chmod +x main.py
chmod -R 755 converter/
```

### "Module not found"
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

### "FFmpeg not found"
```bash
# Install ffmpeg
pkg install ffmpeg -y

# Or skip audio conversion (OGG files only)
```

### Storage Access Issues
```bash
# Check permissions
ls -la ~/storage/

# If error, run:
termux-setup-storage
```

### Pack not Found
```bash
# Check input folder exists
ls -la input/

# Make sure pack.mcmeta di root folder
ls -la input/my_pack/pack.mcmeta
```

### Slow Conversion
```bash
# Free up memory
termux-wake-lock  # Keep CPU awake

# Check disk space
df -h

# Monitor progress
tail -f logs/*.log
```

## 📊 Tips & Tricks

### Batch Convert Multiple Packs
```bash
# Create script
nano batch_convert.sh

# Paste:
#!/bin/bash
for pack in input/*; do
    if [ -d "$pack" ]; then
        echo "Converting $(basename $pack)..."
        python3 main.py "$(basename $pack)"
    fi
done

# Run:
bash batch_convert.sh
```

### Automate with Cron (if available)
```bash
# Create cron job
pkg install cronie -y
crontab -e

# Add line (daily at 2 AM):
# 0 2 * * * /data/data/com.termux/files/home/start-converter.sh
```

### Monitor Resources
```bash
# Watch system resources
top

# Or
htop  # if installed (pkg install htop -y)
```

### Debug Issues
```bash
# Run with verbose logging
python3 main.py my_pack -v

# Check last log
tail -n 50 logs/*.log
```

## 🌐 Network Features

### Access from Computer
```bash
# Share via Python HTTP server
cd output
python3 -m http.server 8000

# Access from computer: http://<termux-ip>:8000
```

### SSH Transfer
```bash
# Start SSH server (if installed)
sshd

# From computer:
scp -r converted_pack user@<phone-ip>:/path/to/server/packs/
```

## 💾 Backup & Restore

### Backup Converted Packs
```bash
# Create archive
tar -czf packs_backup.tar.gz output/

# Save to cloud storage or computer
```

### Restore Packs
```bash
# Extract archive
tar -xzf packs_backup.tar.gz

# Packs restored to output/ folder
```

## 📋 Termux-Specific Notes

- **Home Directory**: `/data/data/com.termux/files/home/`
- **Storage**: `/storage/emulated/0/` or `/sdcard/`
- **Cache**: `~/.cache/` untuk temp files
- **Python Path**: Termux uses own Python build
- **File Permissions**: May need `chmod` after file transfer

## 🎮 Final Steps

1. **Verify Conversion**
   ```bash
   ls -la output/my_pack_bedrock/
   cat output/my_pack_bedrock/manifest.json
   ```

2. **Test with Minecraft**
   - Import to Bedrock locally, atau
   - Give to GeyserMC server admin

3. **Share Success**
   - Enjoy custom textures/sounds!
   - Share converted pack dengan community

## 📞 Support

If issues occur:
1. Check logs in `logs/` folder
2. Verify input pack format
3. Ensure all dependencies installed
4. Try running with `-v` flag for verbose output

---

**Last Updated**: 2024-03-09  
**Tested On**: Termux (Android 10+)
