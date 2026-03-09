"""
Texture Converter - Konversi texture dari Java ke Bedrock
Menangani PNG, JPG, dan format lainnya
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
try:
    from PIL import Image
except ImportError:
    Image = None

from converter.config import (
    TEXTURE_PATH_MAPPING, SUPPORTED_TEXTURES,
    DEFAULT_TEXTURE_FORMAT, MAX_TEXTURE_RESOLUTION
)
from converter.core.base_converter import BaseConverter


class TextureConverter(BaseConverter):
    """Converter untuk texture resources"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        super().__init__(pack_name, verbose)
        self.texture_mappings = {}
        
        if Image is None:
            self.logger.warning("Pillow tidak tersedia, image processing akan dilewati")
    
    def convert_textures(self) -> bool:
        """Convert semua texture dari Java ke Bedrock"""
        self.logger.info("Starting texture conversion")
        
        assets_path = self.java_pack_path / "assets"
        if not assets_path.exists():
            self.logger.warning("No assets folder found")
            return True
        
        minecraft_path = assets_path / "minecraft"
        if not minecraft_path.exists():
            self.logger.warning("No minecraft namespace found")
            return True
        
        textures_path = minecraft_path / "textures"
        if not textures_path.exists():
            self.logger.warning("No textures folder found")
            return True
        
        # Process semua texture files
        texture_files = list(textures_path.rglob("*"))
        for texture_file in texture_files:
            if texture_file.is_file() and texture_file.suffix.lower() in SUPPORTED_TEXTURES:
                self._convert_single_texture(texture_file)
        
        self.logger.info(f"Texture conversion completed: {self.stats['textures_converted']} files")
        return True
    
    def _convert_single_texture(self, texture_file: Path) -> bool:
        """Convert single texture file"""
        try:
            relative_path = texture_file.relative_to(self.java_pack_path / "assets" / "minecraft" / "textures")
            
            # Map path dari Java ke Bedrock
            bedrock_relative_path = self._map_texture_path(str(relative_path))
            bedrock_dest = self.bedrock_pack_path / "textures" / bedrock_relative_path
            
            # Create parent directories
            bedrock_dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Process texture (convert if needed)
            self._process_texture_file(texture_file, bedrock_dest)
            
            self.stats["textures_converted"] += 1
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to convert texture {texture_file}: {e}")
            self.stats["warnings"] += 1
            return False
    
    def _map_texture_path(self, java_path: str) -> str:
        """Map Java texture path ke Bedrock format"""
        bedrock_path = java_path
        
        # Replace Java paths dengan Bedrock paths
        path_mappings = {
            "block/": "blocks/",
            "item/": "items/",
            "entity/": "entity/",
            "gui/": "ui/",
            "font/": "font/",
            "environment/": "environment/",
            "particle/": "particle/",
        }
        
        for java_prefix, bedrock_prefix in path_mappings.items():
            if java_prefix in bedrock_path:
                bedrock_path = bedrock_path.replace(java_prefix, bedrock_prefix)
        
        return bedrock_path
    
    def _process_texture_file(self, src: Path, dest: Path) -> None:
        """Process texture file dengan optimasi jika perlu"""
        if Image is None:
            # Jika Pillow tidak ada, just copy
            import shutil
            shutil.copy2(src, dest)
            self.logger.debug(f"Copied (no processing): {src.name}")
            return
        
        try:
            # Open texture
            img = Image.open(src)
            
            # Ensure RGB or RGBA format
            if img.mode not in ('RGB', 'RGBA', 'P'):
                img = img.convert('RGBA')
            
            # Check resolution
            width, height = img.size
            if width > MAX_TEXTURE_RESOLUTION or height > MAX_TEXTURE_RESOLUTION:
                self.logger.debug(f"Scaling down texture: {src.name} ({width}x{height})")
                max_dim = max(width, height)
                scale = MAX_TEXTURE_RESOLUTION / max_dim
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save sebagai PNG (format standar Bedrock)
            img.save(dest, 'PNG', optimize=True)
            self.logger.debug(f"Processed texture: {src.name} -> {dest.name}")
            
        except Exception as e:
            self.logger.warning(f"Error processing texture {src}: {e}")
            # Fallback: just copy
            import shutil
            shutil.copy2(src, dest)
    
    def create_item_texture_mappings(self) -> Dict:
        """Create item_texture.json untuk Bedrock"""
        item_textures = {
            "texture_data": {}
        }
        
        # Scan items folder
        items_path = self.bedrock_pack_path / "textures" / "items"
        if items_path.exists():
            for texture_file in items_path.glob("*.png"):
                texture_name = texture_file.stem
                item_textures["texture_data"][texture_name] = {
                    "textures": [f"textures/items/{texture_name}"]
                }
        
        return item_textures
    
    def create_terrain_texture_mappings(self) -> Dict:
        """Create terrain_texture.json untuk Bedrock"""
        terrain_textures = {
            "texture_data": {}
        }
        
        # Scan blocks folder
        blocks_path = self.bedrock_pack_path / "textures" / "blocks"
        if blocks_path.exists():
            for texture_file in blocks_path.glob("*.png"):
                texture_name = texture_file.stem
                terrain_textures["texture_data"][texture_name] = {
                    "textures": f"textures/blocks/{texture_name}"
                }
        
        return terrain_textures
    
    def create_flipbook_textures(self) -> Dict:
        """Create flipbook_textures.json untuk animated textures"""
        flipbook_textures = []
        
        # Find animated textures (metadata)
        # Ini adalah placeholder untuk deteksi animated texture
        # Bedrock menggunakan berbeda format
        
        return {"flipbook_textures": flipbook_textures}
    
    def save_texture_mappings(self) -> bool:
        """Save semua texture mapping files"""
        try:
            self.logger.info("Creating texture mapping files")
            
            # Item textures
            item_textures = self.create_item_texture_mappings()
            with open(self.bedrock_pack_path / "item_texture.json", 'w') as f:
                json.dump(item_textures, f, indent=2)
            
            # Terrain textures
            terrain_textures = self.create_terrain_texture_mappings()
            with open(self.bedrock_pack_path / "terrain_texture.json", 'w') as f:
                json.dump(terrain_textures, f, indent=2)
            
            # Flipbook textures
            flipbook = self.create_flipbook_textures()
            with open(self.bedrock_pack_path / "flipbook_textures.json", 'w') as f:
                json.dump(flipbook, f, indent=2)
            
            self.logger.info("Texture mapping files created")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save texture mappings: {e}")
            self.stats["errors"] += 1
            return False
    
    def convert(self) -> bool:
        """Main convert method"""
        if not self.validate_java_pack():
            return False
        
        if not self.setup_output_structure():
            return False
        
        # Convert textures
        if not self.convert_textures():
            return False
        
        # Save texture mappings
        if not self.save_texture_mappings():
            return False
        
        self.logger.info("Texture conversion finished successfully")
        return True
