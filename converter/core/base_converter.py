"""
Base Converter - Inti dari konversi resource pack
Menangani logic umum untuk semua jenis konversi
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
from datetime import datetime
import zipfile

from converter.config import (
    INPUT_DIR, OUTPUT_DIR, TEMP_DIR, LOGS_DIR,
    BEDROCK_PACK_FORMAT, MINECRAFT_NAMESPACE
)


class BaseConverter(ABC):
    """Base class untuk semua converter"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        """
        Inisialisasi base converter
        
        Args:
            pack_name: Nama resource pack
            verbose: Enable verbose logging
        """
        self.pack_name = pack_name
        self.verbose = verbose
        self.logger = self._setup_logger()
        
        # Paths
        self.java_pack_path = INPUT_DIR / pack_name
        self.bedrock_pack_path = OUTPUT_DIR / f"{pack_name}_bedrock"
        self.temp_path = TEMP_DIR / pack_name
        
        # Metadata
        self.java_metadata = {}
        self.bedrock_metadata = {}
        
        # Statistics
        self.stats = {
            "textures_converted": 0,
            "sounds_converted": 0,
            "models_converted": 0,
            "fonts_converted": 0,
            "errors": 0,
            "warnings": 0,
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger untuk converter"""
        logger = logging.getLogger(f"Converter.{self.pack_name}")
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_level = logging.DEBUG if self.verbose else logging.INFO
            console_handler.setLevel(console_level)
            
            # File handler
            log_file = LOGS_DIR / f"{self.pack_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Formatter
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            logger.setLevel(logging.DEBUG)
        
        return logger
    
    def validate_java_pack(self) -> bool:
        """Validasi Java resource pack"""
        self.logger.info(f"Validating Java pack: {self.pack_name}")
        
        if not self.java_pack_path.exists():
            self.logger.error(f"Java pack path tidak ditemukan: {self.java_pack_path}")
            self.stats["errors"] += 1
            return False
        
        # Check for pack.mcmeta
        pack_mcmeta = self.java_pack_path / "pack.mcmeta"
        if not pack_mcmeta.exists():
            self.logger.error("pack.mcmeta tidak ditemukan")
            self.stats["errors"] += 1
            return False
        
        # Parse pack.mcmeta
        try:
            with open(pack_mcmeta, 'r', encoding='utf-8') as f:
                self.java_metadata = json.load(f)
            self.logger.info(f"Pack format version: {self.java_metadata.get('pack', {}).get('pack_format')}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid pack.mcmeta JSON: {e}")
            self.stats["errors"] += 1
            return False
        
        # Check for assets folder
        assets_path = self.java_pack_path / "assets"
        if not assets_path.exists():
            self.logger.warning("Assets folder tidak ditemukan")
            self.stats["warnings"] += 1
        
        self.logger.info("Java pack validation passed")
        return True
    
    def extract_zip_pack(self, zip_path: Path) -> bool:
        """Extract zip resource pack"""
        try:
            self.logger.info(f"Extracting zip: {zip_path}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_path)
            self.logger.info("Zip extracted successfully")
            return True
        except zipfile.BadZipFile as e:
            self.logger.error(f"Invalid zip file: {e}")
            self.stats["errors"] += 1
            return False
    
    def create_bedrock_manifest(self) -> Dict:
        """Buat manifest.json untuk Bedrock"""
        java_name = self.java_metadata.get('pack', {}).get('description', 'Custom Pack')
        
        manifest = {
            "format_version": 2,
            "header": {
                "description": f"Converted from Java: {java_name}",
                "name": f"{self.pack_name} (Bedrock)",
                "uuid": self._generate_uuid(),
                "version": [1, 0, 0]
            },
            "modules": [
                {
                    "description": "Bedrock Resource Pack",
                    "type": "resources",
                    "uuid": self._generate_uuid(),
                    "version": [1, 0, 0]
                }
            ],
            "pack_scope": "global"
        }
        
        return manifest
    
    def _generate_uuid(self) -> str:
        """Generate UUID untuk manifest"""
        import uuid
        return str(uuid.uuid4())
    
    def setup_output_structure(self) -> bool:
        """Setup struktur folder output Bedrock"""
        try:
            self.logger.info("Setting up Bedrock pack structure")
            
            # Create main directories
            folders = [
                "",  # root
                "texts",
                "textures/blocks",
                "textures/items",
                "textures/entity",
                "textures/ui",
                "textures/font",
                "textures/environment",
                "sounds",
                "models/blocks",
                "models/entity",
                "materials",
                "render_controllers",
                "animation_controllers",
                "animations",
            ]
            
            for folder in folders:
                folder_path = self.bedrock_pack_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.info("Output structure created")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup output structure: {e}")
            self.stats["errors"] += 1
            return False
    
    def copy_file_preserve_structure(self, src: Path, dest_base: Path, 
                                     new_subpath: Optional[str] = None) -> bool:
        """Copy file dengan preserve structure atau ke path baru"""
        try:
            if new_subpath:
                dest = dest_base / new_subpath
            else:
                dest = dest_base / src.relative_to(self.java_pack_path)
            
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to copy {src}: {e}")
            self.stats["warnings"] += 1
            return False
    
    def cleanup_temp(self) -> None:
        """Hapus temporary files"""
        try:
            if self.temp_path.exists():
                shutil.rmtree(self.temp_path)
                self.logger.info("Temporary files cleaned up")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup temp: {e}")
    
    def compress_pack(self, output_format: str = "zip") -> Optional[Path]:
        """Compress output pack ke format file"""
        try:
            self.logger.info(f"Compressing pack to {output_format}")
            
            if output_format == "zip":
                output_file = OUTPUT_DIR / f"{self.pack_name}_bedrock.zip"
                shutil.make_archive(
                    str(output_file.with_suffix('')),
                    'zip',
                    self.bedrock_pack_path
                )
                self.logger.info(f"Pack compressed: {output_file}")
                return output_file
            
        except Exception as e:
            self.logger.error(f"Failed to compress pack: {e}")
            self.stats["errors"] += 1
            return None
    
    @abstractmethod
    def convert(self) -> bool:
        """Main conversion method - harus diimplementasikan subclass"""
        pass
    
    def get_statistics(self) -> Dict:
        """Dapatkan statistik konversi"""
        return self.stats.copy()
    
    def log_summary(self) -> None:
        """Log summary dari konversi"""
        self.logger.info("=" * 60)
        self.logger.info("CONVERSION SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"Textures converted: {self.stats['textures_converted']}")
        self.logger.info(f"Sounds converted: {self.stats['sounds_converted']}")
        self.logger.info(f"Models converted: {self.stats['models_converted']}")
        self.logger.info(f"Fonts converted: {self.stats['fonts_converted']}")
        self.logger.info(f"Warnings: {self.stats['warnings']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        self.logger.info("=" * 60)
