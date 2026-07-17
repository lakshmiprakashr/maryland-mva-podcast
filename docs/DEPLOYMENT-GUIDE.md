# Deployment Guide

Deploy the MVA Podcast to Netlify with automated GitHub Actions.

---

## Prerequisites

- GitHub repository: `git@github.com:lakshmiprakashr/maryland-mva-podcast.git`
- Netlify account
- Netlify site ID: `mva-2tqlc3sd`

---

## 1. Set Up Netlify Site

### Via Netlify UI
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Select GitHub
4. Choose repository: `maryland-mva-podcast`
5. Build settings:
   - Build command: `echo "Static site"`
   - Publish directory: `podcast`
6. Click "Deploy site"

### Via Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Link site
netlify link --id=mva-2tqlc3sd
```

---

## 2. Set Up GitHub Secrets

Go to GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `NETLIFY_AUTH_TOKEN` | Your Netlify personal access token |
| `NETLIFY_SITE_ID` | `mva-2tqlc3sd` |
| `NETLIFY_SITE_NAME` | `mva-2tqlc3sd` |

### Get Netlify Auth Token
1. Go to https://app.netlify.com/user/applications
2. Personal access tokens → New access token
3. Copy token

---

## 3. GitHub Actions Workflow

The workflow is at `.github/workflows/deploy-netlify.yml`:

```yaml
name: Deploy to Netlify

on:
  push:
    branches: [main]
    paths:
      - 'podcast/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: ./podcast
          production-deploy: true
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

---

## 4. Deploy Changes

### Automatic Deployment
```bash
# Push to main branch triggers deployment
git add -A
git commit -m "Update podcast"
git push
```

### Manual Deployment
```bash
# Via Netlify CLI
cd podcast
netlify deploy --prod
```

---

## 5. Verify Deployment

```bash
# Check site
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/

# Check RSS feed
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/podcast.xml

# Check audio files
curl -s -o /dev/null -w "%{http_code}" https://mva-2tqlc3sd.netlify.app/Driver-Manual/Chapter-01.mp3
```

Expected: All return `200`

---

## URLs

| Resource | URL |
|----------|-----|
| Site | https://mva-2tqlc3sd.netlify.app |
| RSS Feed | https://mva-2tqlc3sd.netlify.app/podcast.xml |
| Episodes JSON | https://mva-2tqlc3sd.netlify.app/episodes.json |

---

## Troubleshooting

### Deployment fails
- Check GitHub Actions logs
- Verify secrets are set correctly
- Ensure `podcast/` directory exists

### 404 errors
- Check file paths in RSS feed
- Verify files exist in `podcast/` directory

### RSS feed not updating
- Clear Netlify cache
- Force refresh: `curl -H 'Cache-Control: no-cache' https://mva-2tqlc3sd.netlify.app/podcast.xml`

---

## Next Steps

- [APPLE-PODCASTS-GUIDE.md](APPLE-PODCASTS-GUIDE.md) - Submit to Apple Podcasts
- [NETLIFY-CONFIGURATION.md](NETLIFY-CONFIGURATION.md) - Advanced Netlify settings
