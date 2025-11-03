import os
from flask import Flask, Response
import feedparser
from datetime import datetime
from html2text import html2text
import re

app = Flask(__name__)

# Environment variables
RSS_FEED_URL = os.getenv('RSS_FEED_URL', '')
NICK = os.getenv('NICK', 'rss-bridge')
TITLE = os.getenv('TITLE', 'RSS Bridge')
DESCRIPTION = os.getenv('DESCRIPTION', 'RSS to Org Social bridge')
AVATAR = os.getenv('AVATAR', '')
CONTACT = os.getenv('CONTACT', '')
LANG = os.getenv('LANG', 'en')


def html_to_org(html_content):
    """Convert HTML to Org mode format using html2text"""
    if not html_content:
        return ""

    # Convert HTML to markdown-like text
    text = html2text(html_content)

    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Convert markdown-style links to org-mode links
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'[[\2][\1]]', text)

    # Convert markdown bold to org bold
    text = re.sub(r'\*\*([^\*]+)\*\*', r'*\1*', text)

    # Convert markdown italic to org italic
    text = re.sub(r'_([^_]+)_', r'/\1/', text)

    # Clean up any remaining artifacts
    text = text.strip()

    return text


def parse_rss_to_org(feed_url):
    """Parse RSS/Atom feed and convert to Org Social format"""

    if not feed_url:
        return "Error: RSS_FEED_URL environment variable not set"

    # Parse the feed
    feed = feedparser.parse(feed_url)

    if feed.bozo and not feed.entries:
        return f"Error parsing feed: {feed.bozo_exception if hasattr(feed, 'bozo_exception') else 'Unknown error'}"

    # Build the Org Social file
    org_content = []

    # Header metadata
    feed_title = TITLE or feed.feed.get('title', 'RSS Bridge')
    org_content.append(f"#+TITLE: {feed_title}")
    org_content.append(f"#+NICK: {NICK}")

    if DESCRIPTION:
        org_content.append(f"#+DESCRIPTION: {DESCRIPTION}")
    elif hasattr(feed.feed, 'subtitle'):
        org_content.append(f"#+DESCRIPTION: {feed.feed.subtitle}")

    if AVATAR:
        org_content.append(f"#+AVATAR: {AVATAR}")
    elif hasattr(feed.feed, 'image') and 'href' in feed.feed.image:
        org_content.append(f"#+AVATAR: {feed.feed.image.href}")

    if CONTACT:
        org_content.append(f"#+CONTACT: {CONTACT}")

    org_content.append("")
    org_content.append("* Posts")
    org_content.append("")

    # Process each entry
    for entry in feed.entries:
        org_content.append("**")
        org_content.append(":PROPERTIES:")

        # ID (timestamp) - required field
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S+0000')
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            dt = datetime(*entry.updated_parsed[:6])
            timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S+0000')
        else:
            # Fallback to current time if no date available
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+0000')

        org_content.append(f":ID: {timestamp}")
        org_content.append(f":LANG: {LANG}")

        # Tags
        if hasattr(entry, 'tags') and entry.tags:
            tags = ' '.join([tag.term for tag in entry.tags if hasattr(tag, 'term')])
            if tags:
                org_content.append(f":TAGS: {tags}")

        org_content.append(":END:")
        org_content.append("")

        # Title
        if hasattr(entry, 'title') and entry.title:
            org_content.append(f"*** {entry.title}")
            org_content.append("")

        # Content
        content = ""
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].value
        elif hasattr(entry, 'summary') and entry.summary:
            content = entry.summary
        elif hasattr(entry, 'description') and entry.description:
            content = entry.description

        if content:
            org_text = html_to_org(content)
            org_content.append(org_text)
            org_content.append("")

        # Link to original
        if hasattr(entry, 'link') and entry.link:
            org_content.append(f"[[{entry.link}][Original post]]")
            org_content.append("")

        org_content.append("")

    return '\n'.join(org_content)


@app.route('/')
def index():
    """Main endpoint that returns the Org Social file"""
    org_content = parse_rss_to_org(RSS_FEED_URL)

    return Response(org_content, mimetype='text/plain; charset=utf-8')


@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'rss_feed_url': RSS_FEED_URL}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
