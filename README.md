# Minecraft Resource Pack Converter
## Java Edition → Bedrock Edition with GeyserMC Support

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)

Converter komprehensif untuk mengkonversi Minecraft Java Edition resource packs ke Bedrock Edition format dengan full support untuk GeyserMC.

## ✨ Fitur Utama

### Konversi Lengkap
- ✅ **Texture Conversion**: PNG, JPG → Bedrock PNG format
- ✅ **Sound Conversion**: OGG, WAV, MP3 → Bedrock OGG format
- ✅ **Model Conversion**: JSON models → Bedrock format
- ✅ **Font & Language**: TTF fonts dan .lang files → Bedrock format
- ✅ **UI/GUI**: Resource pack GUI files → Bedrock UI format

### Geyser Integration
- ✅ **Custom Items Mapping**: Buat custom item definitions untuk GeyserMC
- ✅ **Custom Blocks Mapping**: Custom block definitions dengan full properties
- ✅ **Item/Block ID Mapping**: Otomatis map Java IDs ke Bedrock IDs
- ✅ **Geyser Extensions**: Generate Geyser extension files

### Fitur Lanjutan
- ✅ **Automatic Manifest Generation**: Bedrock manifest.json dibuat otomatis
- ✅ **Resolution Optimization**: Texture upscaling/downscaling support
- ✅ **Audio Conversion**: Otomatis convert audio ke format Bedrock
- ✅ **Logging System**: Detailed logging untuk troubleshooting
- ✅ **Batch Processing**: Convert multiple packs (extensible)

## 📋 Requirements

### System Requirements
- Python 3.8+
- Linux/macOS/Windows (tested on all platforms)
- 2GB RAM minimum

### Python Dependencies
```
click>=8.1.0          # CLI framework
rich>=13.0.0          # Terminal UI
pillow>=10.0.0        # Image processing
pydantic>=2.0.0       # Data validation
pyyaml>=6.0           # YAML parsing
jsonschema>=4.0       # JSON validation
python-dotenv>=1.0.0  # Environment variables
tqdm>=4.66.0          # Progress bars
```

### Optional Dependencies
- `ffmpeg` - Untuk audio conversion (OGG/WAV/MP3)

## 🚀 Quick Start

### 1. Setup
```bash
# Clone atau download project
cd minecraft-pack-converter

# Install dependencies (jika belum)
pip install -r requirements.txt

# Atau menggunakan UV
uv install
```

### 2. Persiapkan Resource Pack
```bash
# Copy Java resource pack ke folder 'input'
# - Bisa folder dengan structure lengkap, atau
# - Bisa .zip file dari resource pack

# Contoh struktur:
input/
  my_custom_pack/
    pack.mcmeta
    assets/
      minecraft/
        textures/
        sounds/
        models/
        ...
```

### 3. Jalankan Converter

#### Interactive Mode (Recommended)
```bash
python3 main.py
```

Menu akan muncul:
1. Pilih resource pack dari list
2. Configure options (Geyser, verbose, dll)
3. Converter akan berjalan otomatis
4. Output akan disimpan di `output/` folder

#### Command Line Mode
```bash
# Convert specific pack
python3 main.py my_pack

# Dengan verbose logging
python3 main.py my_pack -v

# Convert .zip file
python3 main.py my_pack.zip
```

### 4. Output
Hasil konversi akan tersimpan di:
```
output/
  my_pack_bedrock/
    manifest.json
    textures/
    sounds/
    models/
    geyser_custom_items.json
    geyser_custom_blocks.json
    geyser_item_mappings.json
    geyser_config.json
    _conversion_metadata.json
    ...
```

## 📖 Dokumentasi Lengkap

### File Structure
```
minecraft-pack-converter/
├── main.py                    # Entry point
├── converter/
│   ├── config.py             # Konfigurasi global
│   ├── core/
│   │   ├── base_converter.py          # Base class
│   │   ├── texture_converter.py       # Texture conversion
│   │   ├── sound_converter.py         # Sound conversion
│   │   ├── model_converter.py         # Model conversion
│   │   ├── font_converter.py          # Font conversion
│   │   ├── geyser_mapper.py           # Geyser mappings
│   │   └── resource_pack_converter.py # Master converter
│   └── ui/
│       └── cli.py                     # Rich CLI interface
├── input/                    # Input folder untuk Java packs
├── output/                   # Output folder untuk Bedrock packs
├── temp/                     # Temporary files
├── logs/                     # Conversion logs
└── requirements.txt          # Python dependencies
```

### Conversion Process

