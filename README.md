# Arlington Premier Auto Detailing

Static site for Arlington Premier Auto Detailing, the detailing side of TAB Motors in Arlington, VA.

## Edit from anywhere

- **Business info** (phone, address, hours, domain): the CONFIG block at the top of `generate.py`
- **Prices, packages, page copy**: `content.py`
- **Quote form destination**: `WEBHOOK` at the top of `public/assets/quote.js`

After editing, run `python generate.py` and commit `public/`. Quick text fixes can also be made directly in the `public/` HTML on GitHub, but the next generator run will overwrite them.

Deploy with `vercel --prod` from this folder unless the Vercel project shows a connected GitHub repo.

## Photography

The photo library uses casual, natural-light illustrative photography. See [the photo guide](docs/photography.md) for filenames, placements, provenance, and generation prompts. The original storefront photograph remains unchanged.
