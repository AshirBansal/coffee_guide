# Coffee tutorials — repo brief for Claude Code

Context for a Claude Code session that maintains three QR-linked coffee machine tutorials. The point of working here rather than in a chat: edits land in the repo and ship by commit, instead of being handed back as HTML files to download and re-upload.

## What exists today

Three self-contained HTML pages, one per machine, deployed as static assets on a Cloudflare Worker at `coffee-guide.ashirbansal.workers.dev`, built from a GitHub repo.

| File | Live path | Steps |
| --- | --- | --- |
| `grinder.html` | `/grinder` | 6 |
| `espresso.html` | `/espresso` | 10 |
| `drip.html` | `/drip` | 7 |
| `index.html` | `/` | landing page linking to the three |

How each page works:

- All content lives in one JSON block in the page: `<script type="application/json" id="data">`. Shape: `{slug, icon, title, subtitle, accent:{light,dark}, steps:[{title, text, img}], outro:{title, text}}`.
- `img` is either an empty string, which renders a dashed "Photo for step N" placeholder SVG, or a `data:` URI holding a JPEG or GIF.
- The page renders a horizontal scroll-snap deck of cards from that JSON: one card per step, then a closing card. It opens straight on step 1; the header shows the machine's icon, title and subtitle on every card so people can tell which guide they're in.
- Adding `#edit` to the URL opens a built-in editor for photos and captions.
- CSS and JS are inlined in each file.

Content and code ship together. There is no database and no build step: the text of every step lives in the file that renders it.

## Working in this repo

Edit the files, commit to `main`, and Cloudflare redeploys within a minute or two. Nothing else to run.

- **To change wording or steps**, edit the JSON block in that page. Keep it valid JSON; the page parses it at load.
- **To change behaviour or styling**, edit the inlined `<style id="app-style">` or `<script id="app-script">`. The three pages carry identical copies of both, so a code change must be applied to all three files or they drift.
- **Photos arrive the other way.** Ashir adds them on his phone at `/<slug>#edit`, taps Download updated file, and commits the result. That downloaded file contains the whole page, so it overwrites any code change not yet committed. Pull before editing, and don't sit on uncommitted work.
- Photos are stored inline as `data:` URIs inside the JSON. Diffs on those lines are enormous and unreadable. Never reformat or reflow the JSON block; change only the fields asked for.
- Repo files that aren't pages (`README.md`, this file) are listed in `.assetsignore` so the Worker doesn't serve them. Add any new non-page file there too: they mention `#edit`.

## How a page file is laid out

Top to bottom: `<head>` with viewport and Google Fonts, `<style id="app-style">`, `<div id="root">`, the JSON data block, then `<script id="app-script">` holding everything in one IIFE.

What's in that script:

- `render()` builds the whole deck as an HTML string and wires the controls. `go()` and `update()` drive the scroll-snap navigation and the progress bars.
- `placeholder(n)` returns the dashed "Photo for step N" SVG used when `img` is empty.
- The editor is the back half: `renderEditor()`, `handlePhoto()` (downscales JPEGs to 1400px on a canvas, passes GIFs through untouched), and `download()`.
- `buildDoc(state)` is the load-bearing oddity. It rebuilds the entire HTML document by reading `#app-style` and `#app-script` `textContent` and re-emitting them around new JSON. That is how a page regenerates itself in the browser.

Because of `buildDoc`, the script's own source must never contain a literal `</script>` or `<!--`. The existing code writes them split up on purpose. Preserve that when editing.

## Open items

1. **Grinder blanks.** Steps 2 and 4 of `grinder.html` contain `setting ___` and `___ seconds`, waiting on the numbers the office settles on.
2. **No photos yet.** Every step still renders the placeholder. Expect large commits as photos land.
3. **Duplicated code.** The CSS and JS are copy-pasted across three files. A build step would fix it but would also break the self-regenerating editor, so the duplication is deliberate for now.
4. **Grind-setting labels** on the grinder page assume lower numbers are finer, which should be confirmed against the machine.
5. **Espresso shot times.** The "When to stop" card in `espresso.html` has `___ sec` blanks for a single and a double, waiting on someone timing a shot.

## Constraints

These break something physical or something already printed, so they outrank tidiness.

- **The three paths cannot change.** `/grinder`, `/espresso` and `/drip` are on QR stickers stuck to the machines. Don't rename files or add routing that turns them into redirects.
- **Keep each page one self-contained file.** No frameworks, no bundler, no CDN scripts. It loads on a phone on hospital wifi, and it is currently about 25 KB before photos.
- **Keep the `#edit` editor working.** It is how photos and captions get added. Any refactor that breaks `buildDoc` breaks the only path Ashir has from his phone.
- **Keep the embedded placeholder behaviour.** A step with an empty `img` must still render the dashed frame rather than a broken image.
- **Don't expose the editor publicly.** Nothing in the default view should mention or link to `#edit`.
- **Dark mode is handled by CSS custom properties** on `:root`, with a per-page accent pair. Add colours as tokens, not hex values in rules.

The filter situation is worth knowing: the workplace network blocks `coffee.gasguide.org`, which is why the site lives on `workers.dev`. If the custom domain is ever allowlisted, moving the site means adding a domain and reprinting labels, so keep hostnames out of the code.

## Checks before you commit

Open the changed files straight from disk in a browser, at a phone-sized viewport.

- [ ] Each page swipes end to end with no console errors.
- [ ] Step numbering and the "of N" counts match the number of steps.
- [ ] `#edit` opens, a photo can be added, and Download updated file produces a file that itself still renders and still edits.
- [ ] Dark mode looks right (toggle the OS setting or emulate `prefers-color-scheme`).
- [ ] A code change was applied to all three pages, not just the one being tested.
- [ ] The JSON block still parses and nothing outside the requested fields changed.
