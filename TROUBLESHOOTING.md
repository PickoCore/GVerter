# GVerterx - Comprehensive Troubleshooting Guide

**Having problems? You're in the right place!**

Each issue includes:
- ✅ How to identify the problem
- ✅ Why it happens
- ✅ How to fix it
- ✅ How to prevent it

---

## 📋 Quick Problem Finder

**Select your error:**

- [Python not found](#python-not-found) - `'python' is not recognized`
- [Git not found](#git-not-found) - `git command not found`
- [ModuleNotFoundError](#modulenotfounderror) - `No module named 'rich'`
- [FFmpeg not found](#ffmpeg-not-found) - `FFmpeg not found`
- [Permission denied](#permission-denied) - `Permission denied` error
- [Converter won't start](#converter-wont-start) - Menu doesn't appear
- [Conversion too slow](#conversion-too-slow) - Taking forever
- [Out of memory](#out-of-memory) - Memory error during conversion
- [Storage full](#storage-full) - `No space left on device`
- [Output not created](#output-not-created) - No output folder
- [Termux specific](#termux-specific-issues) - Android problems

---

## 🔴 CRITICAL ISSUES

### Python not found

**Error Message:**
```
'python' is not recognized as an internal or external command
command not found: python
python: No such file or directory
```

**Why it happens:**
- Python not installed
- Python not added to PATH
- Using wrong command

**How to fix:**

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH" ✅
4. Finish installation
5. Restart Command Prompt
6. Try again: `python --version`

**If still not working:**
```bash
# Try python3 instead
python3 --version

# If works, use python3 for all commands:
python3 main.py
pip3 install -r requirements.txt
```

**macOS:**
```bash
# Check if installed
which python3

# If not, install via Homebrew
brew install python@3.10

# Verify
python3 --version
```

**Linux:**
```bash
# Install Python
sudo apt install python3 python3-pip -y

# Verify
python3 --version
```

**Termux:**
```bash
# Install Python
pkg install python -y

# Verify
python --version
```

**How to prevent:**
- Always use latest Python version
- Check "Add to PATH" during installation
- Verify with `python --version` after install

---

### Git not found

**Error Message:**
```
'git' is not recognized
command not found: git
git: command not found
```

**Why it happens:**
- Git not installed
- Not added to PATH

**How to fix:**

**Windows:**
1. Download from [git-scm.com](https://git-scm.com/)
2. Run installer
3. Follow defaults (Next → Finish)
4. Restart Command Prompt
5. Try: `git --version`

**macOS:**
```bash
brew install git
git --version
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install git -y

# Fedora
sudo dnf install git -y

# Arch
sudo pacman -Sy git

git --version
```

**Termux:**
```bash
pkg install git -y
git --version
```

**How to prevent:**
- Install before trying to clone
- Check `git --version` immediately after install

---

### ModuleNotFoundError

**Error Message:**
```
ModuleNotFoundError: No module named 'rich'
ModuleNotFoundError: No module named 'pydantic'
ImportError: cannot import name 'something'
```

**Why it happens:**
- Dependencies not installed
- Installed in wrong Python version
- Virtual environment issues

**How to fix:**

**Option 1: Fresh Install (Recommended)**
```bash
# Navigate to GVerterx folder
cd path/to/GVerterx

# Delete old installation (if any)
rm -rf venv
# Windows: rmdir venv /s /q

# Create fresh virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/macOS/Termux:
source venv/bin/activate

# Install fresh
pip install -r requirements.txt

# Run converter
python main.py
```

**Option 2: Force Reinstall**
```bash
# Direct reinstall
pip install --force-reinstall -r requirements.txt

# Upgrade all
pip install --upgrade -r requirements.txt

# Run again
python main.py
```

**Option 3: Check Installation**
```bash
# Check what's installed
pip list

# Should include: rich, pillow, pydantic, etc.

# If missing, install manually
pip install rich pillow pydantic pyyaml jsonschema python-dotenv tqdm
```

**How to prevent:**
- Don't skip the `pip install -r requirements.txt` step
- Use virtual environment (venv)
- Keep requirements.txt file safe

---

## 🟡 COMMON ISSUES

### FFmpeg not found

**Error Message:**
```
FFmpeg not found
ffmpeg: command not found
'ffmpeg' is not recognized
```

**Why it happens:**
- FFmpeg not installed (optional but recommended)
- Audio conversion will fail or be slower

**Impact:**
- Sound conversion works but slower
- Audio quality might be lower
- Still works without FFmpeg

**How to fix:**

**Windows:**
```bash
# Option 1: Chocolatey
choco install ffmpeg

# Option 2: Manual
# 1. Download from ffmpeg.org
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to PATH
# 4. Restart Command Prompt
# 5. Test: ffmpeg -version
```

**macOS:**
```bash
# Via Homebrew
brew install ffmpeg

# Verify
ffmpeg -version
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install ffmpeg -y

# Fedora
sudo dnf install ffmpeg -y

# Arch
sudo pacman -Sy ffmpeg

# Verify
ffmpeg -version
```

**Termux:**
```bash
pkg install ffmpeg -y
ffmpeg -version
```

**If you can't install:**
- Converter still works without it
- Sound conversion just slower
- Continue anyway: `python main.py`

**How to prevent:**
- Install before first conversion
- Check: `ffmpeg -version`

---

### Permission denied

**Error Message:**
```
Permission denied
./main.py: Permission denied
[Errno 13] Permission denied: 'input/MyPack'
```

**Why it happens:**
- File/folder doesn't have execute permission
- Trying to access restricted folder
- Windows/file ownership issue

**How to fix:**

**Linux/macOS/Termux:**
```bash
# Add execute permission
chmod +x main.py

# Add permission to folders
chmod -R 755 converter/
chmod -R 755 input/ output/

# Retry
python main.py
```

**Windows:**
- Usually not needed
- If happens: Right-click folder → Properties → Advanced → Edit Permissions

**How to prevent:**
- Run from folder you have access to
- Don't use system protected folders
- Use Downloads or Documents

---

### Converter won't start

**Error Message:**
- Menu doesn't appear
- Script seems to hang
- No response after running

**Why it happens:**
- Dependencies not installed properly
- Import error
- Missing required file

**How to fix:**

**Step 1: Check Python**
```bash
python --version
# Should be 3.8+
```

**Step 2: Check Dependencies**
```bash
python -c "import rich; print('✓ Rich OK')"
python -c "import pydantic; print('✓ Pydantic OK')"
python -c "import pillow; print('✓ Pillow OK')"

# If any fail, reinstall:
pip install --force-reinstall -r requirements.txt
```

**Step 3: Check File Exists**
```bash
ls main.py  # Linux/macOS
dir main.py  # Windows

# Should show main.py
```

**Step 4: Check with Debug**
```bash
python -v main.py
# Will show detailed import messages
```

**Step 5: Try from Different Location**
```bash
# Try from different folder
python /full/path/to/main.py
```

**How to prevent:**
- Use virtual environment
- Don't modify main.py
- Keep all project files together

---

### Conversion too slow

**Symptoms:**
- Stuck on "Converting Textures..."
- Taking 30+ minutes for medium pack
- High CPU usage but slow

**Why it happens:**
- Large texture files
- High resolution textures
- Slow storage (microSD card)
- Other apps using resources
- High texture quality settings

**How to fix:**

**Option 1: Reduce Texture Quality (Fastest)**
```bash
# Edit config
nano converter/config.py

# Change this line:
TEXTURE_SCALE = 0.5  # 50% of original size

# Retry conversion
python main.py
```

**Option 2: Reduce Audio Quality**
```bash
# Edit config
nano converter/config.py

# Change:
SOUND_QUALITY = 50  # Lower quality = faster

# Retry
python main.py
```

**Option 3: Skip Geyser Mapping**
```bash
# Edit config
nano converter/config.py

# Change:
ENABLE_GEYSER_MAPPING = False

# Retry
python main.py
```

**Option 4: Free Up Resources**
```bash
# Close other apps
# Kill background tasks
# For Termux: pkill -f "long_running_process"
# Retry
python main.py
```

**Option 5: Use Faster Storage**
- If using microSD: Move to internal storage
- Copy to faster location
- Retry

**Expected Times:**
- Small pack (50MB): 30 seconds
- Medium pack (200MB): 2 minutes  
- Large pack (500MB): 5-10 minutes
- Very large (1GB+): 15-30 minutes

**How to prevent:**
- Close other apps before conversion
- Don't use on slow storage
- Check disk speed: `time dd if=/dev/zero of=test.tmp bs=1M count=1024`

---

### Out of memory

**Error Message:**
```
MemoryError
Killed (SIGKILL)
Process killed by OOM killer
Out of memory error
```

**Why it happens:**
- Pack too large
- RAM too low
- Memory leak
- Running other memory-heavy apps

**How to fix:**

**Option 1: Reduce Texture Resolution**
```bash
# Edit converter/config.py
TEXTURE_SCALE = 0.25  # 25% size = 1/4 memory needed

python main.py
```

**Option 2: Free Up Memory**
```bash
# Close other apps
# Kill unnecessary processes
# For Termux:
free  # Check available memory
```

**Option 3: Convert in Parts**
```bash
# Extract pack manually
# Modify pack to be smaller
# Convert smaller version
# Combine outputs manually
```

**Option 4: Upgrade RAM**
- For long-term: Get device with more RAM
- Temporary: Use Linux swap

**How to prevent:**
- Don't run heavy apps during conversion
- Use TEXTURE_SCALE setting
- Check available memory first: `free` or `free -h`

---

### Storage full

**Error Message:**
```
No space left on device
[Errno 28] No space available
IOError: No space left
```

**Why it happens:**
- Output pack too large
- Temp files filling disk
- Logs consuming space

**How to fix:**

**Option 1: Clean Up**
```bash
# Delete old conversions
rm -rf output/old_pack_*

# Clean temp folder
rm -rf temp/*

# Clear pip cache
pip cache purge

# Clear system cache
# Linux: sudo sync && sudo echo 3 > /proc/sys/vm/drop_caches
```

**Option 2: Check Space**
```bash
# See available space
df -h

# See folder sizes
du -sh */
du -sh ./*

# Find large files
find . -size +100M
```

**Option 3: Move Locations**
```bash
# Move to different drive with more space
mv input/ /larger/drive/
mv output/ /larger/drive/
```

**Option 4: Reduce Resolution**
```bash
# Edit converter/config.py
TEXTURE_SCALE = 0.5

# This creates smaller output files
python main.py
```

**How to prevent:**
- Check space before conversion: `df -h`
- Clean regularly: `rm -rf temp/*`
- Use external drive for large packs

---

### Output not created

**Symptoms:**
- Converter says "Success"
- But no files in output/
- Folder missing

**Why it happens:**
- Conversion failed silently
- Output path issue
- Permission problem

**How to fix:**

**Step 1: Check Logs**
```bash
# View last lines
tail -20 logs/converter.log

# Search for errors
grep -i "error" logs/converter.log
grep -i "failed" logs/converter.log
```

**Step 2: Create Output Folder**
```bash
# Make sure folder exists
mkdir -p output

# Set permissions
chmod 755 output

# Retry
python main.py
```

**Step 3: Check Permissions**
```bash
# Check if can write
touch output/test.txt
rm output/test.txt

# If error, fix:
chmod -R 755 output
```

**Step 4: Try Different Location**
```bash
# Create output in different folder
mkdir -p ~/Downloads/gverter_output
# Edit main.py to use this folder
# Or copy output files there

# Retry
python main.py
```

**Step 5: Verbose Mode**
```bash
# Run with detailed output
python main.py -v

# Shows what's happening step-by-step
```

**How to prevent:**
- Check logs after every conversion
- Verify permissions on output folder
- Make sure disk has space

---

## 🤖 TERMUX-SPECIFIC ISSUES

### Termux: Storage permission denied

**Error:**
```
Permission denied
Cannot access ~/storage/downloads
```

**Why:**
- Storage permission not granted
- termux-setup-storage not run

**Fix:**
```bash
# Setup storage permissions
termux-setup-storage

# Grant permission when popup appears
# Try again:
cd ~/storage/downloads
ls
```

---

### Termux: Pip very slow

**Symptoms:**
- `pip install` takes 30+ minutes
- Download stalls
- Connection timeout

**Fix:**

**Option 1: Faster Mirror**
```bash
# Use Aliyun mirror (fastest for Asia)
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# Or Tsinghua mirror
pip install -i https://pypi.tsinghua.edu.cn/simple -r requirements.txt

# Or official but with timeout
pip install --default-timeout=1000 -r requirements.txt
```

**Option 2: Install individually**
```bash
# Instead of all at once
pip install --no-cache-dir rich
pip install --no-cache-dir pillow
pip install --no-cache-dir pydantic
# ... etc
```

**Option 3: Use offline**
```bash
# Download wheels on fast PC
pip download -r requirements.txt -d ./wheels

# Transfer wheels to Termux
# Then install:
pip install --no-index --find-links ./wheels -r requirements.txt
```

---

### Termux: Build tools error

**Error:**
```
error: command 'clang' not found
ERROR: Could not build wheels for ...
```

**Why:**
- Build tools not installed

**Fix:**
```bash
# Install build tools
pkg install build-essential clang pkg-config -y

# Retry
pip install -r requirements.txt
```

---

### Termux: Cannot write to input/output

**Error:**
```
Permission denied
Cannot create file
```

**Why:**
- Storage permissions not granted

**Fix:**
```bash
# Grant storage access
termux-setup-storage

# Navigate to shared storage
cd ~/storage/shared

# Create folders
mkdir -p input output

# Or use absolute path
cd ~/storage/downloads/GVerterx
mkdir -p input output

# Retry
python main.py
```

---

## 🔍 DIAGNOSTIC COMMANDS

**Use these to diagnose problems:**

```bash
# Check Python version
python --version

# Check installed packages
pip list
pip show rich

# Check available memory
free -h

# Check disk space
df -h
du -sh */

# Check file permissions
ls -la main.py
ls -la converter/

# Check logs
tail -20 logs/converter.log
tail -f logs/converter.log

# Monitor during conversion
watch -n 1 'du -sh output/'

# Check active processes
ps aux | grep python
ps aux | grep ffmpeg

# Check network (if download fails)
ping github.com
```

---

## 🆘 WHEN ALL ELSE FAILS

**If nothing above works:**

1. **Gather information:**
   ```bash
   python --version > debug.txt
   pip list >> debug.txt
   uname -a >> debug.txt  # Linux/macOS/Termux
   systeminfo >> debug.txt  # Windows
   tail -50 logs/converter.log >> debug.txt
   ```

2. **Create fresh install:**
   ```bash
   cd /tmp  # or temp folder
   rm -rf GVerterx
   git clone https://github.com/PickoCore/GVerterx.git
   cd GVerterx
   pip install -r requirements.txt
   python main.py
   ```

3. **Report issue on GitHub:**
   - Include debug.txt
   - Describe what you did
   - Include error message
   - Include OS and Python version

---

## 📞 Getting Help

**Before creating issue:**

1. ✅ Read this troubleshooting guide
2. ✅ Check logs/converter.log
3. ✅ Try recommended fixes
4. ✅ Search GitHub issues
5. ✅ Create detailed issue if still broken

**When creating issue include:**
- Error message (complete, full output)
- Your OS and Python version
- Steps to reproduce
- Logs from logs/converter.log
- What you already tried

---

**Happy Converting! 🎉**

If you need more help, read other documentation:
- [README.md](README.md) - Features
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Installation guide
- [TERMUX_SETUP.md](TERMUX_SETUP.md) - Android setup
- [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md) - Visual walkthrough
