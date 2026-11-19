"""Notes: short posts about the work, written here first and copied elsewhere with a link back (D-25).

data/posts.json holds every note. A note with a "body" is published here: it gets its own page at notes/<id>.html and
an entry in feed.xml (Atom), which DEV and other sites import with this page as the canonical original. A note with a
"home" instead was first published elsewhere: it is listed with a link out and kept out of the feed, so no site
imports a duplicate. A note may name the projects it is about ("projects"): its page then shows each one in action,
with who it is for, what it does and a link to try it live, all taken from data/projects.json.

data/stories.json holds real stories of the projects in use (case studies). A story is published only with its
source, an https link to evidence and the date the person agreed to it being shared (D-28); there are no
illustrative or invented stories. Until a project has one, its page invites readers to share theirs.

Everything is validated before anything is written, and the build stops on the first problem (fail closed):
ids are lower-case slugs, dates are ISO dates, links are https to an allowed host, and a body uses only the
block types below. All text is escaped on output; nothing in the data is treated as HTML.
"""
import datetime as dt
import html
import json
import math
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
# A heading's icon, chosen from words in it; the first match wins (contextual iconography on note pages).
ICON_HINTS = (('find', 'compass'), ('where', 'compass'), ('trust', 'shield'), ('touch', 'chat'), ('contact', 'chat'),
              ('next', 'up'), ('why', 'info'), ('how', 'tool'), ('link', 'hub'), ('use', 'groups'))
WORDS_PER_MINUTE = 200


def _https(url, hosts=None):
    u = urllib.parse.urlsplit(url or '')
    return u.scheme == 'https' and bool(u.hostname) and (hosts is None or u.hostname in hosts)


def load(root=ROOT, project_ids=None):
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
        if project_ids is not None:
            unknown = [p for p in n.get('projects', []) if p not in project_ids]
            if unknown:
                raise SystemExit(f'posts.json: {nid} names projects that are not on the launchpad: {unknown}')
        posts.append(n)
    return sorted(posts, key=lambda n: n['date'], reverse=True)


def load_stories(root=ROOT, project_ids=()):
    """Read and validate data/stories.json: real stories of a project in use, each with its source, evidence and consent."""
    p = Path(root) / 'data' / 'stories.json'
    if not p.exists():
        return []
    out = []
    for s in json.loads(p.read_text(encoding='utf-8')).get('stories', []):
        sid = s.get('id', '')
        if not ID.match(sid):
            raise SystemExit(f'stories.json: bad id {sid!r}')
        if s.get('project') not in project_ids:
            raise SystemExit(f'stories.json: {sid} is about a project that is not on the launchpad')
        for f in ('who', 'what', 'outcome'):
            if not s.get(f):
                raise SystemExit(f'stories.json: {sid} needs {f}')
        if not _https(s.get('evidence')):
            raise SystemExit(f'stories.json: {sid} needs an https link to its evidence')
        dt.date.fromisoformat(s.get('consent', ''))  # the date the person agreed to the story being shared
        out.append(s)
    return out


def url(site, n):
    """Where a note lives: its page here, or its home elsewhere."""
    return n['home'] if 'home' in n else f'{site}notes/{n["id"]}.html'


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def icon_for(text):
    t = text.lower()
    return next((ico for word, ico in ICON_HINTS if word in t), 'book')


def reading_minutes(n):
    words = sum(len((v if isinstance(v, str) else ' '.join(v)).split()) for b in n.get('body', []) for v in b.values())
    return max(1, math.ceil(words / WORDS_PER_MINUTE))


def body_html(n, heading=None):
    """The note's body. heading(text) renders a section heading; the feed uses plain <h2>."""
    out = []
    for b in n.get('body', []):
        (k, v), = b.items()
        if k == 'ul':
            out.append(f'<ul>{"".join(f"<li>{e(x)}</li>" for x in v)}</ul>')
        elif k == 'h2' and heading:
            out.append(heading(v))
        else:
            out.append(f'<{k}>{e(v)}</{k}>')
    if n.get('links') and not heading:
        out.append('<h2>Links</h2><ul>' + ''.join(f'<li><a href="{e(x["url"])}">{e(x["text"])}</a></li>' for x in n['links']) + '</ul>')
    return '\n'.join(out)


