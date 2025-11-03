# Org Social RSS Bridge

A Flask-based bridge that converts RSS/Atom feeds into [Org Social](https://github.com/tanrax/org-social) format. This allows you to follow any RSS feed as if it were an Org Social account.


### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd org-social-rss-bridge
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Edit `.env` with your RSS feed URL and profile settings:
```bash
RSS_FEED_URL=https://xkcd.com/rss.xml
NICK=my-rss-feed
TITLE=My RSS Feed
DESCRIPTION=My favorite RSS feed in Org Social format
AVATAR=https://example.com/avatar.png
CONTACT=me@example.com
LANG=en
```

4. Build and start the service:
```bash
docker compose up -d
```

5. Access your Org Social feed at `http://localhost:5000`

### Using Python directly

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export RSS_FEED_URL=https://xkcd.com/rss.xml
export NICK=my-rss-feed
export TITLE="My RSS Feed"
export DESCRIPTION="My favorite RSS feed in Org Social format"
```

3. Run the application:
```bash
python app.py
```

## Configuration

All configuration is done via environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RSS_FEED_URL` | Yes | - | URL of the RSS/Atom feed to convert |
| `NICK` | No | `rss-bridge` | Your Org Social username (no spaces) |
| `TITLE` | No | `RSS Bridge` | Feed title (falls back to RSS feed title) |
| `DESCRIPTION` | No | `RSS to Org Social bridge` | Profile description (falls back to RSS feed subtitle) |
| `AVATAR` | No | - | Profile avatar URL (falls back to RSS feed image) |
| `CONTACT` | No | - | Contact information (email, XMPP, Matrix, etc.) |
| `LANG` | No | `en` | Default language for posts |

## Usagep

### Get the Org Social feed

Access the feed configured in your environment:
```bash
curl http://localhost:5000/
```

### Health check

Check if the service is running:

```bash
curl http://localhost:5000/health
```
