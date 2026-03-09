"""
File Utilities - Helper functions untuk file operations
"""

import shutil
import zipfile
from pathlib import Path
from typing import List, Optional


class FileUtils:
    """Utility class untuk file operations"""
    
    @staticmethod
    def copy_tree(src: Path, dest: Path, ignore_patterns: Optional[List[str]] = None) -> None:
        """Copy directory tree dengan optional ignore patterns"""
        def ignore_func(directory, contents):
            ignored = []
            for item in contents:
                if ignore_patterns:
                    for pattern in ignore_patterns:
                        if pattern in item:
                            ignored.append(item)
                            break
            return set(ignored)
        
        shutil.copytree(src, dest, ignore=ignore_func, dirs_exist_ok=True)
    
    @staticmethod
    def extract_zip(zip_path: Path, extract_to: Path) -> bool:
        """Extract zip file safely"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        except zipfile.BadZipFile:
            return False
    
    @staticmethod
    def create_zip(source_dir: Path, output_zip: Path) -> bool:
        """Create zip file dari directory"""
        try:
            shutil.make_archive(
                str(output_zip.with_suffix('')),
                'zip',
                source_dir
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path: Path) -> int:
        """Get file size dalam bytes"""
        return file_path.stat().st_size if file_path.exists() else 0
    
    @staticmethod
    def get_directory_size(dir_path: Path) -> int:
        """Get total size directory"""
        total = 0
        if dir_path.exists():
            for file_path in dir_path.rglob('*'):
                if file_path.is_file():
                    total += file_path.stat().st_size
        return total
    
    @staticmethod
    def ensure_directory(dir_path: Path) -> None:
        """Ensure directory exists"""
        dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def clean_directory(dir_path: Path) -> None:
        """Clean all contents dari directory"""
        if dir_path.exists():
            shutil.rmtree(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def list_files_recursive(dir_path: Path, extension: Optional[str] = None) -> List[Path]:
        """List all files recursively"""
        pattern = f"*.{extension}" if extension else "*"
        return list(dir_path.rglob(pattern))
