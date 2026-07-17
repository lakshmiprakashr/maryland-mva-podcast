# Troubleshooting Guide

Common issues and solutions.

---

## Setup Issues

### "uv: command not found"

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### "Python version not supported"

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.10+
# Ubuntu/Debian
sudo apt install python3.10

# macOS
brew install python@3.10
```

### "uv sync fails"

**Solution:**
```bash
# Clear cache
uv cache clean

# Refresh
uv sync --refresh
```

---

## Audio Generation Issues

### "edge-tts not found"

**Solution:**
```bash
uv sync
# or
pip install edge-tts
```

### "No audio generated"

**Solution:**
1. Check text files exist: `ls podcast/Driver-Manual/*.txt`
2. Check disk space: `df -h`
3. Check internet connection (edge-tts requires network)

### "Audio quality poor"

**Solution:**
- Check `config/podcast.yaml` settings
- Try different voice: `en-US-GuyNeural` or `en-US-JennyNeural`
- Increase bitrate in config

### "Audio generation slow"

**Expected:** Each chapter takes 1-3 minutes
**Total time:** ~30-60 minutes for all 35 chapters

**Speed up:**
- Generate specific chapters only
- Use faster network connection

---

## Podcast Generation Issues

### "feedgen not found"

**Solution:**
```bash
uv sync
# or
pip install feedgen
```

### "RSS feed invalid"

**Solution:**
1. Check XML syntax: `xmllint podcast/podcast.xml`
2. Validate with Apple's tool: https://podcasters.apple.com/support/823-podcast-requirements
3. Check all required tags present

### "Episodes not showing"

**Solution:**
1. Check `episodes.json` exists
2. Verify audio files are accessible
3. Check RSS feed is valid XML

---

## Deployment Issues

### "Netlify deployment fails"

**Solution:**
1. Check GitHub Actions logs
2. Verify secrets are set:
   - `NETLIFY_AUTH_TOKEN`
   - `NETLIFY_SITE_ID`
   - `NETLIFY_SITE_NAME`
3. Ensure `podcast/` directory exists

### "404 errors on site"

**Solution:**
1. Check file paths in RSS feed
2. Verify files exist in `podcast/`
3. Check Netlify publish directory is `podcast`

### "RSS feed not updating"

**Solution:**
```bash
# Clear Netlify cache
# Go to Netlify dashboard → Deploys → Clear cache

# Force refresh
curl -H 'Cache-Control: no-cache' https://mva-2tqlc3sd.netlify.app/podcast.xml
```

---

## Obsidian Vault Issues

### "Vault won't open"

**Solution:**
1. Ensure `.obsidian/` folder exists
2. Try creating new vault
3. Copy files to new vault

### "Audio won't play"

**Solution:**
- Audio files need to be downloaded separately
- See OBSIDIAN-VAULT-GUIDE.md for download instructions

### "Missing files"

**Solution:**
```bash
uv run python scripts/package_vault.py
```

---

## Practice Test Issues

### "Tests not generating"

**Solution:**
1. Check `obsidian-vault/04-Practice/` exists
2. Verify chapter files exist in `04-Artifacts/`
3. Check Python script has no errors

### "Wrong answers in tests"

**Solution:**
- Practice tests are auto-generated
- Verify against official Maryland MVA materials
- Report issues to maintainers

---

## Network Issues

### "Connection refused"

**Solution:**
1. Check internet connection
2. Try different network
3. Check if site is down: https://mva-2tqlc3sd.netlify.app

### "Timeout errors"

**Solution:**
1. Check network speed
2. Try again later
3. Use `--timeout` flag if available

---

## Still Stuck?

1. Check [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) for exact commands
2. Search GitHub issues: https://github.com/lakshmiprakashr/maryland-mva-podcast/issues
3. Create new issue with error message

---

## Related

- [QUICK-START.md](QUICK-START.md) - Get started
- [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - All commands
- [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) - Deployment setup
