import os
from pathlib import Path
import yaml
import shutil
import json
from datetime import datetime
import argparse
from collections import defaultdict

# Load configuration
config_path = Path.home() / "downloads_organizer/config.yaml"
if not config_path.exists():
    print(f"❌ Config file not found: {config_path}")
    exit(1)

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

rules = config.get("rules", {})
smart_rules = config.get("smart_rules", {})
destinations = config.get("destinations", {})
settings = config.get("settings", {})
archive_days = settings.get("archive_days", 30)
ignore_patterns = settings.get("ignore_patterns", [])

# Match filetype categories
def get_category(file_name):
    for category, patterns in rules.items():
        for pattern in patterns:
            if Path(file_name).match(pattern):
                return category
    return None

# Match keyword-based smart rules
def get_smart_category(file_name):
    name = file_name.lower()
    for category, keywords in smart_rules.items():
        for keyword in keywords:
            if keyword.lower() in name:
                return category
    return None

# Match ignore patterns
def should_ignore(file_name):
    for pattern in ignore_patterns:
        if Path(file_name).match(pattern):
            return True
    return False

# Handle duplicate files
def resolve_destination(dest_path):
    strategy = settings.get("duplicate_strategy", "rename")
    if not dest_path.exists():
        return dest_path
    if strategy == "overwrite":
        return dest_path
    elif strategy == "skip":
        return None
    elif strategy == "rename":
        stem, suffix = dest_path.stem, dest_path.suffix
        counter = 1
        while True:
            new_dest = dest_path.with_name(f"{stem}_{counter}{suffix}")
            if not new_dest.exists():
                return new_dest
            counter += 1
    else:
        return dest_path

# Organize logic
def organize_files(dry_run=False, no_log=False):
    source_dir = Path.home() / "Downloads"
    log_entries = []
    undo_data = {}
    summary = defaultdict(int)

    for item in source_dir.iterdir():
        if item.is_file():
            if should_ignore(item.name):
                continue

            category = get_category(item.name)
            if not category:
                category = get_smart_category(item.name)

            # Archive by age
            age = (datetime.now() - datetime.fromtimestamp(item.stat().st_mtime)).days
            if archive_days and age > archive_days:
                category = "old"

            if category and category in destinations:
                dest_dir = Path(os.path.expanduser(destinations[category]))
                dest_dir.mkdir(parents=True, exist_ok=True)
                target_path = resolve_destination(dest_dir / item.name)

                if not target_path:
                    continue  # skip duplicates if strategy is 'skip'

                if dry_run:
                    print(f"[DRY RUN] Move {item} -> {target_path}")
                else:
                    shutil.move(str(item), target_path)
                    log_entries.append(f"Moved {item} -> {target_path}")
                    undo_data[str(target_path)] = str(item)
                    summary[category] += 1

    # Logging
    if not dry_run and not no_log and log_entries:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        log_dir = Path.home() / "downloads_organizer/logs"
        undo_dir = Path.home() / "downloads_organizer/undo"
        log_dir.mkdir(parents=True, exist_ok=True)
        undo_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / f"session_{timestamp}.log", "w", encoding="utf-8") as f:
            f.write("\n".join(log_entries))
        with open(undo_dir / f"undo_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(undo_data, f, indent=2, ensure_ascii=False)

    # Summary
    if not dry_run:
        total = sum(summary.values())
        print(f"\n📊 SUMMARY REPORT")
        print(f"✅ {total} file(s) moved")
        for category, count in summary.items():
            print(f"📁 {category}: {count}")

# Undo logic
def undo_last():
    undo_dir = Path.home() / "downloads_organizer/undo"
    undo_files = sorted(undo_dir.glob("undo_*.json"), reverse=True)
    if not undo_files:
        print("❌ No undo files found.")
        return

    with open(undo_files[0], "r", encoding="utf-8") as f:
        undo_map = json.load(f)

    for src, dest in undo_map.items():
        try:
            shutil.move(src, dest)
            print(f"🔄 Undo: {src} -> {dest}")
        except Exception as e:
            print(f"❌ Failed to undo {src}: {e}")

# CLI
parser = argparse.ArgumentParser(description="Downloads Organizer Agent")
parser.add_argument("--run", action="store_true", help="Organize downloads now")
parser.add_argument("--dry-run", action="store_true", help="Preview actions")
parser.add_argument("--undo", action="store_true", help="Undo last session")
parser.add_argument("--no-log", action="store_true", help="Disable logging and undo tracking")
args = parser.parse_args()

if args.run:
    organize_files(dry_run=False, no_log=args.no_log)
elif args.dry_run:
    organize_files(dry_run=True, no_log=args.no_log)
elif args.undo:
    undo_last()
else:
    print("❗ Use --run, --dry-run, or --undo")
