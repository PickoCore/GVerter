"""
Geyser Mapper - Create Geyser mappings untuk compatibility Java/Bedrock
Membuat custom item dan block mappings untuk GeyserMC
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from converter.core.base_converter import BaseConverter
from converter.config import GEYSER_CUSTOM_ITEM_TEMPLATE, GEYSER_CUSTOM_BLOCK_TEMPLATE


class GeyserMapper(BaseConverter):
    """Mapper untuk Geyser extensions"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        super().__init__(pack_name, verbose)
        self.custom_items = {}
        self.custom_blocks = {}
    
    def create_geyser_extensions(self) -> bool:
        """Create Geyser extension mappings"""
        self.logger.info("Creating Geyser mappings")
        
        # Create custom items mapping
        custom_items = self._create_custom_items()
        if custom_items:
            self._save_json(
                self.bedrock_pack_path / "geyser_custom_items.json",
                custom_items
            )
            self.logger.info(f"Created custom items mapping ({len(custom_items)} items)")
        
        # Create custom blocks mapping
        custom_blocks = self._create_custom_blocks()
        if custom_blocks:
            self._save_json(
                self.bedrock_pack_path / "geyser_custom_blocks.json",
                custom_blocks
            )
            self.logger.info(f"Created custom blocks mapping ({len(custom_blocks)} blocks)")
        
        # Create item mappings (Java <-> Bedrock)
        item_mappings = self._create_item_mappings()
        if item_mappings:
            self._save_json(
                self.bedrock_pack_path / "geyser_item_mappings.json",
                item_mappings
            )
            self.logger.info(f"Created item mappings")
        
        # Create block mappings
        block_mappings = self._create_block_mappings()
        if block_mappings:
            self._save_json(
                self.bedrock_pack_path / "geyser_block_mappings.json",
                block_mappings
            )
            self.logger.info(f"Created block mappings")
        
        # Create Geyser config
        geyser_config = self._create_geyser_config()
        self._save_json(
            self.bedrock_pack_path / "geyser_config.json",
            geyser_config
        )
        
        self.logger.info("Geyser mappings creation completed")
        return True
    
    def _create_custom_items(self) -> Dict:
        """Create custom items mapping dari Java pack"""
        custom_items = {}
        
        # Scan item models untuk custom items
        models_path = self.bedrock_pack_path / "models" / "item"
        if models_path.exists():
            for model_file in models_path.glob("*.json"):
                item_name = model_file.stem
                try:
                    with open(model_file, 'r') as f:
                        model_data = json.load(f)
                    
                    # Create custom item entry
                    custom_item = {
                        "name": item_name,
                        "display_name": item_name.replace("_", " ").title(),
                        "icon": item_name,
                        "stack_size": 64,
                        "model": {
                            "type": "geometry",
                            "geometry": f"Geometry.{item_name}"
                        }
                    }
                    
                    # Add textures jika ada
                    if "textures" in model_data:
                        custom_item["textures"] = self._map_textures(model_data["textures"])
                    
                    custom_items[f"geyser:{item_name}"] = custom_item
                    
                except Exception as e:
                    self.logger.debug(f"Error processing item model {model_file}: {e}")
        
        return custom_items
    
    def _create_custom_blocks(self) -> Dict:
        """Create custom blocks mapping dari Java pack"""
        custom_blocks = {}
        
        # Scan block models untuk custom blocks
        models_path = self.bedrock_pack_path / "models" / "block"
        if models_path.exists():
            for model_file in models_path.glob("*.json"):
                block_name = model_file.stem
                try:
                    with open(model_file, 'r') as f:
                        model_data = json.load(f)
                    
                    # Create custom block entry
                    custom_block = {
                        "name": block_name,
                        "display_name": block_name.replace("_", " ").title(),
                        "icon": block_name,
                        "category": "misc",
                        "model": {
                            "type": "geometry",
                            "geometry": f"Geometry.{block_name}"
                        },
                        "lightLevel": 0,
                        "lightDamping": 1
                    }
                    
                    custom_blocks[f"geyser:{block_name}"] = custom_block
                    
                except Exception as e:
                    self.logger.debug(f"Error processing block model {model_file}: {e}")
        
        return custom_blocks
    
    def _create_item_mappings(self) -> Dict:
        """Create Java <-> Bedrock item mappings untuk Geyser"""
        item_mappings = {
            "format_version": "1.0.0",
            "mappings": {}
        }
        
        # Standard item mappings (Java to Bedrock identifier)
        standard_mappings = {
            "diamond_sword": "minecraft:diamond_sword",
            "diamond_pickaxe": "minecraft:diamond_pickaxe",
            "diamond_axe": "minecraft:diamond_axe",
            "diamond_shovel": "minecraft:diamond_shovel",
            "diamond_hoe": "minecraft:diamond_hoe",
            "iron_sword": "minecraft:iron_sword",
            "golden_sword": "minecraft:golden_sword",
            "netherite_sword": "minecraft:netherite_sword",
        }
        
        for java_id, bedrock_id in standard_mappings.items():
            item_mappings["mappings"][java_id] = {
                "bedrock_id": bedrock_id,
                "bedrock_data": 0
            }
        
        return item_mappings
    
    def _create_block_mappings(self) -> Dict:
        """Create Java <-> Bedrock block mappings"""
        block_mappings = {
            "format_version": "1.0.0",
            "mappings": {}
        }
        
        # Standard block mappings
        standard_block_mappings = {
            "stone": "minecraft:stone",
            "dirt": "minecraft:dirt",
            "grass_block": "minecraft:grass_block",
            "oak_log": "minecraft:oak_log",
            "oak_leaves": "minecraft:oak_leaves",
            "glass": "minecraft:glass",
            "sand": "minecraft:sand",
            "gravel": "minecraft:gravel",
            "iron_ore": "minecraft:iron_ore",
            "coal_ore": "minecraft:coal_ore",
            "oak_wood": "minecraft:oak_wood",
        }
        
        for java_id, bedrock_id in standard_block_mappings.items():
            block_mappings["mappings"][java_id] = {
                "bedrock_id": bedrock_id,
                "bedrock_data": 0
            }
        
        return block_mappings
    
    def _create_geyser_config(self) -> Dict:
        """Create Geyser configuration"""
        return {
            "pack_info": {
                "name": f"{self.pack_name} (Bedrock)",
                "description": "Converted from Java using Resource Pack Converter",
                "version": "1.0.0",
                "uuid": str(uuid.uuid4())
            },
            "features": {
                "custom_items": True,
                "custom_blocks": True,
                "item_mappings": True,
                "block_mappings": True
            },
            "compatibility": {
                "geyser_versions": ["1.7.0+"],
                "bedrock_versions": ["1.16.0+"]
            },
            "settings": {
                "enable_custom_items": True,
                "enable_custom_blocks": True,
                "auto_update_mappings": False
            }
        }
    
    def _map_textures(self, textures: Dict) -> Dict:
        """Map texture references"""
        mapped_textures = {}
        
        for texture_key, texture_value in textures.items():
            if isinstance(texture_value, str):
                # Remove namespace if present
                if ":" in texture_value:
                    texture_value = texture_value.split(":", 1)[1]
                mapped_textures[texture_key] = texture_value
        
        return mapped_textures
    
    def _save_json(self, path: Path, data: Dict) -> bool:
        """Save JSON file"""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save {path}: {e}")
            return False
    
    def create_geyser_readme(self) -> None:
        """Create README untuk Geyser mappings"""
        readme_content = f"""# {self.pack_name} - Geyser Mappings

## Informasi Pack
- **Nama Original**: {self.pack_name}
- **Format**: Bedrock Edition Resource Pack
- **GeyserMC Compatible**: Yes

## File yang Tersedia

### Mapping Files
- `geyser_custom_items.json` - Custom item definitions untuk Geyser
- `geyser_custom_blocks.json` - Custom block definitions untuk Geyser
- `geyser_item_mappings.json` - Java to Bedrock item ID mappings
- `geyser_block_mappings.json` - Java to Bedrock block ID mappings
- `geyser_config.json` - Geyser configuration untuk pack ini

### Asset Files
- `textures/` - Texture files (PNG format)
- `sounds/` - Audio files (OGG format)
- `models/` - Model definitions (JSON format)

## Cara Menggunakan dengan GeyserMC

1. Copy folder ini ke GeyserMC packs directory
2. Configure GeyserMC untuk load pack ini
3. Restart GeyserMC
4. Bedrock players akan melihat custom items dan blocks

## Konversi Info
- **Sumber**: Java Edition Resource Pack
- **Tujuan**: Bedrock Edition dengan GeyserMC
- **Conversion Time**: {self.bedrock_metadata.get('conversion_time', 'Unknown')}
- **Bedrock Format**: {self.bedrock_metadata.get('format_version', 15)}

## Support
Untuk masalah atau pertanyaan, lihat dokumentasi GeyserMC di:
https://geysermc.org/wiki/

## License
Format pack ini mengikuti license dari pack Java original.
"""
        
        try:
            with open(self.bedrock_pack_path / "GEYSER_MAPPING_README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
            self.logger.info("Geyser README created")
        except Exception as e:
            self.logger.warning(f"Failed to create README: {e}")
    
    def convert(self) -> bool:
        """Main convert method"""
        if not self.bedrock_pack_path.exists():
            self.logger.error("Bedrock pack path tidak ditemukan")
            return False
        
        # Create Geyser mappings
        if not self.create_geyser_extensions():
            return False
        
        # Create README
        self.create_geyser_readme()
        
        self.logger.info("Geyser mapping completed successfully")
        return True
