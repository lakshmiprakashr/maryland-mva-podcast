# Netlify Configuration

Advanced Netlify settings and customization.

---

## Configuration File

`netlify.toml` in project root:

```toml
[build]
  publish = "podcast"
  command = "echo 'Static site'"

[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "*.mp3"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
    Content-Type = "audio/mpeg"

[[headers]]
  for = "*.xml"
  [headers.values]
    Cache-Control = "public, max-age=3600"
    Content-Type = "application/rss+xml"
```

---

## Key Settings

### Build Settings

| Setting | Value |
|---------|-------|
| Publish directory | `podcast` |
| Build command | `echo "Static site"` |
| Node version | 18 |

### Headers

| Header | Purpose |
|--------|---------|
| `X-Frame-Options` | Prevent clickjacking |
| `X-XSS-Protection` | XSS protection |
| `X-Content-Type-Options` | MIME type sniffing |
| `Cache-Control` | Browser caching |

### Caching

| File Type | Cache Duration |
|-----------|----------------|
| `*.mp3` | 1 year (immutable) |
| `*.xml` | 1 hour |
| `*.json` | 1 hour |
| `*.html` | No cache |

---

## Custom Headers

Add custom headers in `netlify.toml`:

```toml
[[headers]]
  for = "/podcast.xml"
  [headers.values]
    Content-Type = "application/rss+xml; charset=utf-8"
    Access-Control-Allow-Origin = "*"
```

---

## Redirects

Add redirects in `netlify.toml`:

```toml
[[redirects]]
  from = "/feed"
  to = "/podcast.xml"
  status = 200

[[redirects]]
  from = "/rss"
  to = "/podcast.xml"
  status = 200
```

---

## Environment Variables

Set in Netlify dashboard → Site settings → Build & deploy → Environment:

| Variable | Value |
|----------|-------|
| `NODE_VERSION` | 18 |

---

## Deploy Preview

Enable deploy previews for pull requests:

1. Netlify dashboard → Site settings → Build & deploy
2. Deploy previews → Enable

---

## Forms (Not Used)

Netlify Forms are not used for this project.

---

## Functions (Not Used)

Netlify Functions are not used for this project.

---

## Notifications

Set up deploy notifications:

1. Netlify dashboard → Site settings → Build & deploy → Notifications
2. Add email notification for failed deploys

---

## Performance

### Lighthouse Scores (Target)

| Metric | Score |
|--------|-------|
| Performance | 90+ |
| Accessibility | 95+ |
| Best Practices | 95+ |
| SEO | 90+ |

### Optimization Tips

1. **Compress images** - Use WebP format
2. **Minify HTML/CSS/JS** - If adding custom code
3. **Enable Brotli** - Automatic on Netlify
4. **Use CDN** - Automatic on Netlify

---

## Related

- [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) - Deployment setup
- [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - All commands
