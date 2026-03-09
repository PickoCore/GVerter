# Examples & Use Cases

## Example 1: Simple Resource Pack Conversion

### Setup
```bash
# Persiapkan folder structure
mkdir -p input output

# Copy Java resource pack
cp -r ~/Downloads/MyCustomPack input/

# Verify structure
ls -la input/MyCustomPack/pack.mcmeta
```

### Conversion
```bash
# Interactive mode
python3 main.py

# Select: MyCustomPack
# Options: Default (Geyser enabled, no verbose)
# Wait for completion
```

### Result
```
output/MyCustomPack_bedrock/
├── manifest.json
├── textures/
│   ├── blocks/
│   ├── items/
│   └── ui/
├── sounds/
├── models/
├── geyser_custom_items.json
└── _conversion_metadata.json
```

---

## Example 2: Geyser Server Integration

### Setup
```bash
# Java pack dengan custom items
python3 main.py CustomItemsPack -v

# Output di output/CustomItemsPack_bedrock/
```

### Server Setup
```bash
# Copy ke Geyser server
scp -r output/CustomItemsPack_bedrock/ \
    admin@server:/opt/geyser/packs/

# Server restart Geyser
# docker restart geyser
# atau manually: systemctl restart geyser
```

### Result
✅ Bedrock players dapat lihat custom items dan blocks  
✅ Automatic download ke Bedrock clients  
✅ Full compatibility dengan Java players

---

## Example 3: Batch Processing Multiple Packs

### Script
```bash
# batch_convert.sh
#!/bin/bash

INPUT_DIR="input"
OUTPUT_DIR="output"

for pack_dir in "$INPUT_DIR"/*; do
    if [ -d "$pack_dir" ] && [ -f "$pack_dir/pack.mcmeta" ]; then
        pack_name=$(basename "$pack_dir")
        echo "Converting: $pack_name"
        python3 main.py "$pack_name" -v
        
        if [ $? -eq 0 ]; then
            echo "✓ $pack_name completed"
        else
            echo "✗ $pack_name failed"
        fi
        
        echo ""
    fi
done

echo "Batch conversion completed!"
```

### Usage
```bash
chmod +x batch_convert.sh
./batch_convert.sh
```

---

## Example 4: Custom Item Mapping

### Input Pack Structure
```
MyPack/
├── pack.mcmeta
└── assets/minecraft/
    ├── models/item/
    │   ├── diamond_sword.json
    │   ├── custom_item_1.json
    │   └── custom_item_2.json
    ├── textures/item/
    │   ├── diamond_sword.png
    │   ├── custom_item_1.png
    │   └── custom_item_2.png
    └── sounds/
```

### Custom Item JSON
```json
{
  "parent": "item/handheld",
  "textures": {
    "layer0": "item/custom_item_1"
  },
  "overrides": [
    {
      "predicate": {
        "custom_model_data": 1
      },
      "model": "item/custom_item_1"
    }
  ]
}
```

### Conversion
```bash
python3 main.py MyPack -v
```

### Output Files
```
output/MyPack_bedrock/
├── geyser_custom_items.json
│   ├── "geyser:custom_item_1" → custom item definition
│   └── "geyser:custom_item_2" → custom item definition
├── _custom_model_data.json
│   ├── Mappings untuk custom model data
└── models/item/
    ├── custom_item_1.json → Converted model
```

### Geyser Mapping
```json
{
  "geyser:custom_item_1": {
    "name": "Custom Item 1",
    "display_name": "Custom Item 1",
    "icon": "custom_item_1",
    "stack_size": 64,
    "model": {
      "type": "geometry",
      "geometry": "Geometry.custom_item_1"
    },
    "textures": {
      "layer0": "item/custom_item_1"
    }
  }
}
```

---

## Example 5: Texture Optimization

### High Resolution Pack
```bash
# Pack dengan 256x textures
input/HighResPack/
├── assets/minecraft/textures/
│   ├── blocks/stone.png (256x256)
│   ├── items/diamond_sword.png (256x256)
└── pack.mcmeta (format 32)
```

### Conversion
```bash
# Automatic downscaling untuk Bedrock compatibility
python3 main.py HighResPack

# Converter akan:
# - Detect 256x resolution
# - Scale down ke max 512x (Bedrock limit)
# - Optimize file size
# - Maintain quality
```

### Output
```
output/HighResPack_bedrock/
└── textures/
    ├── blocks/stone.png (optimized)
    └── items/diamond_sword.png (optimized)
```

---

## Example 6: Sound Event Mapping

