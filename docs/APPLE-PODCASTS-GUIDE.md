# Apple Podcasts Guide

Submit the MVA Podcast to Apple Podcasts and other platforms.

---

## Prerequisites

- Netlify site deployed and working
- RSS feed accessible at: https://mva-2tqlc3sd.netlify.app/podcast.xml
- Apple ID

---

## 1. Validate RSS Feed

Before submitting, validate your feed:

```bash
# Check feed is accessible
curl -s https://mva-2tqlc3sd.netlify.app/podcast.xml | head -20

# Validate with Apple's tool
# https://podcasters.apple.com/support/823-podcast-requirements
```

---

## 2. Create Apple Podcasts Connect Account

1. Go to https://podcastsconnect.apple.com
2. Sign in with Apple ID
3. Accept terms

---

## 3. Add Podcast

1. Click "+" to add podcast
2. Enter RSS feed URL:
   ```
   https://mva-2tqlc3sd.netlify.app/podcast.xml
   ```
3. Click "Submit"

---

## 4. Apple Review Process

- **Review time:** 24-48 hours (typically)
- **Requirements:**
  - Artwork: 1400x1400 to 3000x3000 pixels
  - At least 1 episode published
  - Valid RSS feed with required tags

---

## 5. Required RSS Tags

Already included in `podcast_generator.py`:

| Tag | Value |
|-----|-------|
| `itunes:title` | Maryland MVA Study Podcast |
| `itunes:author` | MVA Study Team |
| `itunes:summary` | Study materials for Maryland MVA tests |
| `itunes:image` | Artwork URL |
| `itunes:category` | Education |
| `itunes:explicit` | false |

---

## 6. Add Artwork

Create `podcast/artwork.jpg`:

- **Size:** 1400x1400 pixels (minimum)
- **Format:** JPEG or PNG
- **Resolution:** 72 dpi
- **Content:** Podcast title, relevant imagery

### Recommended Tools
- Canva: https://www.canva.com
- Figma: https://www.figma.com
- Adobe Express: https://www.adobe.com/express

---

## 7. Submit to Other Platforms

### Spotify
1. Go to https://podcasters.spotify.com
2. Click "Get Started"
3. Enter RSS feed URL
4. Verify ownership via email

### Google Podcasts
- Automatically discovers via RSS feed
- No manual submission needed
- Takes 24-48 hours to appear

### Amazon Music / Audible
1. Go to https://podcasters.amazon.com
2. Submit RSS feed

---

## 8. Post-Submission

After approval:

1. **Share the podcast link**
   - Apple Podcasts: `https://podcasts.apple.com/us/podcast/maryland-mva-study-podcast/id[your-id]`
   - Spotify: `https://open.spotify.com/show/[your-show-id]`

2. **Monitor analytics**
   - Apple Podcasts Connect shows downloads
   - Spotify for Podcasters shows plays

---

## Troubleshooting

### Feed rejected
- Check artwork size (1400x1400 minimum)
- Ensure all required tags present
- Verify audio files are accessible

### Podcast not appearing
- Wait 24-48 hours after approval
- Check RSS feed is valid
- Contact Apple support if >72 hours

---

## URLs

| Platform | URL |
|----------|-----|
| Apple Podcasts Connect | https://podcastsconnect.apple.com |
| Your Podcast (once approved) | https://podcasts.apple.com/us/podcast/maryland-mva-study-podcast/id[your-id] |
| RSS Feed | https://mva-2tqlc3sd.netlify.app/podcast.xml |

---

## Next Steps

- [RSS-FEED-SPECIFICATION.md](RSS-FEED-SPECIFICATION.md) - Feed format details
- [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) - Hosting setup
