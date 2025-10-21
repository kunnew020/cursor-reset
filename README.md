# Cursor Scripts

Scripts for managing Cursor IDE.

## Cursor Reset Script

Reset Cursor trial with one command.

### One-Line Command

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/cursor-scripts/main/cursor_reset.py | sudo python3
```

### Manual Download

```bash
# Download the script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/cursor-scripts/main/cursor_reset.py

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

