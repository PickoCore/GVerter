"""
Minecraft Resource Pack Converter Configuration
Konfigurasi global dan mapping untuk konversi Java ke Bedrock
"""

from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

# ============================================================================
# PATHS CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
for directory in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# ============================================================================
# MINECRAFT VERSIONS & PACK FORMAT
# ============================================================================

PACK_FORMAT_VERSION = {
    "1.20": 32,
    "1.19": 13,
    "1.18": 12,
    "1.17": 10,
    "1.16": 8,
    "1.15": 5,
    "1.14": 4,
    "1.13": 4,
}

BEDROCK_PACK_FORMAT = 15  # Latest Bedrock format


# ============================================================================
# SOUND MAPPING: Java to Bedrock
# ============================================================================

SOUND_EVENT_MAPPING: Dict[str, str] = {
    # Block sounds
    "block.stone.break": "dig.stone",
    "block.stone.place": "dig.stone",
    "block.dirt.break": "dig.gravel",
    "block.dirt.place": "dig.gravel",
    "block.wood.break": "dig.wood",
    "block.wood.place": "dig.wood",
    "block.grass.break": "dig.grass",
    "block.grass.place": "dig.grass",
    "block.sand.break": "dig.sand",
    "block.sand.place": "dig.sand",
    
    # Entity sounds
    "entity.player.attack.strong": "mob.player.attack.strong",
    "entity.player.hurt": "mob.player.hurt",
    "entity.player.death": "mob.player.death",
    "entity.zombie.hurt": "mob.zombie.say",
    "entity.zombie.death": "mob.zombie.death",
    "entity.creeper.hurt": "mob.creeper.say",
    "entity.creeper.death": "mob.creeper.death",
    
    # UI sounds
    "ui.button.click": "gui.button.press",
    "ui.loom.select_pattern": "gui.loom.select_pattern",
    
    # Ambient sounds
    "ambient.cave": "ambient.cave",
    "ambient.weather.rain": "weather.rain",
    "ambient.weather.thunder": "weather.thunder",
}


# ============================================================================
# TEXTURE MAPPING: Java to Bedrock
# ============================================================================

TEXTURE_PATH_MAPPING: Dict[str, str] = {
    # Blocks
    "textures/block/": "textures/blocks/",
    
    # Items
    "textures/item/": "textures/items/",
    
    # Entity
    "textures/entity/": "textures/entity/",
    
    # GUI/UI
    "textures/gui/": "textures/ui/",
    "textures/font/": "textures/font/",
}


# ============================================================================
# FONT MAPPING
# ============================================================================

FONT_METADATA_TEMPLATE = {
    "type": "java",
    "version": 1
}

# Bedrock font metadata
BEDROCK_FONT_METADATA = {
    "emotes": {}
}


# ============================================================================
# MODEL MAPPING: Java to Bedrock
# ============================================================================

# Item model properties yang bisa di-map ke Bedrock
ITEM_MODEL_PROPERTIES = [
    "damaged",
    "damage",
    "broken",
    "custom_model_data",
]

ITEM_PREDICATE_MAPPING = {
    "broken": "is_broken",
    "damaged": "is_damaged",
    "custom_model_data": "custom_model_data",
    "blocking": "is_blocking",
    "blocked": "is_blocked",
    "pull": "pull",
    "pulling": "pulling",
    "casting": "casting",
    "charged": "charged",
}


# ============================================================================
# GEYSER CUSTOM ITEM MAPPING
# ============================================================================

GEYSER_CUSTOM_ITEM_TEMPLATE = {
    "minecraft:diamond_hoe": {
        "name": "Custom Item",
        "display_name": "Custom Item",
        "icon": "diamond_hoe",
        "stack_size": 64
    }
}

GEYSER_CUSTOM_BLOCK_TEMPLATE = {
    "minecraft:stone": {
        "name": "Custom Block",
        "display_name": "Custom Block",
        "icon": "stone"
    }
}


# ============================================================================
# SUPPORTED FILE TYPES & EXTENSIONS
# ============================================================================

SUPPORTED_TEXTURES = {".png", ".jpg", ".jpeg", ".bmp", ".tga"}
SUPPORTED_SOUNDS = {".ogg", ".wav", ".mp3", ".fsb"}
SUPPORTED_MODELS = {".json"}
SUPPORTED_FONTS = {".ttf", ".otf"}
SUPPORTED_LANG = {".lang", ".json"}


# ============================================================================
# CONVERSION RULES
# ============================================================================

@dataclass
class ConversionRules:
    """Aturan konversi resource pack"""
    
    # Texture conversion
    convert_texture_format: bool = True
    compress_textures: bool = False
    upscale_resolution: bool = False
    
    # Sound conversion
    convert_sound_format: bool = True  # OGG to OGG, WAV to OGG, etc
    normalize_sound_level: bool = True
    
    # Model conversion
    convert_item_models: bool = True
    convert_block_models: bool = True
    map_custom_models: bool = True
    
    # UI/Font conversion
    convert_fonts: bool = True
    convert_lang: bool = True
    convert_guis: bool = True
    
    # Geyser mapping
    include_geyser_mapping: bool = True
    create_item_mapping: bool = True
    create_block_mapping: bool = True
    
    # Output
    create_bedrock_manifest: bool = True
    pack_format_version: int = BEDROCK_PACK_FORMAT


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================================
# GEYSER EXTENSIONS MAPPING
# ============================================================================

GEYSER_EXTENSION_MAPPING = {
    "custom_items": "geyser_custom_items.json",
    "custom_blocks": "geyser_custom_blocks.json",
    "item_mappings": "geyser_item_mappings.json",
    "block_mappings": "geyser_block_mappings.json",
}


# ============================================================================
# MINECRAFT NAMESPACES
# ============================================================================

MINECRAFT_NAMESPACE = "minecraft"
CUSTOM_NAMESPACE_PREFIX = "custom"


# ============================================================================
# CONSTANTS
# ============================================================================

MAX_TEXTURE_RESOLUTION = 512  # Bedrock typical max
DEFAULT_TEXTURE_FORMAT = "png"
DEFAULT_SOUND_FORMAT = "ogg"

# Error messages
ERROR_MESSAGES = {
    "pack_not_found": "Resource pack tidak ditemukan di input folder",
    "invalid_manifest": "manifest.json tidak valid",
    "invalid_pack_mcmeta": "pack.mcmeta tidak valid",
    "texture_conversion_failed": "Gagal mengonversi texture",
    "sound_conversion_failed": "Gagal mengonversi sound",
    "model_conversion_failed": "Gagal mengonversi model",
}

# Success messages
SUCCESS_MESSAGES = {
    "conversion_complete": "Konversi resource pack berhasil!",
    "manifest_created": "Manifest Bedrock berhasil dibuat",
    "geyser_mapping_created": "Geyser mapping berhasil dibuat",
}
