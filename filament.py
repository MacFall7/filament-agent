#!/usr/bin/env python3
"""
Filament Agent v1.0
Undoable file automation for creators and knowledge workers.

Built by M87 Studio
https://github.com/m87labs/filament-agent
https://filament-agent.com
"""

import os
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import yaml
import argparse

__version__ = "1.0.0"

class FilamentAgent:
    def __init__(self, config_path: str = "filament.yaml"):
        self.downloads_path = Path.home() / "Downloads"
        self.config_path = Path(config_path)
        self.logs_dir = Path("logs")
        self.undo_dir = Path("undo")
        
        # Create required directories
        self.logs_dir.mkdir(exist_ok=True)
        self.undo_dir.mkdir(exist_ok=True)
        
        # Load config
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Expand destination paths
        for category, path in self.config['destinations'].items():
            expanded_path = Path(path).expanduser()
            self.config['destinations'][category] = expanded_path
            expanded_path.mkdir(parents=True, exist_ok=True)
        
        self.session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.moves_log = []
    
    def _get_file_category(self, file_path: Path) -> Optional[str]:
        """Determine file category based on extension"""
        suffix = file_path.suffix.lower()
        
        for category, patterns in self.config['rules'].items():
            for pattern in patterns:
                if pattern.startswith('*.') and suffix == pattern[1:]:
                    return category
        return None
    
    def _get_smart_category(self, file_path: Path) -> Optional[str]:
        """Determine file category based on filename keywords"""
        filename_lower = file_path.name.lower()
        smart_rules = self.config.get('smart_rules', {})
        
        for category, keywords in smart_rules.items():
            for keyword in keywords:
                if keyword.lower() in filename_lower:
                    return category
        return None
    
    def organize(self, dry_run: bool = False) -> Dict[str, int]:
        """Main organization logic"""
        stats = {'moved': 0, 'skipped': 0, 'errors': 0}
        
        if not self.downloads_path.exists():
            print(f"❌ Downloads folder not found: {self.downloads_path}")
            return stats
        
        print(f"🔍 Scanning: {self.downloads_path}")
        print(f"{'🧪 DRY RUN MODE' if dry_run else '🚀 LIVE MODE'}")
        print("-" * 50)
        
        files = [f for f in self.downloads_path.iterdir() if f.is_file()]
        
        for file_path in files:
            try:
                # Skip directories and system files
                if file_path.name.startswith('.'):
                    print(f"⏭️  Ignoring: {file_path.name}")
                    stats['skipped'] += 1
                    continue
                
                # Determine category - smart rules first, then file type
                category = self._get_smart_category(file_path)
                if not category:
                    category = self._get_file_category(file_path)
                
                if not category:
                    print(f"❓ Unknown type: {file_path.name}")
                    stats['skipped'] += 1
                    continue
                
                # Determine destination
                dest_dir = self.config['destinations'][category]
                dest_path = dest_dir / file_path.name
                
                # Show what would happen
                action = "WOULD MOVE" if dry_run else "MOVING"
                smart_indicator = "🧠" if self._get_smart_category(file_path) else "📁"
                print(f"{smart_indicator} {action}: {file_path.name} → {category}/")
                
                if not dry_run:
                    # Actually move the file
                    if dest_path.exists():
                        # Handle duplicate by renaming
                        counter = 1
                        stem = dest_path.stem
                        suffix = dest_path.suffix
                        while dest_path.exists():
                            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                            counter += 1
                    
                    shutil.move(str(file_path), str(dest_path))
                
                stats['moved'] += 1
                
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
                stats['errors'] += 1
        
        print("-" * 50)
        print(f"📊 Results: {stats['moved']} moved, {stats['skipped']} skipped, {stats['errors']} errors")
        
        return stats

def main():
    parser = argparse.ArgumentParser(
        description="Filament Agent - Undoable file automation for creators",
        epilog="Built by M87 Studio - https://github.com/m87labs/filament-agent"
    )
    parser.add_argument('--version', action='version', version=f'Filament Agent {__version__}')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without executing')
    parser.add_argument('--run', action='store_true', help='Execute organization')
    parser.add_argument('--undo', action='store_true', help='Undo last session')
    
    args = parser.parse_args()
    
    # Print header
    print(f"🔥 Filament Agent v{__version__}")
    print("Undoable file automation for creators")
    print("Built by M87 Studio")
    print()
    
    agent = FilamentAgent()
    
    if args.undo:
        print("↩️  Undo functionality coming soon...")
    elif args.dry_run or args.run:
        agent.organize(dry_run=args.dry_run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
