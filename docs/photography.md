# Website photography

The November 6, 2026 refresh replaces all 16 generated service photographs with a casual phone-photo style with varied vehicles, imperfect framing, natural wear, and available light. These are AI-generated illustrative images, not documentation of actual customer vehicles, staff, or completed jobs. The existing `shop-front.jpg` is the original business photograph and remains unchanged. Logos and brand icons are unchanged.

The images were created with the built-in image generation tool. Full prompts are saved in `photo-prompts.json`: each entry contains the complete final prompt.

## Files and placement

All website JPEGs live in `public/assets/img/`. Existing photo filenames stay stable so every service, area, package, and blog page receives the replacement.

| File | Subject | Main use |
| --- | --- | --- |
| `hero.jpg` | Black sedan outside a service bay | Homepage and local-area hero |
| `foam.jpg` | Hand-wash foam on black paint | Express Clean and pricing |
| `interior.jpg` | Black leather rear cabin | Basic Detail |
| `polish.jpg` | Orbital polisher resting on a hood | Premium Full Detail and paint polish |
| `seats.jpg` | Burgundy and black leather seats | Interior Deep Detail |
| `wheel.jpg` | Clean alloy wheel and satin tire | Exterior Detail |
| `pethair.jpg` | Rubber brush beside collected dog hair | Pet Hair Removal |
| `seat.jpg` | Extraction nozzle on cloth upholstery | Seat and Carpet Shampoo |
| `carpet.jpg` | Extraction in a beige footwell | Carpet cleaning and local-area pages |
| `engine.jpg` | Clean satin-finish engine bay | Engine Bay Cleaning |
| `headlight.jpg` | Clear headlight on an older sedan | Headlight Restoration |
| `clay.jpg` | Clay bar resting on wet silver paint | Clay Bar Treatment |
| `wax.jpg` | Wax applicator resting on dark blue paint | Hand Wax or Sealant |
| `beads.jpg` | Irregular water droplets on paint | Paint protection and blog |
| `wheelseal.jpg` | Alloy wheel beside sealant bottle | Wheel Ceramic Sealant |
| `paint.jpg` | Continuous dark blue panel in daylight | Homepage paint-care section |
| `finished-suv.jpg` | Clean silver crossover | New: services hub; reusable for family vehicles |
| `dashboard-detail.jpg` | Dashboard with brush and towel on passenger seat | New: Interior Deep Detail supporting image |
| `hand-dry.jpg` | Drying towel draped over a white hood | New: Basic Detail supporting image |
| `headlight-work.jpg` | Headlight with protective tape and restoration tools | New: Headlight Restoration supporting image |

Images use optimized JPEG compression, with 1200-pixel service photos and larger landscape hero/paint images. The social preview at `public/assets/og-card-v1.jpg` uses the new hero photograph. The brand logo remains in the page header and existing logo files.

## Editing and rebuilding

Update image selections and alt text in `content.py` or `generate.py`, then run `python3 generate.py`. The generator preserves `public/assets/`.

`tools/prepare_assets.py` is the original one-time import utility. Its remote photo references describe the superseded image set. Do not use those URLs to restore missing photos; restore the current committed files from Git instead.

Before using these illustrations as a portfolio or before-and-after evidence, replace them with genuine photographs of the relevant work.
