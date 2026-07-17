# RSS Feed Specification

RSS feed format for the MVA Podcast.

---

## Feed Location

```
https://mva-2tqlc3sd.netlify.app/podcast.xml
```

---

## Feed Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:atom="http://www.w3.org/2005/Atom">
  
  <channel>
    <!-- Channel metadata -->
    <title>Maryland MVA Study Podcast</title>
    <link>https://mva-2tqlc3sd.netlify.app</link>
    <description>...</description>
    <language>en-us</language>
    <itunes:author>MVA Study Team</itunes:author>
    <itunes:category text="Education"/>
    <itunes:image href="..."/>
    
    <!-- Episodes -->
    <item>
      <title>Chapter 1: The Maryland DMV</title>
      <enclosure url="..." length="..." type="audio/mpeg"/>
      <itunes:duration>...</itunes:duration>
      <itunes:summary>...</itunes:summary>
    </item>
  </channel>
</rss>
```

---

## Required Tags

### Channel Tags

| Tag | Required | Description |
|-----|----------|-------------|
| `title` | Yes | Podcast title |
| `link` | Yes | Website URL |
| `description` | Yes | Podcast description |
| `language` | Yes | Language code |
| `itunes:author` | Yes | Author name |
| `itunes:category` | Yes | iTunes category |
| `itunes:image` | Yes | Artwork URL |

### Item Tags

| Tag | Required | Description |
|-----|----------|-------------|
| `title` | Yes | Episode title |
| `enclosure` | Yes | Audio file URL |
| `itunes:duration` | Yes | Duration (HH:MM:SS) |
| `itunes:summary` | Yes | Episode description |

---

## iTunes Tags

### Channel iTunes Tags

```xml
<itunes:author>MVA Study Team</itunes:author>
<itunes:summary>Study materials for Maryland MVA tests</itunes:summary>
<itunes:category text="Education"/>
<itunes:category text="Courses">
  <itunes:category text="Educational Technology"/>
</itunes:category>
<itunes:image href="https://mva-2tqlc3sd.netlify.app/artwork.jpg"/>
<itunes:explicit>false</itunes:explicit>
<itunes:type>episodic</itunes:type>
```

### Item iTunes Tags

```xml
<itunes:title>Chapter 1: The Maryland DMV</itunes:title>
<itunes:duration>1234</itunes:duration>
<itunes:summary>Learn about the Maryland DMV...</itunes:summary>
<itunes:episode>1</itunes:episode>
<itunes:episodeType>full</itunes:episodeType>
<itunes:explicit>false</itunes:explicit>
```

---

## Episode Numbering

### Driver Manual
- Episodes 1-10
- Chapter number = Episode number

### Rookie Manual
- Episodes 11-35
- Chapter number + 10 = Episode number

---

## Duration Format

### In RSS Feed
```xml
<itunes:duration>1234</itunes:duration>
```
Seconds as integer.

### In Display
```
20:34
```
MM:SS format.

---

## Artwork Requirements

| Requirement | Value |
|-------------|-------|
| Minimum size | 1400x1400 pixels |
| Maximum size | 3000x3000 pixels |
| Format | JPEG or PNG |
| Resolution | 72 dpi |
| Color space | RGB |

---

## Feed Validation

### Validate with Apple
https://podcasters.apple.com/support/823-podcast-requirements

### Validate with Podcast Validator
https://castfeedvalidator.com

### Check Feed Manually
```bash
# View feed
curl -s https://mva-2tqlc3sd.netlify.app/podcast.xml

# Count episodes
curl -s https://mva-2tqlc3sd.netlify.app/podcast.xml | grep -c "<item>"

# Check specific episode
curl -s https://mva-2tqlc3sd.netlify.app/podcast.xml | grep "Chapter 1"
```

---

## Common Issues

### "Feed not valid"
- Check XML syntax
- Ensure all required tags present
- Verify artwork URL is accessible

### "Episodes not appearing"
- Check `enclosure` URL is correct
- Verify audio files are accessible
- Ensure `itunes:duration` is present

### "Artwork not showing"
- Check artwork URL is accessible
- Verify image size (1400x1400 minimum)
- Ensure JPEG or PNG format

---

## Regenerate Feed

```bash
uv run python scripts/podcast_generator.py \
  --base-url "https://mva-2tqlc3sd.netlify.app"
```

---

## Related

- [APPLE-PODCASTS-GUIDE.md](APPLE-PODCASTS-GUIDE.md) - Apple submission
- [PODCAST-GENERATOR.md](PODCAST-GENERATOR.md) - Generator script
- [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) - Deployment
