#!/usr/bin/env python3
"""Regenerate work.htm from projects.json. Run: python3 build_work.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
projects = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))

def esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))

def inline_paragraph(text, links):
    # Keep the small amount of intentional inline HTML (e.g. italic asides).
    # Inline links are inserted by matching their exact text in order.
    for item in links:
        text = text.replace(item["text"], f'<a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{item["text"]}</a>')
    return text

cards = []
for project in projects:
    link = ""
    if project.get("link"):
        link = (f'<a class="project-link" href="{esc(project["link"])}" '
                f'target="_blank" rel="noopener noreferrer">{esc(project.get("link_label", "Open"))}</a>')
    index = f'<div class="card-topline"><span class="project-type">{esc(project["category"])}</span>{link}</div>'
    title = f'<h2>{project["title"]}</h2>'
    paragraphs = "".join(
        f'<p>{inline_paragraph(p, project.get("inline_links", []))}</p>'
        for p in project.get("paragraphs", [])
    )
    media = ""
    if project.get("image"):
        media = f'<img class="project-image" src="{esc(project["image"])}" alt="{esc(project.get("alt", ""))}">'
    elif project.get("video"):
        media = (f'<video class="project-image project-video" autoplay loop muted playsinline '
                 f'aria-label="{esc(project.get("alt", ""))}"><source src="{esc(project["video"])}" type="video/mp4"></video>')
    cards.append(f'      <article class="project-card">\n        {index}\n        {title}\n        {paragraphs}\n        {media}\n      </article>')

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#080B12">
  <link rel="stylesheet" href="styles.css">
  <link rel="icon" type="image/png" href="images/icon.png">
  <title>Projects - NB</title>
</head>
<body>
  <header class="site-header">
    <a class="wordmark" href="index.html" aria-label="NB home">NB</a>
    <nav aria-label="Main navigation">
      <a href="index.html">Home</a>
      <a href="work.htm" aria-current="page">Projects</a>
      <a href="misc.htm">Misc</a>
    </nav>
  </header>
  <main class="site-main">
    <section class="page-intro">
      <p class="eyebrow">A FEW THINGS I'VE WORKED ON</p>
      <h1>Projects</h1>
      <p class="intro-copy"><i>Cue the highlight reel-</i></p>
    </section>
    <section class="project-grid" aria-label="Projects">
__CARDS__
    </section>
    <footer class="page-footer"><span>NB</span><span>Built with HTML &amp; CSS</span></footer>
  </main>
</body>
</html>
"""
(ROOT / "work.htm").write_text(template.replace("__CARDS__", "\n".join(cards)) + "\n", encoding="utf-8")
print(f"Updated work.htm with {len(projects)} projects.")
