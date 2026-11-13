# Pristine Auto Detailing Arlington

Static site for Pristine Auto Detailing Arlington, the detailing side of TAB Motors in Arlington, VA.

## Edit from anywhere

- **Business info** (phone, address, hours, domain): the CONFIG block at the top of `generate.py`
- **Prices, packages, page copy**: `content.py`
- **Quote form destination**: `WEBHOOK` at the top of `public/assets/quote.js`

After editing, run `python generate.py`, then `python tools/make_social_cards.py` if the logo, a headline, or a hero photo changed, and commit `public/`. Quick text fixes can also be made directly in the `public/` HTML on GitHub, but the next generator run will overwrite them.

Deploy with `vercel --prod` from this folder unless the Vercel project shows a connected GitHub repo.

## Photography

The photo library uses casual, natural-light illustrative photography. See [the photo guide](docs/photography.md) for filenames, placements, provenance, and generation prompts. The original storefront photograph remains unchanged.
