"""
Font & Language Converter - Konversi font dan language files
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from converter.config import SUPPORTED_FONTS, SUPPORTED_LANG
from converter.core.base_converter import BaseConverter


class FontConverter(BaseConverter):
    """Converter untuk font dan language resources"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        super().__init__(pack_name, verbose)
        self.fonts = {}
        self.languages = {}
    
    def convert_fonts(self) -> bool:
        """Convert font files dari Java ke Bedrock"""
        self.logger.info("Starting font conversion")
        
        # Check untuk font dalam assets
        assets_path = self.java_pack_path / "assets" / "minecraft"
        if not assets_path.exists():
            self.logger.info("No assets found")
            return True
        
        # Java fonts typically in assets/minecraft/font/
        java_fonts_path = assets_path / "font"
        
        # Check untuk custom font files
        textures_path = assets_path / "textures" / "font"
        if textures_path.exists():
            self._copy_font_textures(textures_path)
        
        self.logger.info(f"Font conversion completed: {self.stats['fonts_converted']} files")
        return True
    
    def _copy_font_textures(self, source_path: Path) -> None:
        """Copy font texture files"""
        try:
            dest_path = self.bedrock_pack_path / "textures" / "font"
            dest_path.mkdir(parents=True, exist_ok=True)
            
            for font_file in source_path.glob("*"):
                if font_file.is_file() and font_file.suffix.lower() in {".png", ".ttf", ".otf"}:
                    dest_file = dest_path / font_file.name
                    shutil.copy2(font_file, dest_file)
                    self.stats["fonts_converted"] += 1
                    self.logger.debug(f"Copied font file: {font_file.name}")
            
        except Exception as e:
            self.logger.warning(f"Error copying font textures: {e}")
            self.stats["warnings"] += 1
    
    def create_font_metadata(self) -> Dict:
        """Create font metadata untuk Bedrock"""
        font_metadata = {
            "type": "java",
            "version": 1,
            "fonts": [],
            "emotes": {}
        }
        
        # Scan font textures
        font_path = self.bedrock_pack_path / "textures" / "font"
        if font_path.exists():
            for font_file in font_path.glob("*.png"):
                font_metadata["fonts"].append({
                    "name": font_file.stem,
                    "file": f"textures/font/{font_file.name}"
                })
        
        return font_metadata
    
    def convert_languages(self) -> bool:
        """Convert language files dari Java ke Bedrock"""
        self.logger.info("Starting language conversion")
        
        assets_path = self.java_pack_path / "assets" / "minecraft"
        if not assets_path.exists():
            self.logger.info("No assets found")
            return True
        
        # Java lang files typically in assets/minecraft/lang/
        lang_path = assets_path / "lang"
        
        if lang_path.exists():
            self._process_lang_files(lang_path)
        
        self.logger.info(f"Language conversion completed")
        return True
    
    def _process_lang_files(self, lang_path: Path) -> None:
        """Process language files"""
        try:
            dest_lang_path = self.bedrock_pack_path / "texts"
            dest_lang_path.mkdir(parents=True, exist_ok=True)
            
            lang_files = {}
            
            for lang_file in lang_path.glob("*.lang"):
                language_code = lang_file.stem  # e.g., "en_us"
                
                # Read Java format lang file
                java_strings = self._read_java_lang_file(lang_file)
                
                # Create Bedrock format
                bedrock_lang = {
                    "language.code": language_code,
                    "language.name": self._get_language_name(language_code),
                    **java_strings
                }
                
                lang_files[language_code] = bedrock_lang
            
            # Create language names file
            language_names = {}
            for code, content in lang_files.items():
                if "language.name" in content:
                    language_names[code] = content["language.name"]
            
            if language_names:
                with open(dest_lang_path / "language_names.json", 'w', encoding='utf-8') as f:
                    json.dump(language_names, f, indent=2, ensure_ascii=False)
            
            # Save language files dalam Bedrock format
            for code, content in lang_files.items():
                self._save_bedrock_lang_file(dest_lang_path, code, content)
            
        except Exception as e:
            self.logger.warning(f"Error processing lang files: {e}")
            self.stats["warnings"] += 1
    
    def _read_java_lang_file(self, lang_file: Path) -> Dict[str, str]:
        """Read Java format lang file"""
        strings = {}
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            strings[key.strip()] = value.strip()
            
            self.logger.debug(f"Loaded {len(strings)} strings from {lang_file.name}")
        except Exception as e:
            self.logger.warning(f"Error reading lang file {lang_file}: {e}")
        
        return strings
    
    def _get_language_name(self, language_code: str) -> str:
        """Get friendly language name from code"""
        language_names = {
            "en_us": "English (US)",
            "en_gb": "English (GB)",
            "de_de": "Deutsch",
            "fr_fr": "Français",
            "es_es": "Español",
            "it_it": "Italiano",
            "ja_jp": "日本語",
            "zh_cn": "中文 (简体)",
            "zh_tw": "中文 (繁體)",
            "ko_kr": "한국어",
            "ru_ru": "Русский",
            "pt_br": "Português (Brasil)",
        }
        
        return language_names.get(language_code, language_code.replace("_", " ").title())
    
    def _save_bedrock_lang_file(self, dest_path: Path, language_code: str, content: Dict) -> None:
        """Save lang file dalam Bedrock format (JSON)"""
        try:
            # Create language subfolder
            lang_folder = dest_path / language_code
            lang_folder.mkdir(parents=True, exist_ok=True)
            
            # Save as JSON
            lang_json_path = lang_folder / f"{language_code}.json"
            with open(lang_json_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Saved language file: {language_code}")
            
        except Exception as e:
            self.logger.warning(f"Error saving lang file: {e}")
    
    def create_language_metadata(self) -> Dict:
        """Create language metadata"""
        return {
            "languages": [],
            "default_language": "en_us"
        }
    
    def save_language_files(self) -> bool:
        """Save language related files"""
        try:
            self.logger.info("Saving language metadata")
            
            texts_path = self.bedrock_pack_path / "texts"
            texts_path.mkdir(parents=True, exist_ok=True)
            
            # Create languages.json
            languages_file = {
                "en_us": "English (US)",
                "de_de": "Deutsch",
                "fr_fr": "Français",
                "es_es": "Español",
                "ja_jp": "日本語",
                "zh_cn": "中文 (简体)",
            }
            
            with open(texts_path / "languages.json", 'w', encoding='utf-8') as f:
                json.dump(languages_file, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save language files: {e}")
            self.stats["errors"] += 1
            return False
    
    def convert(self) -> bool:
        """Main convert method"""
        if not self.validate_java_pack():
            return False
        
        if not self.setup_output_structure():
            return False
        
        # Convert fonts
        if not self.convert_fonts():
            return False
        
        # Convert languages
        if not self.convert_languages():
            return False
        
        # Save metadata
        if not self.save_language_files():
            return False
        
        self.logger.info("Font and language conversion finished successfully")
        return True