def cards(site, posts):
    """The Notes section's list, for the launchpad page."""
    rows = []
    for n in posts:
        where = 'Published here' if 'body' in n else f'Published on {urllib.parse.urlsplit(n["home"]).hostname}'
        d = dt.date.fromisoformat(n['date'])
        rows.append(f'<article class="panel note-card" id="note-{e(n["id"])}"><p class="eyebrow"><time datetime="{e(n["date"])}">{d.day} {d:%B %Y}</time> · {where}</p>'
                    f'<h3><a href="{e(url(site, n))}">{e(n["title"])}</a></h3><p>{e(n["summary"])}</p></article>')
    return ''.join(rows)


def page(site, n, owner, kit):
    """A note's own page: a reading layout with its own canonical address (D-25, D-27).

    kit carries what the launchpad's build already draws: stylesheet, contact, icon(name, size), art (the note's
    signature drawing), qr, barcode, profiles, projects (those the note is about), cats, stories, others (other notes)."""
    icon = kit['icon']
    d = dt.date.fromisoformat(n['date'])
    name = owner.get('site_name') or owner['display_name']
    me = f'{site}notes/{n["id"]}.html'
    heads = [v for b in n['body'] for k, v in b.items() if k == 'h2']

    def heading(text):
        return f'<h2 id="{slug(text)}"><span class="tile sm" aria-hidden="true">{icon(icon_for(text), 16)}</span>{e(text)}</h2>'

    toc = ''
    if len(heads) >= 2:
        toc = ('<nav class="note-toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>'
               + ''.join(f'<li><a href="#{slug(h)}">{e(h)}</a></li>' for h in heads)
               + ('<li><a href="#in-action">See it in action</a></li>' if kit['projects'] else '') + '</ol></nav>')
    tags = ''.join(f'<li>#{e(t)}</li>' for t in n.get('tags', []))
    links = ''.join(f'<li><a href="{e(x["url"])}"><span class="tile sm" aria-hidden="true">{icon("hub", 16)}</span><span>{e(x["text"])}'
                    f'<small>{e(urllib.parse.urlsplit(x["url"]).hostname)}</small></span></a></li>' for x in n.get('links', []))
    links_html = f'<section class="note-links" aria-labelledby="links">{heading("Links")}<ul class="link-cards">{links}</ul></section>' if links else ''

    by_project = {}
    for s in kit['stories']:
        by_project.setdefault(s['project'], []).append(s)
    demos = ''
    for p in kit['projects']:
        c = kit['cats'][p['category']]
        hl = ''.join(f'<li>{e(h)}</li>' for h in p.get('highlights', [])[:3])
        told = ''.join(f'<blockquote class="story"><p>{e(s["what"])} {e(s["outcome"])}</p><footer>{e(s["who"])} · '
                       f'<a href="{e(s["evidence"])}">evidence</a></footer></blockquote>' for s in by_project.get(p['id'], []))
        demos += (f'<article class="demo c-{e(p["category"])}"><div class="demo-head"><span class="tile sm" aria-hidden="true">{icon(c.get("icon", "layers"), 16)}</span>'
                  f'<p class="eyebrow">{e(c["label"])} · {e(p["status"])}</p></div><h3>{e(p["name"])}</h3>'
                  f'<p class="demo-for"><strong>For:</strong> {e(p.get("audience", ""))}</p>'
                  + (f'<ul class="demo-hl">{hl}</ul>' if hl else '') + told
                  + f'<p class="demo-go"><a class="go" href="{e(p["site"])}">{icon("compass", 16)}Try it live</a>'
                  f'<a href="{e(p["repo"])}">Code</a></p></article>')
    action = ''
    if demos:
        action = (f'<section class="note-action" aria-labelledby="in-action"><h2 id="in-action"><span class="tile sm" aria-hidden="true">{icon("groups", 16)}</span>'
                  f'See it in action</h2><p>Every project below has a live site you can try now. Who each is for and what it does are taken from the project itself.</p>'
                  f'<div class="demo-grid">{demos}</div>'
                  f'<aside class="story-ask"><span class="tile sm" aria-hidden="true">{icon("chat", 16)}</span><p><strong>Using one of these?</strong> '
                  f'Real stories of the work in use are published here with the person\'s agreement and a link to the evidence. '
                  f'<a href="{e(kit["contact"])}">Share yours through the contact form</a>.</p></aside></section>')
    others = ''.join(f'<li><a href="{e(url(site, o))}">{e(o["title"])}</a> <span class="muted small">{dt.date.fromisoformat(o["date"]).day} '
                     f'{dt.date.fromisoformat(o["date"]):%B %Y}</span></li>' for o in kit['others'])
    more = f'<section class="note-more" aria-labelledby="more-notes"><h2 id="more-notes">More notes</h2><ul>{others}</ul></section>' if others else ''
    profiles = ' · '.join(f'<a rel="me" href="{e(p["url"])}">{e(p["name"])}</a>' for p in kit['profiles'])
    return f'''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(n["title"])}: {e(name)}</title>
<meta name="description" content="{e(n["summary"])}">
<link rel="canonical" href="{e(me)}">
<meta property="og:type" content="article"><meta property="og:title" content="{e(n["title"])}"><meta property="og:description" content="{e(n["summary"])}"><meta property="og:url" content="{e(me)}"><meta property="og:image" content="{site}og.jpg">
<link rel="alternate" type="application/atom+xml" href="/feed.xml" title="{e(name)}: notes">
<link rel="icon" href="{kit["favicon"]}">
<link rel="preload" href="/fonts/space-grotesk-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/{kit["stylesheet"]}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": n["title"], "description": n["summary"], "datePublished": n["date"], "url": me, "author": {"@type": "Person", "name": owner["display_name"], "url": site}, "keywords": n.get("tags", [])}, ensure_ascii=False).replace("</", "<\\/")}</script>
</head><body class="note-body">
<a class="skip" href="#main">Skip to content</a>
<div class="read-progress" aria-hidden="true"></div>
<header class="hero note-hero">{kit["starfield"]}
<div class="note-wrap">
<nav class="note-top" aria-label="Site"><a class="brand" href="/">{kit["mark"]}<span>{e(name)}<small>by {e(owner["display_name"])} · projects for better public services</small></span></a><a class="note-crumb" href="/#notes">{icon("book", 16)}All notes</a></nav>
<p class="eyebrow">Note · <time datetime="{e(n["date"])}">{d.day} {d:%B %Y}</time> · {reading_minutes(n)} min read</p>
<h1>{e(n["title"])}</h1>
{f'<ul class="note-tags" aria-label="Topics">{tags}</ul>' if tags else ''}
<div class="note-art c-standards" aria-hidden="true">{kit["art"]}</div>
</div></header>
<main class="note-page" id="main">
<article class="note-article">
<aside class="tldr" aria-labelledby="in-short"><h2 id="in-short"><span class="tile sm" aria-hidden="true">{icon("info", 16)}</span>In short</h2><p>{e(n["summary"])}</p></aside>
{toc}
<div class="prose">
{body_html(n, heading)}
</div>
{action}
{links_html}
</article>
{more}
</main>
<footer class="note-foot"><div class="note-wrap">
<p><strong>Written by {e(owner["display_name"])}.</strong> This page is the original; copies elsewhere link back here. Elsewhere: {profiles}</p>
<p><strong>Disclaimer.</strong> Personal projects and personal views. None is an official government service, policy or endorsement unless the project says so.</p>
<p><strong>Transparency.</strong> Written with help from Claude (Anthropic). The drawing at the top is generated in code from this note's id; there are no photographs and no third-party requests.</p>
<p><strong>Contact.</strong> <a href="{e(kit["contact"])}">Contact form</a> · <a href="/feed.xml">Notes feed</a> · <a href="/">All projects</a></p>
<div class="colophon" aria-label="Colophon">{kit["qr"]}<div class="bc">{kit["barcode"]}<span>{e(name)} · note · {e(n["id"])} · {e(n["date"])}</span></div></div>
</div></footer>
</body></html>
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
