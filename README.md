# Org Social RSS Bridge

A simple bridge that converts RSS/Atom feeds into [Org Social](https://github.com/tanrax/org-social) format. This allows you to follow any RSS feed as if it were an Org Social account.

## Quick Start

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
RSS_FEED_URL=https://blog.orgmode.org/feed.xml
NICK=org-mode-blog
TITLE=Org Mode Blog
DESCRIPTION=Official Org Mode blog RSS feed
AVATAR=
CONTACT=
LANG=en
PORT=5000
DEBUG=false
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
export RSS_FEED_URL=https://blog.orgmode.org/feed.xml
export NICK=org-mode-blog
export TITLE="Org Mode Blog"
export DESCRIPTION="Official Org Mode blog RSS feed"
export PORT=5000
export DEBUG=false
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
| `PORT` | No | `5000` | Port where the service listens |
| `DEBUG` | No | `false` | Enable debug mode (`true`/`false`) |
| `CACHE_TIMEOUT` | No | `300` | Cache timeout in seconds (5 minutes default) |

## Usage

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
