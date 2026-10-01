# Office coffee tutorials

Swipeable how-to pages for the office coffee machines, one per machine, linked from QR stickers.

| File | Live path |
| --- | --- |
| `index.html` | `/` (landing page) |
| `grinder.html` | `/grinder` |
| `espresso.html` | `/espresso` |
| `drip.html` | `/drip` |

## Hosting
Served as static assets by a Cloudflare Worker at `coffee-guide.ashirbansal.workers.dev`, built from this repo.
Every commit to `main` redeploys within a minute or two. There is no build step.
Don't rename the tutorial files: the paths are printed on the QR stickers.
`.assetsignore` keeps repo files like this one off the live site.

## Changing text
Each page keeps its content in the JSON block `<script type="application/json" id="data">`.
Edit that block and commit. Keep it valid JSON.

## Adding photos and captions
1. Open a tutorial with `#edit` on the end, e.g. `/espresso#edit`.
2. Add photos or GIFs, edit the steps, and tap Preview to check. Edits are kept on that device until you download.
3. Tap "Download updated file" and keep the name exactly as it is (e.g. `espresso.html`).
4. In GitHub, pull in any pending changes first, then Add file → Upload files, drop the file in, and commit to `main`.
   The downloaded file is the whole page, code included, so it replaces whatever is committed.

For animations, don't use the editor: GIFs are too big to go inside the page. Upload the GIFs (or short clips)
to a separate branch on GitHub and ask Claude to convert them; they become small videos in `media/<page>/`.

Photos are shrunk automatically. Keep GIFs short (under 6 MB each). Each page must stay under 25 MB or
GitHub and Cloudflare reject it; the editor shows the file size and warns from 15 MB.
Coworkers without `#edit` in the address never see the editor.

## Changing code or styling
The three tutorial pages carry identical copies of the CSS and JS, which lets each page rebuild itself
when downloaded from the editor. Apply any code change to all three. The `Check pages` GitHub Action
fails if they drift apart or a JSON block stops parsing; run `python3 .github/scripts/check_pages.py` locally.
See `CLAUDE.md` for the full maintenance notes.