```
1. VALIDATION
   ├─ Check pack.mcmeta exists
   ├─ Validate JSON format
   └─ Read metadata

2. TEXTURE CONVERSION
   ├─ Scan assets/minecraft/textures/
   ├─ Convert paths (block/ → blocks/)
   ├─ Process images (PNG optimization)
   ├─ Create texture mappings
   └─ Save terrain_texture.json, item_texture.json

3. SOUND CONVERSION
   ├─ Scan assets/minecraft/sounds/
   ├─ Convert audio formats (→ OGG)
   ├─ Map sound events
   └─ Create sound_definitions.json

4. MODEL CONVERSION
   ├─ Parse JSON models
   ├─ Convert texture paths
   ├─ Map predicates
   └─ Extract custom model data

5. FONT & LANGUAGE
   ├─ Copy font files
   ├─ Convert .lang files
   ├─ Create language metadata
   └─ Setup texts/

6. GEYSER MAPPING
   ├─ Create custom_items.json
   ├─ Create custom_blocks.json
   ├─ Create item_mappings.json
   ├─ Create block_mappings.json
   └─ Generate Geyser config

7. FINALIZE
   ├─ Create manifest.json
   ├─ Generate metadata
   ├─ Cleanup temp files
   └─ Complete!
```

## 🎮 Menggunakan Converted Pack

### Di Minecraft Bedrock (Lokal)
1. Copy folder output ke Bedrock packs directory:
   - Windows: `%APPDATA%\.minecraft\resource_packs\`
   - macOS: `~/Library/Application Support/minecraft/resource_packs/`
   - Linux: `~/.minecraft/resource_packs/`
2. Buka Minecraft → Settings → Resource Packs
3. Activate pack Anda

### Dengan GeyserMC Server
1. Copy output folder ke `GeyserMC/packs/`
2. Restart server (atau reload packs)
3. Bedrock clients akan auto-download pack
4. Custom items & blocks akan terlihat untuk Bedrock players

### Dengan Geyser Proxy (Standalone)
```yaml
# geyser-config.yml
resource-packs:
  packs:
    - path/to/converted_pack

custom-items: true
custom-blocks: true
```

## 🔧 Advanced Configuration

### Custom Conversion Rules
Edit `converter/config.py`:

```python
CONVERSION_RULES = ConversionRules(
    compress_textures=True,         # Compress output textures
    normalize_sound_level=True,     # Normalize audio levels
    convert_item_models=True,       # Convert item models
    include_geyser_mapping=True,    # Include Geyser files
)
```

### Sound Event Mapping
Custom sound event mappings di `config.py`:

```python
SOUND_EVENT_MAPPING: Dict[str, str] = {
    "block.stone.break": "dig.stone",
    "entity.player.hurt": "mob.player.hurt",
    # Add more mappings...
}
```

### Texture Path Mapping
Customize texture path conversion:

```python
TEXTURE_PATH_MAPPING: Dict[str, str] = {
    "textures/block/": "textures/blocks/",
    "textures/item/": "textures/items/",
    # Add more mappings...
}
```

## 📊 Supported Assets

### Textures
- ✅ PNG (primary)
- ✅ JPG/JPEG
- ✅ Animated textures (MCMeta)
- ✅ Custom colors

### Sounds
- ✅ OGG (recommended)
- ✅ WAV (converts to OGG)
- ✅ MP3 (converts to OGG with ffmpeg)
- ✅ FSB (Bedrock native)

### Models
- ✅ Item models (JSON)
- ✅ Block models (JSON)
- ✅ Predicates (custom_model_data)
- ✅ Overrides

### Other
- ✅ TTF/OTF Fonts
- ✅ Language files (.lang)
- ✅ GUI/UI files
- ✅ Particle definitions

## 🐛 Troubleshooting

### Pack tidak ditemukan
```
Error: "Pack not found in input folder"
→ Pastikan pack folder di letakkan di `input/` folder
→ Check pack.mcmeta ada di root pack folder
```

### Conversion error
```
Error: "Invalid pack.mcmeta JSON"
→ Check pack.mcmeta file format (valid JSON)
→ Pastikan encoding UTF-8
```

### Sounds tidak convert
```
Warning: "ffmpeg not found"
→ Install ffmpeg untuk audio conversion
→ Atau gunakan OGG files (no conversion needed)
```

### Output pack tidak muncul di Bedrock
```
→ Check folder permissions
→ Verify manifest.json format valid
→ Test dengan vanilla Bedrock pack terlebih dahulu
```

## 🔍 Logging

Logs disimpan di `logs/` folder:
```
logs/
  my_pack_20240309_150530.log
  another_pack_20240309_160000.log
```

View recent log:
```bash
tail -f logs/*.log
```

## 📝 Limitations

- Custom shader packs tidak supported (Bedrock no shaders)
- OptiFine models hanya partial support
- 3D custom models terbatas oleh Bedrock capabilities
- Animated GIF textures → PNG statis

## 🤝 Contributing

Issues & pull requests welcome! Improvements:
- Additional format support
- Optimization passes
- Better error handling
- Documentation improvements

## 📄 License

MIT License - Feel free to use dan modify!

## 🙏 Credits

- Minecraft by Mojang Studios
- GeyserMC Project
- Resource Pack Converter Team

## 📧 Support

- Check logs untuk detailed error messages
- Verify input pack format valid
- Ensure all dependencies installed
- Check firewall/permissions untuk output folder

---

**Version**: 1.0.0  
**Last Updated**: 2024-03-09  
**Status**: Production Ready ✅
