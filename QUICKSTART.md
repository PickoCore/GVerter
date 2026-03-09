# Quick Start Guide - 5 Minutes to Convert

## 1️⃣ Install (1 minute)

```bash
# Clone/Download project
cd minecraft-pack-converter

# Install dependencies
pip install -r requirements.txt
# Or: pip install click rich pillow pydantic pyyaml jsonschema python-dotenv tqdm
```

## 2️⃣ Prepare Pack (30 seconds)

```bash
# Put your Java resource pack here
cp ~/Downloads/MyPack input/

# Or if it's a ZIP
cp ~/Downloads/MyPack.zip input/
```

## 3️⃣ Run Converter (2 minutes)

```bash
# Interactive mode (EASIEST)
python3 main.py
```

**Then:**
1. Select your pack number
2. Answer 2-3 simple questions (defaults OK)
3. Watch it convert (colorful progress bars!)
4. Done! ✅

## 4️⃣ Get Your Pack (30 seconds)

```bash
# Find converted pack
ls output/

# Copy to Minecraft (Windows example)
xcopy output\MyPack_bedrock %APPDATA%\.minecraft\resource_packs\

# Or on Mac/Linux
cp -r output/MyPack_bedrock ~/.minecraft/resource_packs/
```

## 5️⃣ Use in Minecraft!

1. Open Minecraft
2. Settings → Resource Packs
3. Activate your converted pack ✅

---

## 🎮 For GeyserMC Server

```bash
# Convert pack
python3 main.py MyPack

# Copy to server
scp -r output/MyPack_bedrock admin@server:/opt/geyser/packs/

# Restart Geyser
# (Server admin does this)

# Done! Bedrock players get it automatically ✅
```

---

## 📱 For Termux (Android)

```bash
# Install Python
pkg install python ffmpeg -y

# Setup project
pip install -r requirements.txt

# Place pack in input/
# Run converter (same as above)
python3 main.py
```

---

## ⌨️ Command Line Mode (Advanced)

```bash
# Convert specific pack
python3 main.py MyPack

# With verbose logging
python3 main.py MyPack -v

# Convert ZIP file
python3 main.py MyPack.zip

# Convert multiple
python3 main.py Pack1 && python3 main.py Pack2
```

---

## 📊 What Gets Converted

| Asset | From | To | Status |
|-------|------|-----|--------|
| Textures | PNG, JPG | Bedrock PNG | ✅ |
| Sounds | OGG, WAV, MP3 | Bedrock OGG | ✅ |
| Models | JSON | Bedrock JSON | ✅ |
| Fonts | TTF, OTF | Bedrock | ✅ |
| Languages | .lang | JSON | ✅ |
| Custom Items | JSON | Geyser | ✅ |
| Custom Blocks | JSON | Geyser | ✅ |

---

## ✨ Features Included

✅ Texture conversion (PNG, JPG → optimized)  
✅ Sound mapping (OGG, WAV, MP3 → OGG)  
✅ Model conversion (JSON)  
✅ Font & language support  
✅ **Geyser integration** (full support!)  
✅ Automatic manifest  
✅ Detailed logging  
✅ Beautiful colored UI  

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Pack not found" | Make sure pack is in `input/` folder |
| "No Python" | Install: `pip install -r requirements.txt` |
| Output doesn't show | Check: `ls output/` |
| Minecraft can't find pack | Check: Resource Packs folder path correct |
| Need help | Run with `-v`: `python3 main.py pack -v` |

---

## 📂 Output Structure

```
output/MyPack_bedrock/
├── manifest.json (Bedrock metadata)
├── textures/ (converted textures)
├── sounds/ (converted sounds)
├── models/ (converted models)
├── texts/ (language files)
├── geyser_*.json (Geyser mappings)
└── _conversion_metadata.json
```

---

## 🎯 Typical Workflow

```
1. Place Java pack in input/
            ↓
2. Run: python3 main.py
            ↓
3. Select pack from list
            ↓
4. Choose options (or press Enter for defaults)
            ↓
5. Converter runs...
            ↓
6. Find converted pack in output/
            ↓
7. Copy to Minecraft resource packs folder
            ↓
8. Activate in Minecraft
            ↓
9. Enjoy! 🎮
```

---

## 💡 Pro Tips

1. **Batch convert** - Put multiple packs in input/, run multiple times
2. **High resolution** - Converter auto-scales 256x textures down to fit Bedrock
3. **Verbose mode** - Use `-v` to see detailed conversion process
4. **Check logs** - `tail -f logs/*.log` to monitor real-time
5. **Audio** - Install ffmpeg for MP3→OGG conversion
6. **Termux** - Works great on Android! See TERMUX_SETUP.md
7. **GeyserMC** - Perfect for servers (full Java/Bedrock compatibility)

---

## 📚 Learn More

- **README.md** - Full documentation
- **EXAMPLES.md** - Detailed examples
- **TERMUX_SETUP.md** - Android guide
- **PROJECT_SUMMARY.md** - Technical details

---

## ❓ FAQ

**Q: Will my pack work in vanilla Bedrock?**  
A: Yes! Converted to Bedrock format with auto-generated manifest.

**Q: What about GeyserMC?**  
A: Fully supported! Custom items/blocks included automatically.

**Q: Can I convert multiple packs?**  
A: Yes! Put them in input/ and run converter for each.

**Q: What about custom models?**  
A: Converted to Bedrock format (some limitations due to Bedrock).

**Q: How long does it take?**  
A: Minutes for typical packs. Check progress with colors!

---

## 🚀 Ready to Convert?

```bash
# ONE COMMAND to start:
python3 main.py
```

**That's it!** Follow the interactive menu. 🎉

---

Need help? Check logs or read full documentation!

Happy converting! 🎮✨
