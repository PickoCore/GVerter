"""
Minecraft Resource Pack Converter
Full conversion from Java Edition to Bedrock Edition with Geyser support
"""

__version__ = "1.0.0"
__author__ = "Resource Pack Converter Team"
__description__ = "Convert Minecraft Java resource packs to Bedrock Edition format"

from converter.core.resource_pack_converter import ResourcePackConverter
from converter.config import INPUT_DIR, OUTPUT_DIR

__all__ = [
    'ResourcePackConverter',
    'INPUT_DIR',
    'OUTPUT_DIR',
]