### Java Sounds Definition
```json
{
  "custom.magic_spell": {
    "sounds": [
      "custom/spell_cast_1",
      "custom/spell_cast_2"
    ],
    "subtitle": "subtitles.custom.magic_spell"
  },
  "block.custom_block.break": {
    "sounds": [
      "block/custom_break"
    ]
  }
}
```

### Conversion
```bash
python3 main.py SoundPack -v
```

### Generated Bedrock Mappings
```json
{
  "sound_definitions": {
    "custom.magic_spell": {
      "sounds": [
        "sounds/custom/spell_cast_1",
        "sounds/custom/spell_cast_2"
      ]
    },
    "block.custom_block.break": {
      "sounds": [
        "sounds/block/custom_break"
      ]
    }
  }
}
```

---

## Example 7: Language File Conversion

### Java Language Files
```
assets/minecraft/lang/
├── en_us.lang
├── de_de.lang
└── ja_jp.lang
```

### en_us.lang Content
```
# Custom translations
item.custom.diamond_sword=Diamond Sword
block.custom.magic_block=Magic Block
subtitles.custom.magic_spell=Magic spell cast
```

### Conversion
```bash
python3 main.py LanguagePack
```

### Output Structure
```
output/LanguagePack_bedrock/
└── texts/
    ├── en_us/
    │   └── en_us.json
    ├── de_de/
    │   └── de_de.json
    ├── ja_jp/
    │   └── ja_jp.json
    └── language_names.json
```

### Converted JSON
```json
{
  "language.code": "en_us",
  "language.name": "English (US)",
  "item.custom.diamond_sword": "Diamond Sword",
  "block.custom.magic_block": "Magic Block",
  "subtitles.custom.magic_spell": "Magic spell cast"
}
```

---

## Example 8: Troubleshooting & Logs

### Enable Verbose Logging
```bash
python3 main.py MyPack -v
```

### Check Logs
```bash
# Latest log
tail -f logs/*.log

# Specific conversion
ls logs/MyPack*.log

# View full log
cat logs/MyPack_20240309_150530.log
```

### Log Content
```
[2024-03-09 15:05:30] [INFO] Starting conversion: MyPack
[2024-03-09 15:05:31] [INFO] ► Converting textures...
[2024-03-09 15:05:33] [DEBUG] Copied texture: stone.png
[2024-03-09 15:05:33] [INFO] ✓ Textures converted: 45 files
[2024-03-09 15:05:34] [INFO] ► Converting sounds...
[2024-03-09 15:05:35] [WARNING] ffmpeg not available, skipping audio conversion
[2024-03-09 15:05:36] [INFO] ► Creating Geyser mappings...
[2024-03-09 15:05:37] [INFO] ✓ Geyser mappings created
[2024-03-09 15:05:37] [INFO] CONVERSION SUMMARY
[2024-03-09 15:05:37] [INFO] Textures: 45, Sounds: 12, Models: 8
```

---

## Example 9: Geyser Server Configuration

### GeyserMC Config
```yaml
# geyser-config.yml
remote:
  address: java.server.address
  port: 25565

remote-port: 25566

resource-packs:
  packs:
    - packs/MyPack_bedrock
  pack-encapsulation: true

custom:
  commands:
    enabled: true
    
custom-items: true
custom-blocks: true

# Resource pack settings
bedrock:
  auth-type: offline
  compress-world-data: false
```

### Result
- Bedrock players mendapat resource pack otomatis
- Custom items terlihat tanpa manual setup
- Seamless Java ↔ Bedrock experience

---

## Example 10: Performance Optimization

### Large Resource Pack
```bash
# Monitor during conversion
watch -n 1 'ps aux | grep python3'

# Run dengan optimized settings
PYTHONHASHSEED=0 python3 main.py LargePack -v

# Check output size
du -sh output/LargePack_bedrock/
```

### Tips
- Convert textures dulu (largest)
- Skip sound conversion jika tidak perlu
- Use verbose flag untuk progress tracking
- Monitor disk space sebelum conversion

---

## Quick Reference

| Task | Command |
|------|---------|
| Interactive mode | `python3 main.py` |
| Convert pack | `python3 main.py PackName` |
| Verbose output | `python3 main.py PackName -v` |
| View logs | `tail -f logs/*.log` |
| List packs | `ls input/` |
| Check output | `ls output/` |
| Create zip | `zip -r pack.zip output/PackName_bedrock/` |
| Clean temp | `rm -rf temp/*` |

---

**More examples coming soon!**  
Have a specific use case? Check the documentation or open an issue.
