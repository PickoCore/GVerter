"""
Master Resource Pack Converter - Orchestrates keseluruhan konversi
Mengkoordinasikan texture, sound, model, font, dan Geyser mappings
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from converter.config import (
    INPUT_DIR, OUTPUT_DIR, BEDROCK_PACK_FORMAT,
    MINECRAFT_NAMESPACE, SUCCESS_MESSAGES
)
from converter.core.base_converter import BaseConverter
from converter.core.texture_converter import TextureConverter
from converter.core.sound_converter import SoundConverter
from converter.core.model_converter import ModelConverter
from converter.core.font_converter import FontConverter
from converter.core.geyser_mapper import GeyserMapper


class ResourcePackConverter:
    """Master converter untuk full resource pack conversion"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        """
        Inisialisasi master converter
        
        Args:
            pack_name: Nama resource pack (folder name atau zip filename)
            verbose: Enable verbose logging
        """
        self.pack_name = self._clean_pack_name(pack_name)
        self.verbose = verbose
        self.logger = self._setup_logger()
        
        # Paths
        self.java_pack_path = INPUT_DIR / self.pack_name
        self.bedrock_pack_path = OUTPUT_DIR / f"{self.pack_name}_bedrock"
        
        # Converters
        self.converters = {
            'texture': None,
            'sound': None,
            'model': None,
            'font': None,
            'geyser': None,
        }
        
        # Statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'duration': 0,
            'status': 'pending',
            'total_textures': 0,
            'total_sounds': 0,
            'total_models': 0,
            'total_fonts': 0,
            'errors': [],
            'warnings': [],
        }
    
    def _clean_pack_name(self, name: str) -> str:
        """Bersihkan nama pack"""
        # Remove extensions
        name = name.replace('.zip', '').replace('.tar', '').replace('.gz', '')
        return name.strip()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger untuk master converter"""
        logger = logging.getLogger("MasterConverter")
        
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_level = logging.DEBUG if self.verbose else logging.INFO
            console_handler.setLevel(console_level)
            
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            logger.setLevel(logging.DEBUG)
        
        return logger
    
    def convert(self) -> bool:
        """Main conversion process"""
        self.stats['start_time'] = datetime.now()
        self.logger.info("=" * 70)
        self.logger.info(f"Starting conversion: {self.pack_name}")
        self.logger.info("=" * 70)
        
        try:
            # 1. Validate Java pack
            if not self._validate_pack():
                self.stats['status'] = 'failed'
                return False
            
            # 2. Convert textures
            if not self._convert_textures():
                self.logger.warning("Texture conversion failed or skipped")
            
            # 3. Convert sounds
            if not self._convert_sounds():
                self.logger.warning("Sound conversion failed or skipped")
            
            # 4. Convert models
            if not self._convert_models():
                self.logger.warning("Model conversion failed or skipped")
            
            # 5. Convert fonts & languages
            if not self._convert_fonts():
                self.logger.warning("Font conversion failed or skipped")
            
            # 6. Create Bedrock manifest
            if not self._create_manifest():
                self.logger.warning("Failed to create manifest")
            
            # 7. Create Geyser mappings
            if not self._create_geyser_mappings():
                self.logger.warning("Geyser mapping creation failed or skipped")
            
            # 8. Create conversion metadata
            self._create_metadata()
            
            # 9. Finalize & cleanup
            self._finalize()
            
            self.stats['status'] = 'success'
            return True
            
        except Exception as e:
            self.logger.error(f"Conversion failed with error: {e}", exc_info=self.verbose)
            self.stats['status'] = 'failed'
            self.stats['errors'].append(str(e))
            return False
        
        finally:
            self.stats['end_time'] = datetime.now()
            if self.stats['start_time']:
                duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
                self.stats['duration'] = duration
                self._log_summary()
    
    def _validate_pack(self) -> bool:
        """Validate Java resource pack"""
        self.logger.info("Validating Java resource pack...")
        
        if not self.java_pack_path.exists():
            self.logger.error(f"Pack not found: {self.java_pack_path}")
            self.stats['errors'].append(f"Pack directory not found: {self.java_pack_path}")
            return False
        
        # Check pack.mcmeta
        pack_mcmeta = self.java_pack_path / "pack.mcmeta"
        if not pack_mcmeta.exists():
            self.logger.error("pack.mcmeta not found")
            self.stats['errors'].append("pack.mcmeta not found")
            return False
        
        try:
            with open(pack_mcmeta, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            self.logger.info(f"✓ Pack validated (format: {metadata.get('pack', {}).get('pack_format', 'unknown')})")
            return True
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid pack.mcmeta: {e}")
            self.stats['errors'].append(f"Invalid pack.mcmeta: {e}")
            return False
    
    def _convert_textures(self) -> bool:
        """Convert textures"""
        self.logger.info("\n► Converting textures...")
        try:
            converter = TextureConverter(self.pack_name, self.verbose)
            self.converters['texture'] = converter
            
            # Setup output structure
            converter.setup_output_structure()
            
            # Convert
            if converter.convert():
                stats = converter.get_statistics()
                self.stats['total_textures'] = stats['textures_converted']
                self.logger.info(f"✓ Textures converted: {stats['textures_converted']} files")
                return True
            else:
                self.logger.warning("Texture conversion incomplete")
                return False
        except Exception as e:
            self.logger.error(f"Texture conversion error: {e}")
            self.stats['errors'].append(f"Texture conversion: {e}")
            return False
    
    def _convert_sounds(self) -> bool:
        """Convert sounds"""
        self.logger.info("\n► Converting sounds...")
        try:
            converter = SoundConverter(self.pack_name, self.verbose)
            self.converters['sound'] = converter
            
            # Setup output structure
            converter.setup_output_structure()
            
            # Convert
            if converter.convert():
                stats = converter.get_statistics()
                self.stats['total_sounds'] = stats['sounds_converted']
                self.logger.info(f"✓ Sounds converted: {stats['sounds_converted']} files")
                return True
            else:
                self.logger.warning("Sound conversion incomplete")
                return False
        except Exception as e:
            self.logger.error(f"Sound conversion error: {e}")
            self.stats['errors'].append(f"Sound conversion: {e}")
            return False
    
    def _convert_models(self) -> bool:
        """Convert models"""
        self.logger.info("\n► Converting models...")
        try:
            converter = ModelConverter(self.pack_name, self.verbose)
            self.converters['model'] = converter
            
            # Setup output structure
            converter.setup_output_structure()
            
            # Convert
            if converter.convert():
                stats = converter.get_statistics()
                self.stats['total_models'] = stats['models_converted']
                self.logger.info(f"✓ Models converted: {stats['models_converted']} files")
                return True
            else:
                self.logger.warning("Model conversion incomplete")
                return False
        except Exception as e:
            self.logger.error(f"Model conversion error: {e}")
            self.stats['errors'].append(f"Model conversion: {e}")
            return False
    
    def _convert_fonts(self) -> bool:
        """Convert fonts and languages"""
        self.logger.info("\n► Converting fonts & languages...")
        try:
            converter = FontConverter(self.pack_name, self.verbose)
            self.converters['font'] = converter
            
            # Setup output structure
            converter.setup_output_structure()
            
            # Convert
            if converter.convert():
                stats = converter.get_statistics()
                self.stats['total_fonts'] = stats['fonts_converted']
                self.logger.info(f"✓ Fonts converted: {stats['fonts_converted']} files")
                return True
            else:
                self.logger.warning("Font conversion incomplete")
                return False
        except Exception as e:
            self.logger.error(f"Font conversion error: {e}")
            self.stats['errors'].append(f"Font conversion: {e}")
            return False
    
    def _create_manifest(self) -> bool:
        """Create Bedrock manifest.json"""
        self.logger.info("\n► Creating Bedrock manifest...")
        try:
            # Create manifest
            converter = BaseConverter(self.pack_name, self.verbose)
            manifest = converter.create_bedrock_manifest()
            
            # Save manifest
            manifest_path = self.bedrock_pack_path / "manifest.json"
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info("✓ Manifest created")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create manifest: {e}")
            self.stats['errors'].append(f"Manifest creation: {e}")
            return False
    
    def _create_geyser_mappings(self) -> bool:
        """Create Geyser mappings"""
        self.logger.info("\n► Creating Geyser mappings...")
        try:
            mapper = GeyserMapper(self.pack_name, self.verbose)
            
            if mapper.convert():
                self.logger.info("✓ Geyser mappings created")
                return True
            else:
                self.logger.warning("Geyser mapping creation incomplete")
                return False
        except Exception as e:
            self.logger.error(f"Geyser mapping error: {e}")
            self.stats['errors'].append(f"Geyser mapping: {e}")
            return False
    
    def _create_metadata(self) -> None:
        """Create conversion metadata file"""
        self.logger.info("Creating conversion metadata...")
        try:
            metadata = {
                "conversion_info": {
                    "source_pack": self.pack_name,
                    "conversion_date": datetime.now().isoformat(),
                    "conversion_duration_seconds": self.stats['duration'],
                    "source_format": "Java Edition",
                    "target_format": "Bedrock Edition",
                    "bedrock_format_version": BEDROCK_PACK_FORMAT,
                    "status": self.stats['status']
                },
                "assets_converted": {
                    "textures": self.stats['total_textures'],
                    "sounds": self.stats['total_sounds'],
                    "models": self.stats['total_models'],
                    "fonts": self.stats['total_fonts']
                },
                "features": {
                    "geyser_compatible": True,
                    "custom_items_support": True,
                    "custom_blocks_support": True,
                    "sound_mappings": True,
                    "texture_support": True
                }
            }
            
            metadata_path = self.bedrock_pack_path / "_conversion_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info("✓ Metadata created")
        except Exception as e:
            self.logger.warning(f"Failed to create metadata: {e}")
    
    def _finalize(self) -> None:
        """Finalize conversion"""
        self.logger.info("\n► Finalizing conversion...")
        
        # Optional: create zip archive
        # converter = BaseConverter(self.pack_name)
        # converter.bedrock_pack_path = self.bedrock_pack_path
        # converter.compress_pack()
    
    def _log_summary(self) -> None:
        """Log conversion summary"""
        self.logger.info("\n" + "=" * 70)
        self.logger.info("CONVERSION SUMMARY")
        self.logger.info("=" * 70)
        self.logger.info(f"Pack Name: {self.pack_name}")
        self.logger.info(f"Status: {self.stats['status'].upper()}")
        self.logger.info(f"Duration: {self.stats['duration']:.2f} seconds")
        self.logger.info(f"\nAssets Converted:")
        self.logger.info(f"  - Textures: {self.stats['total_textures']}")
        self.logger.info(f"  - Sounds: {self.stats['total_sounds']}")
        self.logger.info(f"  - Models: {self.stats['total_models']}")
        self.logger.info(f"  - Fonts: {self.stats['total_fonts']}")
        
        if self.stats['errors']:
            self.logger.info(f"\nErrors: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                self.logger.error(f"  - {error}")
        
        self.logger.info(f"\nOutput: {self.bedrock_pack_path}")
        self.logger.info("=" * 70 + "\n")
    
    def get_statistics(self) -> Dict:
        """Get conversion statistics"""
        return self.stats.copy()
