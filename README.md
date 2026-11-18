# Thatch Clean Marloth

Website for Thatch Clean (Andre Wiid), eco thatch cleaning specialists in Marloth Park, Mpumalanga: thatch fumigation, deep thatch vacuuming, freshener mist, beam and deck restoration, and home maintenance.

Live: https://obsidianstudiodesigns.github.io/Thatch-Clean-Marloth/

- Static HTML, CSS and JavaScript with no build step, hosted on GitHub Pages from `main`.
- Content comes from the business's Facebook page and flyers (services, the three-step process, client comments, contact details).
- All photographs are AI-generated scene-setters (Figma, gpt-image). The Facebook images are flyers, not usable work photos. Swap in real before/after photos when the client has them.
- `tools/build_assets.py` makes the WebP images, the lapa logo mark, favicons, the icon sprite and the WhatsApp/social share image (`assets/img/og-share.jpg`) from the raw files in `_source/` (not in git).
- `tools/build_pages.py` makes the privacy policy, terms, 404, robots.txt, sitemap.xml and the manifest.
- The quote form has no backend: it opens WhatsApp to 082 563 1277 with the message filled in.
- Fonts: Bricolage Grotesque and Geist (self-hosted, OFL). Icons: Phosphor (MIT).

## To confirm with the client

- Which email to show: the Facebook page lists wiidandre59@gmail.com, one flyer shows willandres9@gmail.com. The site uses the Facebook one.
- Whether 066 205 6008 should be labelled "Office" or with a person's name.
- Names (or permission) for the three client comments, which are shown unattributed.
- Quote validity (terms default to 30 days) and data retention periods in the privacy policy.
- Whether they want a custom domain.

Designed by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).
