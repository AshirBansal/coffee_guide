# Office coffee tutorials

Files:
- `index.html`: landing page listing all three tutorials
- `grinder.html`, `espresso.html`, `drip.html`: one swipeable tutorial each (these get the QR codes)

## Put it online (GitHub + Cloudflare Pages)
1. Create a GitHub repo (e.g. `coffee-tutorials`) and upload these files to it (the files themselves, not the folder).
2. In the Cloudflare dashboard, go to Workers & Pages → Create application → Pages → Connect to Git, and pick the repo.
3. Build settings: Framework preset "None", leave the build command empty, output directory `/`. Then Save and Deploy.
4. In the Pages project, go to Custom domains → Set up a custom domain → `coffee.gasguide.org`.
   Because gasguide.org is on Cloudflare, the DNS record is added automatically.
5. The tutorials are then live at:
   - https://coffee.gasguide.org/grinder
   - https://coffee.gasguide.org/espresso
   - https://coffee.gasguide.org/drip

## Add photos and captions
1. Open a tutorial with `#edit` on the end, e.g. `https://coffee.gasguide.org/espresso#edit`.
   (Opening the downloaded file straight from your computer works too.)
2. Add photos or GIFs, write the step titles and instructions, and reorder or delete steps as needed.
   Tap Preview to check it. Your edits are kept on that device until you download.
3. Tap "Download updated file". Keep the name exactly as it is (e.g. `espresso.html`).
4. In GitHub, click Add file → Upload files, drop the file in, and commit. It replaces the old one,
   and Cloudflare redeploys the site within a minute or two. The QR codes never change.

Tips: photos are shrunk automatically. Keep GIFs short (under ~6 MB each) so the page loads fast on phones.
Coworkers without `#edit` in the address never see the editor.
