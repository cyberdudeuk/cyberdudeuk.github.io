"""Notes: short posts about the work, written here first and copied elsewhere with a link back (D-25).

data/posts.json holds every note. A note with a "body" is published here: it gets its own page at notes/<id>.html and
an entry in feed.xml (Atom), which DEV and other sites import with this page as the canonical original. A note with a
"home" instead was first published elsewhere: it is listed with a link out and kept out of the feed, so no site
imports a duplicate.

Everything is validated before anything is written, and the build stops on the first problem (fail closed):
ids are lower-case slugs, dates are ISO dates, links are https to an allowed host, and a body uses only the
block types below. All text is escaped on output; nothing in the data is treated as HTML.
"""
import datetime as dt
import html
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
e = html.escape
ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
BLOCKS = {'p', 'h2', 'ul'}
HOME_HOSTS = {'dev.to'}
LINK_HOSTS = {'cyberdudeuk.github.io', 'github.com', 'dev.to', 'orcid.org', 'www.linkedin.com', 'zenodo.org',
              'archive.softwareheritage.org', 'doi.org'}


def _https(url, hosts):
    u = urllib.parse.urlsplit(url or '')
    return u.scheme == 'https' and u.hostname in hosts


def load(root=ROOT):
    """Read and validate data/posts.json. Returns the notes, newest first."""
    data = json.loads((Path(root) / 'data' / 'posts.json').read_text(encoding='utf-8'))
    posts, seen = [], set()
    for n in data.get('posts', []):
        nid = n.get('id', '')
        if not ID.match(nid) or nid in seen:
            raise SystemExit(f'posts.json: bad or duplicate id {nid!r}')
        seen.add(nid)
        dt.date.fromisoformat(n.get('date', ''))  # raises on a bad date
        if not n.get('title') or not n.get('summary'):
            raise SystemExit(f'posts.json: {nid} needs a title and a summary')
        if ('body' in n) == ('home' in n):
            raise SystemExit(f'posts.json: {nid} needs exactly one of body (published here) or home (published elsewhere)')
        if 'home' in n and not _https(n['home'], HOME_HOSTS):
            raise SystemExit(f'posts.json: {nid} home must be https on {sorted(HOME_HOSTS)}')
        for b in n.get('body', []):
            if len(b) != 1 or next(iter(b)) not in BLOCKS:
                raise SystemExit(f'posts.json: {nid} has a block that is not one of {sorted(BLOCKS)}: {b}')
            v = next(iter(b.values()))
            if not (isinstance(v, str) or (isinstance(v, list) and all(isinstance(x, str) for x in v))):
                raise SystemExit(f'posts.json: {nid} block text must be text')
        for link in n.get('links', []):
            if not link.get('text') or not _https(link.get('url'), LINK_HOSTS):
                raise SystemExit(f'posts.json: {nid} link refused (https to a known host only): {link}')
        posts.append(n)
    return sorted(posts, key=lambda n: n['date'], reverse=True)


def url(site, n):
    """Where a note lives: its page here, or its home elsewhere."""
    return n['home'] if 'home' in n else f'{site}notes/{n["id"]}.html'


def body_html(n):
    out = []
    for b in n.get('body', []):
        (k, v), = b.items()
        out.append(f'<ul>{"".join(f"<li>{e(x)}</li>" for x in v)}</ul>' if k == 'ul' else f'<{k}>{e(v)}</{k}>')
    if n.get('links'):
        out.append('<h2>Links</h2><ul>' + ''.join(f'<li><a href="{e(x["url"])}">{e(x["text"])}</a></li>' for x in n['links']) + '</ul>')
    return '\n'.join(out)


def cards(site, posts):
    """The Notes section's list, for the launchpad page."""
    rows = []
    for n in posts:
        where = 'Published here' if 'body' in n else f'Published on {urllib.parse.urlsplit(n["home"]).hostname}'
        d = dt.date.fromisoformat(n['date'])
        rows.append(f'<article class="panel note" id="note-{e(n["id"])}"><p class="eyebrow"><time datetime="{e(n["date"])}">{d.day} {d:%B %Y}</time> · {where}</p>'
                    f'<h3><a href="{e(url(site, n))}">{e(n["title"])}</a></h3><p>{e(n["summary"])}</p></article>')
    return ''.join(rows)


def page(site, n, owner, stylesheet, contact):
    """A note's own page. Its canonical address is this page."""
    d = dt.date.fromisoformat(n['date'])
    name = owner.get('site_name') or owner['display_name']
    me = f'{site}notes/{n["id"]}.html'
    return f'''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(n["title"])}: {e(name)}</title>
<meta name="description" content="{e(n["summary"])}">
<link rel="canonical" href="{e(me)}">
<link rel="alternate" type="application/atom+xml" href="/feed.xml" title="{e(name)}: notes">
<link rel="stylesheet" href="/{stylesheet}">
</head><body><main class="wrap note-page" id="main">
<p class="eyebrow"><a href="/#notes">{e(name)}</a> · Notes · <time datetime="{e(n["date"])}">{d.day} {d:%B %Y}</time></p>
<h1>{e(n["title"])}</h1>
<p class="intro">{e(n["summary"])}</p>
{body_html(n)}
<hr><p class="small">Written by {e(owner["display_name"])}. This page is the original; copies elsewhere link back here. Personal views, not official policy.
<a href="/">All projects</a> · <a href="/feed.xml">Notes feed</a> · <a href="{e(contact)}">Contact form</a></p>
</main></body></html>
'''


def feed(site, posts, owner):
    """Atom feed of the notes published here (not the ones published elsewhere)."""
    own = [n for n in posts if 'body' in n]
    name = owner.get('site_name') or owner['display_name']
    updated = (own[0]['date'] if own else '2026-01-01') + 'T00:00:00Z'
    entries = ''.join(f'''
 <entry>
  <title>{e(n["title"])}</title>
  <link rel="alternate" type="text/html" href="{e(url(site, n))}"/>
  <id>{e(url(site, n))}</id>
  <published>{n["date"]}T00:00:00Z</published>
  <updated>{n["date"]}T00:00:00Z</updated>
  <summary>{e(n["summary"])}</summary>
  <content type="html">{e(body_html(n))}</content>{"".join(f'{chr(10)}  <category term="{e(t)}"/>' for t in n.get("tags", []))}
 </entry>''' for n in own)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-GB">
 <title>{e(name)}: notes</title>
 <subtitle>Notes on open tools for data and AI in public services, written here first.</subtitle>
 <link rel="self" type="application/atom+xml" href="{site}feed.xml"/>
 <link rel="alternate" type="text/html" href="{site}#notes"/>
 <id>{site}feed.xml</id>
 <updated>{updated}</updated>
 <author><name>{e(owner["display_name"])}</name><uri>{site}</uri></author>{entries}
</feed>
'''
