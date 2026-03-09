"""
Sound Converter - Konversi sound dari Java ke Bedrock
Menangani OGG, WAV, MP3 dan mapping sound events
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from converter.config import (
    SOUND_EVENT_MAPPING, SUPPORTED_SOUNDS,
    DEFAULT_SOUND_FORMAT
)
from converter.core.base_converter import BaseConverter


class SoundConverter(BaseConverter):
    """Converter untuk sound resources"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        super().__init__(pack_name, verbose)
        self.sound_mappings = {}
        self.java_sounds_config = {}
        self.bedrock_sounds_config = {}
    
    def convert_sounds(self) -> bool:
        """Convert semua sound dari Java ke Bedrock"""
        self.logger.info("Starting sound conversion")
        
        assets_path = self.java_pack_path / "assets"
        if not assets_path.exists():
            self.logger.warning("No assets folder found")
            return True
        
        minecraft_path = assets_path / "minecraft"
        if not minecraft_path.exists():
            self.logger.warning("No minecraft namespace found")
            return True
        
        sounds_path = minecraft_path / "sounds"
        if not sounds_path.exists():
            self.logger.info("No sounds folder found")
            return True
        
        # Load sounds.json untuk mapping
        sounds_json = minecraft_path / "sounds.json"
        if sounds_json.exists():
            self._load_java_sounds_config(sounds_json)
        
        # Process semua sound files
        sound_files = list(sounds_path.rglob("*"))
        for sound_file in sound_files:
            if sound_file.is_file() and sound_file.suffix.lower() in SUPPORTED_SOUNDS:
                self._convert_single_sound(sound_file)
        
        self.logger.info(f"Sound conversion completed: {self.stats['sounds_converted']} files")
        return True
    
    def _load_java_sounds_config(self, sounds_json: Path) -> None:
        """Load sounds.json dari Java pack"""
        try:
            with open(sounds_json, 'r', encoding='utf-8') as f:
                self.java_sounds_config = json.load(f)
            self.logger.info("Loaded Java sounds.json")
        except Exception as e:
            self.logger.warning(f"Failed to load sounds.json: {e}")
    
    def _convert_single_sound(self, sound_file: Path) -> bool:
        """Convert single sound file"""
        try:
            relative_path = sound_file.relative_to(self.java_pack_path / "assets" / "minecraft" / "sounds")
            
            # Map path dari Java ke Bedrock
            bedrock_relative_path = str(relative_path)
            bedrock_dest = self.bedrock_pack_path / "sounds" / bedrock_relative_path
            
            # Create parent directories
            bedrock_dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert sound format jika perlu
            self._process_sound_file(sound_file, bedrock_dest)
            
            self.stats["sounds_converted"] += 1
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to convert sound {sound_file}: {e}")
            self.stats["warnings"] += 1
            return False
    
    def _process_sound_file(self, src: Path, dest: Path) -> None:
        """Process sound file dengan konversi format jika perlu"""
        
        # Bedrock prefers OGG format
        if src.suffix.lower() == '.ogg':
            # Already OGG, just copy
            import shutil
            shutil.copy2(src, dest)
            self.logger.debug(f"Copied sound: {src.name}")
            return
        
        # Coba convert ke OGG jika ffmpeg tersedia
        if src.suffix.lower() in {'.wav', '.mp3', '.flac'}:
            dest_ogg = dest.with_suffix('.ogg')
            if self._convert_to_ogg(src, dest_ogg):
                self.logger.debug(f"Converted to OGG: {src.name}")
                return
        
        # Fallback: copy original
        import shutil
        shutil.copy2(src, dest)
        self.logger.debug(f"Copied sound (original format): {src.name}")
    
    def _convert_to_ogg(self, src: Path, dest: Path) -> bool:
        """Convert audio file ke OGG menggunakan ffmpeg"""
        try:
            # Check if ffmpeg is available
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            
            # Convert to OGG Vorbis
            result = subprocess.run(
                ['ffmpeg', '-i', str(src), '-c:a', 'libvorbis', '-q:a', '4', '-y', str(dest)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.debug(f"Successfully converted {src.name} to OGG")
                return True
            else:
                self.logger.warning(f"ffmpeg conversion failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            self.logger.debug("ffmpeg not available, skipping audio conversion")
            return False
        except Exception as e:
            self.logger.warning(f"Error converting audio: {e}")
            return False
    
    def create_sound_definitions(self) -> Dict:
        """Create sound_definitions.json untuk Bedrock"""
        sound_definitions = {
            "sound_definitions": {}
        }
        
        # Scan sounds folder dan create definitions
        sounds_folder = self.bedrock_pack_path / "sounds"
        if sounds_folder.exists():
            for sound_file in sounds_folder.rglob("*.ogg"):
                relative = sound_file.relative_to(sounds_folder)
                sound_name = str(relative).replace('\\', '.').replace('/', '.').replace('.ogg', '')
                
                sound_definitions["sound_definitions"][sound_name] = {
                    "sounds": [
                        f"sounds/{relative}".replace('\\', '/').replace('.ogg', '')
                    ]
                }
        
        return sound_definitions
    
    def create_sound_event_mappings(self) -> Dict:
        """Create mapping antara Java sound events ke Bedrock"""
        mappings = {}
        
        for java_event, bedrock_event in SOUND_EVENT_MAPPING.items():
            mappings[java_event] = {
                "bedrock_event": bedrock_event,
                "replacement": bedrock_event
            }
        
        return mappings
    
    def map_java_sounds_to_bedrock(self) -> Dict:
        """Map Java sounds.json ke Bedrock sound_definitions.json"""
        bedrock_sounds = {}
        
        for event_name, event_data in self.java_sounds_config.items():
            # Get Bedrock mapping
            bedrock_event = SOUND_EVENT_MAPPING.get(event_name, event_name)
            
            # Extract sounds
            sounds = []
            if isinstance(event_data, dict):
                if 'sounds' in event_data:
                    for sound in event_data['sounds']:
                        if isinstance(sound, dict):
                            sounds.append(sound.get('name', sound))
                        else:
                            sounds.append(str(sound))
            
            if sounds:
                bedrock_sounds[bedrock_event] = {
                    "sounds": sounds
                }
        
        return bedrock_sounds
    
    def save_sound_definitions(self) -> bool:
        """Save sound_definitions.json"""
        try:
            self.logger.info("Creating sound definitions")
            
            sound_definitions = self.create_sound_definitions()
            
            # Save sound_definitions.json
            with open(self.bedrock_pack_path / "sound_definitions.json", 'w') as f:
                json.dump(sound_definitions, f, indent=2)
            
            # Save sound mappings untuk reference
            mappings = self.create_sound_event_mappings()
            with open(self.bedrock_pack_path / "_sound_event_mappings.json", 'w') as f:
                json.dump(mappings, f, indent=2)
            
            self.logger.info("Sound definitions created")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save sound definitions: {e}")
            self.stats["errors"] += 1
            return False
    
    def convert(self) -> bool:
        """Main convert method"""
        if not self.validate_java_pack():
            return False
        
        if not self.setup_output_structure():
            return False
        
        # Convert sounds
        if not self.convert_sounds():
            return False
        
        # Save sound definitions
        if not self.save_sound_definitions():
            return False
        
        self.logger.info("Sound conversion finished successfully")
        return True
