# Cursor Scripts

Scripts for managing Cursor IDE.

## Cursor Reset Script

Reset Cursor trial with one command.

### One-Line Command (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/kunnew020/cursor-reset/main/reset.sh | bash
```

This command:
- ✅ Downloads and runs the reset script automatically
- ✅ Checks system compatibility (macOS only)
- ✅ Verifies Python 3 installation
- ✅ Guides you through the reset process interactively
- ✅ Cleans up automatically after completion

### Manual Download

```bash
# Download the script
curl -O https://raw.githubusercontent.com/kunnew020/cursor-reset/main/cursor_reset.py

# Make it executable
chmod +x cursor_reset.py

# Run with sudo
sudo python3 cursor_reset.py
```

### Important Notes

- ⚠️ **Quit Cursor before running the reset script**
- 🍎 This script only works on macOS
- 🔐 Requires admin password (uses sudo)
- 💾 Backups will be created automatically (.backup files)
- 🔄 Restart Cursor after the script completes

### What Gets Reset

**Machine IDs:**
- Device ID
- Machine ID
- Mac Machine ID
- SQM ID

**Configuration Files:**
- storage.json
- state.vscdb
- machineId file
- main.js (patched)

## License

MIT

