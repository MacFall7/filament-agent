# Filament Agent

File organizer for your Downloads folder with full session reversal. Built by M87 Studio.

---

## What It Does

Filament moves files from your Downloads folder into organized destinations based on keyword rules and file types. Every session is logged and fully reversible — if something moved wrong, one command undoes the entire session.

---

## Quick Start

```bash
git clone https://github.com/MacFall7/filament-agent.git
cd filament-agent
pip install -r requirements.txt

# Preview what would happen (no changes made)
python filament.py --dry-run

# Run it
python filament.py --run

# Undo the last session
python filament.py --undo
```

---

## Configuration

Edit `filament.yaml` to define your rules and destinations:

```yaml
smart_rules:
  finance: ["invoice", "receipt", "tax", "statement"]
  work: ["contract", "proposal", "meeting", "agenda"]
  personal: ["photo", "vacation", "family"]

destinations:
  finance: "~/Documents/Finance"
  work: "~/Documents/Work"
  personal: "~/Pictures/Personal"
```

Smart rules take precedence over file type matching. `Q2_Invoice_AcmeCorp.pdf` routes to `Finance/` because of the keyword, not because it's a PDF.

---

## How Undo Works

Every session writes a JSON log to `undo/`. Running `--undo` reads the most recent log and moves every file back to its original path.

```bash
python filament.py --undo
# Restoring: invoice_q3.pdf -> Downloads/
# Restoring: vacation_photos.zip -> Downloads/
# Restored 23/23 files
```

---

## Requirements

- Python 3.7+
- PyYAML (`pip install PyYAML`)

---

## Project Context

Filament is a utility tool from the M87 Studio Forge track — standalone tools built separately from the core governance stack. For production agent governance infrastructure see [Spine Lite](https://github.com/MacFall7/M87-Spine-lite) and [m87-audit-agent](https://github.com/MacFall7/m87-audit-agent).

---

## License

MIT — © 2025 M87 Studio LLC.


