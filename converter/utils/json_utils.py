"""
JSON Utilities - Helper functions untuk JSON operations
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class JSONUtils:
    """Utility class untuk JSON operations"""
    
    @staticmethod
    def load_json(file_path: Path, default: Optional[Dict] = None) -> Dict[str, Any]:
        """Load JSON file safely"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return default or {}
    
    @staticmethod
    def save_json(file_path: Path, data: Dict, indent: int = 2, 
                 ensure_ascii: bool = False) -> bool:
        """Save JSON file safely"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
            return True
        except IOError:
            return False
    
    @staticmethod
    def merge_json(base: Dict, override: Dict) -> Dict[str, Any]:
        """Deep merge two JSON objects"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JSONUtils.merge_json(result[key], value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def get_nested(data: Dict, path: str, default: Any = None) -> Any:
        """Get nested value menggunakan dot notation"""
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    @staticmethod
    def set_nested(data: Dict, path: str, value: Any) -> Dict:
        """Set nested value menggunakan dot notation"""
        keys = path.split('.')
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
        return data
    
    @staticmethod
    def validate_json_schema(data: Dict, schema: Dict) -> bool:
        """Simple JSON schema validation"""
        try:
            import jsonschema
            jsonschema.validate(data, schema)
            return True
        except ImportError:
            # Fallback: basic type checking
            for key, value_type in schema.items():
                if key in data:
                    if not isinstance(data[key], value_type):
                        return False
            return True
        except Exception:
            return False
