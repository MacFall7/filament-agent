# Filament Agent

**Undoable File Automation for Creators**

> A self-hosted automation kernel that intelligently organizes your Downloads folder with full undo capability. Built by [M87 Studio](https://m87.studio).

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/MacFall7/filament-agent)

## Why Filament?

Stop babysitting your Downloads folder. Filament routes files based on smart rules, handles duplicates gracefully, and lets you undo any session that goes wrong.

**The only file organizer with full session reversal.**

### vs. Commercial Alternatives

| Feature | Filament | Hazel | File Juggler | DropIt |
|---------|----------|-------|--------------|--------|
| **Price** | Free | $32 | $30 | $29 |
| **Undo Capability** | ✅ Full session reversal | ❌ | ❌ | ❌ |
| **Smart Keywords** | ✅ "invoice" → Finance | ❌ | ❌ | ❌ |
| **Cross-Platform** | ✅ Python anywhere | ❌ macOS only | ❌ Windows only | ❌ Windows only |
| **CLI Automation** | ✅ Scriptable | ❌ GUI only | ❌ GUI only | ❌ GUI only |
| **Dry Run Mode** | ✅ Safe preview | ❌ | ❌ | ❌ |
| **Open Source** | ✅ MIT License | ❌ | ❌ | ❌ |

## Quick Start

```bash
# Clone and setup
git clone https://github.com/MacFall7/filament-agent.git
cd filament-agent
pip install -r requirements.txt

# Preview what would happen (safe)
python filament.py --dry-run

# Actually organize files
python filament.py --run

# Undo last session
python filament.py --undo
```

## Smart Rules in Action

Filament understands context, not just file types:

```yaml
smart_rules:
  finance: ["invoice", "receipt", "tax", "statement"]
  work: ["contract", "proposal", "meeting", "agenda"]
  personal: ["photo", "vacation", "family"]
```

**Result:** `Q2_Invoice_AcmeCorp.pdf` automatically routes to `~/Documents/Finance/` even though it's a PDF.

## Features

- 🧠 **Smart categorization** - Keywords + file types
- ↩️ **Full undo capability** - Reverse any organization session
- 🧪 **Dry run mode** - Preview changes safely
- 📁 **Age-based archiving** - Auto-archive old files
- 🔄 **Duplicate handling** - Rename, skip, or overwrite
- 📝 **Session logging** - Track every move
- ⚙️ **Configurable rules** - YAML-based customization
- 🚀 **CLI-first design** - Perfect for automation
- 🌍 **Cross-platform** - Works anywhere Python runs

## Installation Options

### Option 1: Direct Download
```bash
curl -O https://raw.githubusercontent.com/MacFall7/filament-agent/main/filament.py
curl -O https://raw.githubusercontent.com/MacFall7/filament-agent/main/filament.yaml
python filament.py --help
```

### Option 2: Git Clone
```bash
git clone https://github.com/MacFall7/filament-agent.git
cd filament-agent
python filament.py --dry-run
```

### Option 3: Package Manager (Coming Soon)
```bash
brew install filament-agent  # macOS
pip install filament-agent   # Python
```

## Configuration

Edit `filament.yaml` to customize rules and destinations:

```yaml
# Add your own smart rules
smart_rules:
  music: ["mix", "master", "session", "track"]
  clients: ["client", "project", "deliverable"]

# Set your preferred destinations  
destinations:
  music: "~/Music/Projects"
  clients: "~/Work/Client_Files"
```

## Automation

### Daily Cleanup (Cron)
```bash
# Add to crontab: organize downloads daily at 2 AM
0 2 * * * cd ~/filament-agent && python filament.py --run
```

### On-Demand Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias organize='cd ~/filament-agent && python filament.py'
```

## Use Cases

### Knowledge Workers
- PDFs, contracts, invoices → organized by content
- Screenshots, downloads → cleaned up automatically
- Research files → routed to project folders

### Content Creators
- Media assets → sorted by type and project keywords
- Client deliverables → automatically filed
- Software downloads → separate from creative files

### Developers
- Documentation → categorized by technology
- Tools and utilities → organized by purpose
- Project files → routed to active workspace

### Productivity Enthusiasts
- Replace expensive commercial tools
- Integrate with existing automation workflows
- Maintain clean, organized file systems

## How It Works

### 1. Smart Detection
```
M87_Project_Proposal.pdf
├── Smart rule: "M87" → work category
├── File type: ".pdf" → documents category  
└── Winner: work (smart rules take precedence)
```

### 2. Safe Organization
```
🧪 DRY RUN MODE
🧠 WOULD MOVE: M87_Project_Proposal.pdf → work/
📁 WOULD MOVE: vacation_photos.zip → archives/
📁 WOULD MOVE: invoice_q3.pdf → finance/
```

### 3. Full Reversibility
```
python filament.py --undo
↩️  Undoing session: undo_2024-06-30_14-30-15
📁 Restoring: M87_Project_Proposal.pdf → Downloads/
✅ Restored 23/23 files
```

## Logs & Undo

Every session is logged and reversible:

```bash
# Session logs
logs/session_2024-06-30_14-30-15.log

# Undo data (JSON format)
undo/undo_2024-06-30_14-30-15.json

# Reverse last organization
python filament.py --undo
```

## Requirements

- Python 3.7+
- PyYAML (`pip install PyYAML`)
- Standard library modules (pathlib, shutil, etc.)

## Roadmap

- [ ] GUI application (Electron/Tauri)
- [ ] Package manager distribution (`brew`, `pip`)
- [ ] Cloud sync for rules
- [ ] AI-powered categorization
- [ ] Team/enterprise features
- [ ] Integration with popular productivity tools

## Contributing

Filament is open source (MIT License). Contributions welcome:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/MacFall7/filament-agent.git
cd filament-agent
pip install -r requirements.txt
python filament.py --help
```

## Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/MacFall7/filament-agent/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/MacFall7/filament-agent/discussions)
- 📧 **Contact:** [M87 Studio](https://m87.studio)

## License

MIT License - see [LICENSE](LICENSE) file.

## About M87 Studio

Filament Agent is a Labs project by [M87 Studio](https://m87.studio) - we build intelligent systems for creators and knowledge workers.

**M87 Studio Services:**
- Strategic consulting for creative teams
- Custom automation solutions
- Productivity infrastructure design
- Agent-native workflow development

---

⭐ **Star this repo** if Filament saves you time organizing files!

**Tried Hazel and want something better?** Filament Agent offers everything Hazel does, plus full undo capability and smart keyword detection - completely free.

**Built something cool with Filament?** We'd love to hear about it. Share your automation workflows and configurations!
