"""
Model Converter - Konversi model dan NBT dari Java ke Bedrock
Menangani item models, block models, dan custom model data
"""

import json
import copy
from pathlib import Path
from typing import Dict, List, Optional, Any

from converter.config import (
    ITEM_MODEL_PROPERTIES, ITEM_PREDICATE_MAPPING,
    MINECRAFT_NAMESPACE
)
from converter.core.base_converter import BaseConverter


class ModelConverter(BaseConverter):
    """Converter untuk model resources"""
    
    def __init__(self, pack_name: str, verbose: bool = False):
        super().__init__(pack_name, verbose)
        self.item_models = {}
        self.block_models = {}
    
    def convert_models(self) -> bool:
        """Convert semua model dari Java ke Bedrock"""
        self.logger.info("Starting model conversion")
        
        assets_path = self.java_pack_path / "assets"
        if not assets_path.exists():
            self.logger.warning("No assets folder found")
            return True
        
        minecraft_path = assets_path / "minecraft"
        if not minecraft_path.exists():
            self.logger.warning("No minecraft namespace found")
            return True
        
        models_path = minecraft_path / "models"
        if not models_path.exists():
            self.logger.info("No models folder found")
            return True
        
        # Process item models
        item_models_path = models_path / "item"
        if item_models_path.exists():
            self._convert_item_models(item_models_path)
        
        # Process block models
        block_models_path = models_path / "block"
        if block_models_path.exists():
            self._convert_block_models(block_models_path)
        
        self.logger.info(f"Model conversion completed: {self.stats['models_converted']} files")
        return True
    
    def _convert_item_models(self, item_models_path: Path) -> None:
        """Convert item models dari Java"""
        for model_file in item_models_path.rglob("*.json"):
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    java_model = json.load(f)
                
                # Convert model
                bedrock_model = self._convert_java_model_to_bedrock(java_model, "item")
                
                # Save to output
                relative_path = model_file.relative_to(item_models_path)
                bedrock_path = self.bedrock_pack_path / "models" / "item" / relative_path
                bedrock_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(bedrock_path, 'w', encoding='utf-8') as f:
                    json.dump(bedrock_model, f, indent=2)
                
                self.stats["models_converted"] += 1
                self.logger.debug(f"Converted item model: {model_file.name}")
                
            except Exception as e:
                self.logger.warning(f"Failed to convert model {model_file}: {e}")
                self.stats["warnings"] += 1
    
    def _convert_block_models(self, block_models_path: Path) -> None:
        """Convert block models dari Java"""
        for model_file in block_models_path.rglob("*.json"):
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    java_model = json.load(f)
                
                # Convert model
                bedrock_model = self._convert_java_model_to_bedrock(java_model, "block")
                
                # Save to output
                relative_path = model_file.relative_to(block_models_path)
                bedrock_path = self.bedrock_pack_path / "models" / "block" / relative_path
                bedrock_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(bedrock_path, 'w', encoding='utf-8') as f:
                    json.dump(bedrock_model, f, indent=2)
                
                self.stats["models_converted"] += 1
                self.logger.debug(f"Converted block model: {model_file.name}")
                
            except Exception as e:
                self.logger.warning(f"Failed to convert model {model_file}: {e}")
                self.stats["warnings"] += 1
    
    def _convert_java_model_to_bedrock(self, java_model: Dict, model_type: str) -> Dict:
        """Convert individual Java model ke Bedrock format"""
        bedrock_model = copy.deepcopy(java_model)
        
        # Konversi texture paths
        if "textures" in bedrock_model:
            for key, value in bedrock_model["textures"].items():
                # Konversi path
                if isinstance(value, str):
                    # Remove namespace if present
                    if ":" in value:
                        value = value.split(":", 1)[1]
                    # Map path
                    bedrock_model["textures"][key] = self._map_model_texture_path(value)
        
        # Konversi elements (cubes/faces)
        if "elements" in bedrock_model:
            for element in bedrock_model["elements"]:
                if "faces" in element:
                    for face, face_data in element["faces"].items():
                        if "texture" in face_data:
                            # Ensure texture reference format
                            texture_ref = face_data["texture"]
                            if not texture_ref.startswith("#"):
                                face_data["texture"] = f"#{texture_ref}"
        
        # Add Bedrock-specific metadata
        bedrock_model["bedrock_conversion"] = {
            "source_format": "java",
            "conversion_type": model_type,
            "bedrock_format": 1
        }
        
        return bedrock_model
    
    def _map_model_texture_path(self, java_path: str) -> str:
        """Map Java texture path dalam model ke Bedrock format"""
        bedrock_path = java_path
        
        # Konversi path components
        path_mappings = {
            "block/": "blocks/",
            "item/": "items/",
            "entity/": "entity/",
            "misc/": "misc/",
        }
        
        for java_prefix, bedrock_prefix in path_mappings.items():
            if java_path.startswith(java_prefix):
                bedrock_path = bedrock_prefix + java_path[len(java_prefix):]
                break
        
        return bedrock_path
    
    def create_render_controllers(self) -> List[str]:
        """Create render controllers untuk models"""
        render_controllers = []
        
        # Scan models dan create render controllers
        models_dir = self.bedrock_pack_path / "models"
        if models_dir.exists():
            for model_file in models_dir.rglob("*.json"):
                try:
                    with open(model_file, 'r') as f:
                        model_data = json.load(f)
                    
                    if "elements" in model_data:
                        # Create render controller for this model
                        model_name = model_file.stem
                        render_controller = self._generate_render_controller(model_name, model_data)
                        render_controllers.append(render_controller)
                
                except Exception as e:
                    self.logger.debug(f"Error processing model for render controller: {e}")
        
        return render_controllers
    
    def _generate_render_controller(self, model_name: str, model_data: Dict) -> Dict:
        """Generate render controller untuk model"""
        return {
            "format_version": "1.8.0",
            "render_controllers": {
                f"controller.render.{model_name}": {
                    "geometry": f"Geometry.default",
                    "materials": [
                        {
                            "*": "Material.default"
                        }
                    ],
                    "textures": [
                        f"Texture.{model_name}"
                    ]
                }
            }
        }
    
    def extract_custom_model_data(self) -> Dict:
        """Extract custom model data mappings dari Java models"""
        custom_models = {}
        
        item_models_path = self.bedrock_pack_path / "models" / "item"
        if item_models_path.exists():
            for model_file in item_models_path.rglob("*.json"):
                try:
                    with open(model_file, 'r') as f:
                        model_data = json.load(f)
                    
                    model_name = model_file.stem
                    
                    # Extract predicates dan custom model data
                    if "overrides" in model_data:
                        for override in model_data["overrides"]:
                            if "predicate" in override:
                                predicate = override["predicate"]
                                if "custom_model_data" in predicate:
                                    cmd = predicate["custom_model_data"]
                                    custom_models[f"{model_name}_{cmd}"] = {
                                        "model": model_name,
                                        "custom_model_data": cmd,
                                        "model_file": str(override.get("model", ""))
                                    }
                
                except Exception as e:
                    self.logger.debug(f"Error extracting custom model data: {e}")
        
        return custom_models
    
    def save_model_mappings(self) -> bool:
        """Save model mappings dan metadata"""
        try:
            self.logger.info("Creating model mappings")
            
            # Extract custom model data
            custom_models = self.extract_custom_model_data()
            if custom_models:
                with open(self.bedrock_pack_path / "_custom_model_data.json", 'w') as f:
                    json.dump(custom_models, f, indent=2)
            
            self.logger.info("Model mappings created")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save model mappings: {e}")
            self.stats["errors"] += 1
            return False
    
    def convert(self) -> bool:
        """Main convert method"""
        if not self.validate_java_pack():
            return False
        
        if not self.setup_output_structure():
            return False
        
        # Convert models
        if not self.convert_models():
            return False
        
        # Save model mappings
        if not self.save_model_mappings():
            return False
        
        self.logger.info("Model conversion finished successfully")
        return True
