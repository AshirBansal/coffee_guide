"""Checks the three tutorial pages: shared code identical, JSON parses, media files exist, editor-safe script."""
import json, os, re, sys

PAGES = ["grinder.html", "espresso.html", "drip.html"]
errors, blocks = [], {}

for page in PAGES:
    html = open(page, encoding="utf-8").read()
    style = re.search(r'<style id="app-style">(.*?)</style>', html, re.S)
    script = re.search(r'<script id="app-script">(.*?)</script>', html, re.S)
    data = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S)
    if not (style and script and data):
        errors.append(f"{page}: missing app-style, app-script or data block")
        continue
    blocks[page] = (style.group(1), script.group(1))
    if "<!--" in script.group(1):
        errors.append(f"{page}: app-script contains a literal '<!--', which breaks buildDoc")
    try:
        d = json.loads(data.group(1))
        if d.get("slug") + ".html" != page:
            errors.append(f"{page}: slug is {d.get('slug')!r}, so downloads would get the wrong file name")
        for i, step in enumerate(d.get("steps", []), 1):
            img = step.get("img", "")
            if img and not img.startswith("data:") and not os.path.isfile(img):
                errors.append(f"{page}: step {i} points to {img}, which isn't in the repo")
    except ValueError as e:
        errors.append(f"{page}: data block is not valid JSON ({e})")

if len(blocks) == len(PAGES):
    first = PAGES[0]
    for page in PAGES[1:]:
        for name, a, b in zip(("app-style", "app-script"), blocks[first], blocks[page]):
            if a != b:
                errors.append(f"{page}: {name} differs from {first}; apply code changes to all three pages")

print("\n".join(errors) or "All pages OK")
sys.exit(1 if errors else 0)
