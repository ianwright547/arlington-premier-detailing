#!/usr/bin/env python3
"""Arlington Premier Auto Detailing site generator.

Edit the CONFIG block or the content in content.py, then run: python generate.py
Every page, sitemap.xml, robots.txt and llms.txt is rebuilt from this file.
"""
import json, os, shutil, html, re
from content import PACKAGES, ADDONS, SERVICES, AREAS, POSTS, HOME_FAQ

# ---------------- CONFIG: change a value here and every page follows ----------
SITE_URL = "https://arlington-premier-detailing.vercel.app"  # swap when the domain is live
NAME = "Arlington Premier Auto Detailing"
SHORT = "Arlington Premier"
PARENT = "TAB Motors Arlington"
PHONE_DISPLAY = "(703) 243-3080"
PHONE_TEL = "+17032433080"
EMAIL = "support@tabmotorsarlington.com"
STREET = "4035 Old Dominion Dr"
CITY = "Arlington"
STATE = "VA"
ZIP = "22207"
ADDRESS = f"{STREET}, {CITY}, {STATE} {ZIP}"
HOURS = [("Monday - Friday", "7:00 AM - 6:00 PM"), ("Saturday", "7:00 AM - 3:00 PM"), ("Sunday", "Closed")]
MAPS_Q = "TAB+Motors+Arlington+4035+Old+Dominion+Dr+Arlington+VA+22207"
MAPS_URL = f"https://www.google.com/maps/search/?api=1&query={MAPS_Q}"
MAPS_EMBED = f"https://www.google.com/maps?q={MAPS_Q}&hl=en&z=14&output=embed"
LASTMOD = "2026-11-06"
ASSET_V = "2"
PHOTO_V = "20261106-opt"
# ------------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
pages = []  # (path, title, description)

ARROW = "&rarr;"
e = html.escape


def price_pair(p):
    return f"${p['sedan']} sedan / ${p['suv']} SUV or truck"


def head(path, title, desc, schema, og_type="website", image=None, image_alt=None):
    url = SITE_URL + path
    image = image or "og/" + (path.strip("/").replace("/", "-") or "home") + ".jpg"
    image_alt = e(image_alt or f"{NAME} in Arlington, VA")
    article = (f'<meta property="article:published_time" content="{LASTMOD}">\n'
               f'<meta property="article:modified_time" content="{LASTMOD}">\n') if og_type == "article" else ""
    blocks = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#05080d">
<meta name="format-detection" content="telephone=yes">
<meta name="application-name" content="{SHORT}">
<meta name="apple-mobile-web-app-title" content="{SHORT}">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="US-VA">
<meta name="geo.placename" content="Arlington">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/{image}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{image_alt}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_US">
{article}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE_URL}/assets/{image}">
<meta name="twitter:image:alt" content="{image_alt}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/premier.css?v={ASSET_V}">
{blocks}
</head>
<body>
"""


def nav():
    svc = "".join(f'<a href="/services/{s["slug"]}/">{e(s["name"])}</a>' for s in SERVICES)
    area = "".join(f'<a href="/areas/{a["slug"]}/">{e(a["name"])}</a>' for a in AREAS)
    return f"""<header><nav class="nav" id="nav" aria-label="Main navigation">
  <div class="nav-logo"><a href="/" aria-label="{NAME} home"><img src="/assets/logo-nav.png" alt="{NAME} by TAB Motors logo" width="188" height="64"></a></div>
  <div class="nav-right">
    <a href="tel:{PHONE_TEL}" class="btn-nav">Call Now</a>
    <button class="nav-menu-toggle" id="navMenuToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <div class="nav-menu" id="navMenu">
    <button type="button" class="nav-menu-close" id="navMenuClose" aria-label="Close menu">&times;</button>
    <div class="nav-submenu"><button type="button" class="nav-submenu-toggle" aria-expanded="false">Services <span class="nav-caret">&#9662;</span></button><div class="nav-submenu-list">{svc}</div></div>
    <a href="/pricing/">Pricing</a>
    <div class="nav-submenu"><button type="button" class="nav-submenu-toggle" aria-expanded="false">Service Areas <span class="nav-caret">&#9662;</span></button><div class="nav-submenu-list">{area}</div></div>
    <a href="/about/">About</a>
    <a href="/blog/">Blog</a>
    <a href="/contact/">Contact</a>
  </div>
</nav></header>
"""


def footer():
    svc = "".join(f'<a href="/services/{s["slug"]}/">{e(s["name"])}</a>' for s in SERVICES[:7])
    area = "".join(f'<a href="/areas/{a["slug"]}/">{e(a["name"])}</a>' for a in AREAS)
    hours = "".join(f"<div><span>{d}</span><span>{h}</span></div>" for d, h in HOURS)
    return f"""<section class="fl-section">
  <div class="fl-grid">
    <div class="fl-map"><iframe src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map to {NAME}" allowfullscreen></iframe></div>
    <div>
      <div class="fl-label">{NAME}</div>
      <h3>By TAB Motors</h3>
      <address>{STREET}<br>{CITY}, {STATE} {ZIP}</address>
      <a class="fl-phone" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
      <div class="fl-hours">{hours}</div>
      <a class="fl-dir" href="{MAPS_URL}" target="_blank" rel="noopener">Get Directions {ARROW}</a>
    </div>
  </div>
</section>
<footer class="footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <img class="footer-logo-img" src="/assets/logo-nav.png" alt="{NAME}" width="188" height="64" loading="lazy">
      <p>Professional hand detailing in Arlington, VA. Express cleans, full details, interior and exterior packages, and add-on services with prices posted up front.</p>
      <p class="footer-contact">{PHONE_DISPLAY} &bull; {EMAIL}</p>
    </div>
    <div class="footer-col"><h5>Services</h5>{svc}<a href="/services/">All Services</a></div>
    <div class="footer-col"><h5>Service Areas</h5>{area}</div>
    <div class="footer-col"><h5>Company</h5><a href="/pricing/">Pricing</a><a href="/about/">About</a><a href="/blog/">Blog</a><a href="/contact/">Contact</a></div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 {NAME}. A TAB Motors company. Some photos are illustrative.</span></div>
</footer>
<script src="/assets/site.js?v={ASSET_V}"></script>
<script src="/assets/quote.js?v={ASSET_V}"></script>
</body>
</html>
"""


def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "AutoWash",
        "@id": SITE_URL + "/#business",
        "name": NAME,
        "url": SITE_URL + "/",
        "image": SITE_URL + "/assets/img/shop-front.jpg",
        "logo": SITE_URL + "/assets/logo-card.png",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "priceRange": "$49 - $299",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                    "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
        "parentOrganization": {"@type": "Organization", "name": PARENT},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "07:00", "closes": "15:00"},
        ],
        "areaServed": [{"@type": "City", "name": a["schema"]} for a in AREAS] + [{"@type": "City", "name": "Arlington, VA"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Auto detailing packages",
            "itemListElement": [
                {"@type": "Offer", "price": str(p["sedan"]), "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": p["name"]}} for p in PACKAGES
            ],
        },
    }


def crumbs(items):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + p}
            for i, (n, p) in enumerate(items)
        ],
    }


def faq_block(title, intro, faqs):
    items = "".join(
        f'<details class="faq-item pm-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs
    )
    return f"""<section class="pm-faq-section" id="faq"><div class="pm-narrow">
  <div class="pm-chip">FAQ</div>
  <h2 class="pm-h2">{e(title)}</h2>
  <p class="pm-sub">{e(intro)}</p>
  <div class="pm-faq-list">{items}</div>
</div></section>
"""


def package_cards():
    out = []
    for p in PACKAGES:
        feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
        cls = "pk-card pk-gold fade-up" if p.get("featured") else "pk-card fade-up"
        badge = '<span class="pk-badge">Most Complete</span>' if p.get("featured") else ""
        out.append(f"""<article class="{cls}">
  <div class="pk-head">{badge}<h3>{e(p['name'])}</h3><p>{e(p['tag'])}</p></div>
  <img src="/assets/img/{p['img']}.jpg" alt="{e(p['alt'])}" width="600" height="400" loading="lazy">
  <div class="pk-prices"><div><strong>${p['sedan']}</strong><span>Sedan</span></div><div><strong>${p['suv']}</strong><span>SUV / Truck</span></div></div>
  <ul>{feats}</ul>
  <div class="pk-time">Approx. {e(p['time'])}</div>
  <a class="pk-link" href="/services/{p['slug']}/">View Details {ARROW}</a>
</article>""")
    return f'<div class="pk-grid">{"".join(out)}</div>'


def addon_cards():
    out = []
    for a in ADDONS:
        out.append(f"""<a class="ad-card fade-up" href="/services/{a['slug']}/">
  <img src="/assets/img/{a['img']}.jpg" alt="{e(a['alt'])}" width="300" height="200" loading="lazy">
  <h3>{e(a['name'])}</h3><div class="ad-price">{e(a['price'])}</div></a>""")
    return f'<div class="ad-grid">{"".join(out)}</div>'


def quote_section(sub="Tell us about your vehicle and what it needs. We will follow up during shop hours."):
    return f"""<section class="quote-section section" id="quote">
  <div class="quote-section-inner">
    <h2 class="quote-section-heading">Get A Quote</h2>
    <p class="quote-section-sub">{e(sub)}</p>
    <div class="quote-box quote-multistep" id="quoteForm">
      <div class="qf-progress"><div class="qf-progress-track"><div class="qf-progress-bar" id="qfProgressBar"></div></div><div class="qf-progress-text" id="qfProgressText">Step 1 of 3</div></div>
      <div class="qf-steps">
        <div class="qf-step qf-step-active" data-step="1">
          <h3 class="qf-step-title">What are we detailing?</h3>
          <div class="qf-choices qf-choices-3x2">
            <button type="button" class="qf-choice" data-type="Sedan">Sedan</button>
            <button type="button" class="qf-choice" data-type="SUV">SUV</button>
            <button type="button" class="qf-choice" data-type="Truck">Truck</button>
          </div>
          <label class="qf-text-label" for="qfVehicleDetails">Year, make, model (optional)</label>
          <input type="text" id="qfVehicleDetails" class="qf-text-input" placeholder="e.g. 2021 Honda CR-V" autocomplete="off">
          <div class="qf-actions"><button type="button" class="qf-next" id="qfStep1Next" disabled>Next &rarr;</button></div>
        </div>
        <div class="qf-step" data-step="2">
          <button type="button" class="qf-back">&larr; Back</button>
          <h3 class="qf-step-title">Which package?</h3>
          <div class="qf-choices qf-choices-depth">
            <button type="button" class="qf-choice qf-depth" data-service="Express Clean"><span class="qf-depth-name">Express Clean</span><span class="qf-depth-sub">wash + quick interior, from $49</span></button>
            <button type="button" class="qf-choice qf-depth" data-service="Basic Detail"><span class="qf-depth-name">Basic Detail</span><span class="qf-depth-sub">clean and refreshed, from $129</span></button>
            <button type="button" class="qf-choice qf-depth qf-depth-popular" data-service="Premium Full Detail"><span class="qf-popular-badge">Most Complete</span><span class="qf-depth-name">Premium Full Detail</span><span class="qf-depth-sub">everything, inside and out, from $249</span></button>
            <button type="button" class="qf-choice qf-depth" data-service="Interior or Exterior Only"><span class="qf-depth-name">Interior or Exterior Only</span><span class="qf-depth-sub">from $119</span></button>
            <button type="button" class="qf-choice qf-depth" data-service="Help me choose"><span class="qf-depth-name">Help me choose</span><span class="qf-depth-sub">we will recommend one</span></button>
          </div>
        </div>
        <div class="qf-step" data-step="3">
          <button type="button" class="qf-back">&larr; Back</button>
          <h3 class="qf-step-title">Where should we reach you?</h3>
          <input type="text" id="qfName" class="qf-text-input" placeholder="Name" autocomplete="name">
          <input type="tel" id="qfPhone" class="qf-text-input qf-text-input-large" placeholder="Phone number" autocomplete="tel">
          <div class="qf-actions"><button type="button" class="qf-submit" id="qfSubmit">Send My Request &rarr;</button></div>
          <a class="qf-emergency-link" href="tel:{PHONE_TEL}"><span>Prefer to talk? Call {PHONE_DISPLAY}</span></a>
        </div>
        <div class="qf-step qf-success" data-step="success">
          <div class="qf-success-icon">&#10003;</div>
          <h3 class="qf-step-title">Almost done</h3>
          <p class="qf-step-sub" id="qfSuccessText">Your email app should now be open with your request filled in. Hit send, or call {PHONE_DISPLAY}.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def cta(h="Ready to See the Difference?", p="Book your detail at our Arlington shop today."):
    return f"""<div class="cta-band"><h2>{e(h)}</h2><p>{e(p)}</p>
<a class="btn-white" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
"""


def write(path, title, desc, schema, body, og_type="website"):
    title = title.strip()
    pages.append((path, title, desc))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S).group(1)
    h1 = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h1))).strip()
    full = head(path, title, desc, schema, og_type, image_alt=f"{h1} | {NAME}") + nav() + body + footer()
    full = re.sub(r'(/assets/img/[^"<> ]+\.jpg)(?=")', lambda m: f"{m[1]}?v={PHOTO_V}", full)
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8", newline="\n") as f:
        f.write(full)


def page_hero(crumb, h1, lede, img="hero", ctas=True, stats=None):
    cr = " <span class=\"sep\">/</span> ".join(
        [f'<a href="{p}">{e(n)}</a>' if p else f'<span class="here">{e(n)}</span>' for n, p in crumb]
    )
    btns = f"""<div class="svc3-hero-ctas"><a href="/contact/#quote" class="svc3-btn svc3-btn-primary">Get a Quote {ARROW}</a><a href="tel:{PHONE_TEL}" class="svc3-btn svc3-btn-ghost">Call {PHONE_DISPLAY}</a></div>""" if ctas else ""
    st = ""
    if stats:
        st = '<div class="svc3-hero-stats">' + "".join(
            f'<div class="svc3-stat"><div class="svc3-stat-label">{e(l)}</div><div class="svc3-stat-value">{e(v)}</div></div>' for l, v in stats
        ) + "</div>"
    return f"""<section class="svc3-hero has-video">
  <img class="svc3-hero-video" src="/assets/img/{img}.jpg" alt="" fetchpriority="high">
  <div class="svc3-hero-veil"></div>
  <div class="svc3-wrap">
    <div class="svc3-crumb">{cr}</div>
    <h1 class="svc3-h1">{h1}</h1>
    <p class="svc3-lede">{e(lede)}</p>
    {btns}{st}
  </div>
</section>
"""


def build_home():
    title = "Auto Detailing Arlington VA | Arlington Premier"
    desc = f"Professional auto detailing in Arlington, VA. Express cleans from $49, full details from $249. Interior, exterior and add-ons. Call {PHONE_DISPLAY}."
    cards = [
        ("premium-full-detail", "Premium Full Detail", "polish", "Orbital polisher and microfiber cloth on a car hood"),
        ("exterior-detail", "Exterior Detail", "wheel", "Freshly detailed wheel and tire on a black car in Arlington, VA"),
        ("interior-detail", "Interior Detail", "seats", "Deep cleaned burgundy leather seats after an interior detail in Arlington, VA"),
        ("express-clean", "Express Clean", "foam", "Foam hand wash on a black car during an express clean in Arlington, VA"),
    ]
    svc = "".join(
        f"""<a class="service-card fade-up" href="/services/{s}/" aria-label="{e(n)}"><div class="card-img-wrap"><img src="/assets/img/{i}.jpg" alt="{e(a)}" loading="lazy"></div><div class="card-overlay"><div class="card-title">{e(n)}</div><div class="card-price">View Details</div></div></a>"""
        for s, n, i, a in cards)
    icons = "".join(
        f'<div class="ic-item fade-up"><img src="/assets/icon-{k}.png" alt="" width="84" height="84" loading="lazy"><h3>{t}</h3><p>{d}</p></div>'
        for k, t, d in [
            ("cleaner", "Cleaner", "Hand washed and hand finished, inside and out."),
            ("protected", "Protected", "Wax, sealant and trim care that hold up to Virginia weather."),
            ("brighter", "Brighter", "Clear glass, restored headlights and paint with real depth."),
            ("lasting", "Longer Lasting", "Regular care keeps resale value and interiors in shape."),
        ])
    threats = [
        ("Road Salt and Brine", "Winter treatment on I-66, Route 50 and Glebe Road sticks to rockers, wheels and door jambs. A hand wash and clay treatment gets it off before it sits."),
        ("Spring Pollen", "Northern Virginia pollen coats paint and fills cowl vents and cabin carpets. Our interior packages pull it out of the places a car wash never reaches."),
        ("Tree Sap and Birds", "Arlington's tree canopy is great until you park under it. Sap and droppings etch clear coat, so clay and protection matter here."),
        ("Summer Humidity", "Spilled coffee and damp floor mats turn into odors fast in July. Carpet and seat shampoo removes the source, not just the smell."),
        ("Commuter Grime", "Stop-and-go traffic bakes brake dust into wheels and road film into paint. Exterior packages include full wheel and tire cleaning."),
        ("Pets and Kids", "Hair, crumbs and stains are what most interiors really need help with. Pet hair removal starts at $30 and pairs with any package."),
    ]
    tgrid = "".join(f'<div class="th-card fade-up"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in threats)
    steps = [("01", "Call or Request a Quote", "Tell us the vehicle and package. We will confirm the price and find a time that works."),
             ("02", "Drop Off at the Shop", f"Bring it to {STREET}. Drop it off on your way to work and pick it up when it is ready."),
             ("03", "We Detail It by Hand", "Express cleans take about an hour. A Premium Full Detail takes 3.5 to 5 hours."),
             ("04", "Pick Up and Walk Around", "We go over the car with you before you leave, so you can see the work for yourself.")]
    sgrid = "".join(f'<div class="process-step fade-up"><div class="step-num">{n}</div><h4>{e(t)}</h4><p>{e(d)}</p></div>' for n, t, d in steps)
    arealist = "".join(f'<li><a href="/areas/{a["slug"]}/">{e(a["name"])} {ARROW}</a></li>' for a in AREAS)
    body = f"""<main>
<section class="hero" id="home">
  <img class="hero-video" src="/assets/img/hero.jpg" alt="Clean black sedan outside an independent service bay" fetchpriority="high">
  <div class="hero-bg"></div>
  <div class="hero-content"><div class="hero-grid"><div>
    <div class="hero-badge"><div class="badge-text">Arlington, VA &bull; By TAB Motors</div></div>
    <h1>Professional Auto Detailing <br>Inside and Out in <span class="accent">Arlington, VA</span></h1>
    <p class="hero-sub">Premium care and an exceptional shine at a shop you already know. Packages from $49, with every price posted up front.</p>
    <div class="hero-ctas">
      <a class="btn-primary" href="#quote">Get A Quote {ARROW}</a>
      <a class="btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
    </div>
  </div></div></div>
</section>
<section class="ic-strip"><div class="ic-grid">{icons}</div></section>
<section class="section" id="services">
  <h2 class="section-heading">Auto Detailing Services in Arlington</h2>
  <p class="section-sub">From a quick clean to a full reset, done by hand at our Arlington shop.</p>
  <div class="services-grid">{svc}</div>
  <div class="services-cta"><a class="btn-primary" href="/services/">See All Services</a></div>
</section>
<section class="section pk-section" id="packages">
  <div class="section-label">Detailing Packages</div>
  <h2 class="section-heading">Prices Up Front. No Guessing.</h2>
  <p class="section-sub">Pick a package by vehicle size. Heavy soiling or oversized vehicles may cost more, and we will tell you before we start.</p>
  {package_cards()}
</section>
<section class="section" id="addons">
  <div class="section-label">Popular Add-Ons</div>
  <h2 class="section-heading">Add What Your Car Needs</h2>
  <p class="section-sub">Stack any of these onto a package, or book them on their own.</p>
  {addon_cards()}
</section>
{quote_section()}
<section class="ba-static"><div class="ba-static-inner">
  <img src="/assets/img/paint.jpg" alt="Soft tree reflections in clean dark blue car paint" loading="lazy" width="1600" height="900">
  <div class="ba-text"><div class="section-label">The Reality of Paint Care</div>
  <h2 class="section-heading">Clean Is Not the Same as Cared For</h2>
  <p>Automatic washes leave fine swirl marks and miss everything baked into the clear coat. A clay treatment lifts what washing leaves behind, a one-step polish brings back depth, and wax or sealant protects the finish so it stays that way longer.</p>
  <a class="btn-primary" href="/services/paint-polish/">See Paint Polish</a></div>
</div></section>
<section class="section">
  <div class="section-label">Simple and Easy</div>
  <h2 class="section-heading">How Detailing Works Here</h2>
  <p class="section-sub">Four steps, no surprises.</p>
  <div class="process-steps">{sgrid}</div>
</section>
<section class="section th-section" id="northern-virginia">
  <div class="section-label">Built for Northern Virginia</div>
  <h2 class="section-heading">What Arlington Does to Your Car</h2>
  <p class="section-sub">Every season here brings its own mess. These are the ones we see most.</p>
  <div class="th-grid">{tgrid}</div>
</section>
{faq_block("Auto Detailing Questions", "Straight answers about pricing, timing and what to expect.", HOME_FAQ)}
<section class="sa-section"><div class="sa-wrap">
  <div class="sa-head"><div class="pm-chip">Service Area</div><h2 class="pm-h2">Serving Arlington and Northern Virginia</h2>
  <p class="pm-sub">Our shop is in North Arlington, close to Cherrydale, Ballston and Route 29.</p></div>
  <ul class="sa-cities">{arealist}</ul>
  <div class="services-cta"><a class="btn-primary" href="/areas/">All Service Areas</a></div>
</div></section>
{cta()}
</main>
"""
    write("/", title, desc, [business_schema(), {
        "@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website",
        "name": NAME, "url": SITE_URL + "/"}], body)


def build_services_hub():
    body = "<main>" + page_hero([("Home", "/"), ("Services", None)], 'Auto Detailing <span class="light">Services</span>',
        "Five detailing packages and a full menu of add-ons, all done by hand at our shop in Arlington, VA.", "finished-suv") + f"""
<section class="section pk-section"><div class="section-label">Packages</div><h2 class="section-heading">Detailing Packages</h2>
<p class="section-sub">Prices are listed for sedans and for SUVs or trucks.</p>{package_cards()}</section>
<section class="section"><div class="section-label">Add-Ons</div><h2 class="section-heading">Add-On Services</h2>
<p class="section-sub">Add to any package, or book on their own.</p>{addon_cards()}</section>
{cta()}</main>
"""
    write("/services/", "Auto Detailing Services in Arlington, VA | Arlington Premier",
          "Every auto detailing service at Arlington Premier: express clean, basic and premium details, interior, exterior, paint polish, pet hair and more.",
          [crumbs([("Home", "/"), ("Services", "/services/")])], body)


def build_pricing():
    rows = "".join(
        f'<tr><td><a href="/services/{p["slug"]}/">{e(p["name"])}</a></td><td>${p["sedan"]}</td><td>${p["suv"]}</td><td>{e(p["time"])}</td></tr>' for p in PACKAGES)
    arows = "".join(f'<tr><td><a href="/services/{a["slug"]}/">{e(a["name"])}</a></td><td>{e(a["price"])}</td></tr>' for a in ADDONS)
    body = "<main>" + page_hero([("Home", "/"), ("Pricing", None)], 'Detailing <span class="light">Prices</span>',
        "What auto detailing costs at Arlington Premier. Every package and add-on price in one place.", "foam") + f"""
<section class="section"><h2 class="section-heading">Detailing Packages</h2>
<div class="tbl-wrap"><table class="pr-table"><thead><tr><th>Package</th><th>Sedan</th><th>SUV / Truck</th><th>Time</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2 class="section-heading pr-gap">Add-On Services</h2>
<div class="tbl-wrap"><table class="pr-table"><thead><tr><th>Add-On</th><th>Price</th></tr></thead><tbody>{arows}</tbody></table></div>
<p class="pr-note">Add-on prices are ranges because the work depends on the condition of the vehicle. We confirm the exact price before we begin.</p>
</section>{quote_section()}{cta()}</main>
"""
    write("/pricing/", "Car Detailing Prices Arlington VA | Arlington Premier",
          "Car detailing prices in Arlington, VA. Express Clean $49, Basic Detail $129, Premium Full Detail $249, plus add-on prices for every service.",
          [crumbs([("Home", "/"), ("Pricing", "/pricing/")])], body)


def build_service(s):
    path = f"/services/{s['slug']}/"
    n = s["name"]
    inc = "".join(
        f'<li><span class="svc3-list-num">{i+1:02d}</span><span class="svc3-list-item">{e(x)}</span></li>' for i, x in enumerate(s["included"]))
    pair = "".join(
        f'<li><span class="svc3-list-num">+</span><span class="svc3-list-item"><a href="/services/{sl}/">{e(nm)}</a></span></li>' for sl, nm in s["pairs"])
    steps = "".join(
        f'<div class="svc3-step"><div class="svc3-step-num">{i+1:02d}</div><div><h4>{e(t)}</h4><p>{e(d)}</p></div></div>' for i, (t, d) in enumerate(s["steps"]))
    specs = "".join(
        f'<div class="svc3-spec"><div class="svc3-spec-label">{e(l)}</div><div class="svc3-spec-value">{e(v)}</div></div>' for l, v in s["stats"])
    switch = "".join(
        f'<a href="/services/{o["slug"]}/" class="{"current" if o["slug"]==s["slug"] else ""}">{e(o["short"])}</a>' for o in SERVICES)
    paras = "".join(f"<p>{e(p)}</p>" for p in s["body"])
    body = "<main>" + page_hero([("Home", "/"), ("Services", "/services/"), (n, None)], s["h1"], s["lede"], s["img"], stats=s["stats"]) + f"""
<section class="svc3-section svc3-mix" id="overview"><div class="svc3-wrap">
  <div class="svc3-mix-head"><div class="svc3-eyebrow">The Service</div><h2 class="svc3-mix-h2">{e(s['headline'])}</h2></div>
  <div class="svc3-mix-row"><div class="svc3-mix-text">{paras}</div>
  <div class="svc3-mix-media"><img src="/assets/img/{s['img2']}.jpg" alt="{e(s['alt'])}" loading="lazy"></div></div>
</div></section>
<section class="svc3-section" id="included"><div class="svc3-wrap"><div class="svc3-lists">
  <div class="svc3-list-col"><div class="svc3-list-label">{e(price_label(s))}</div><h3>What&rsquo;s<br>Included</h3><ol class="svc3-list">{inc}</ol></div>
  <div class="svc3-list-col alt"><div class="svc3-list-label">Optional + Related</div><h3>Pairs<br>Well With</h3><ol class="svc3-list">{pair}</ol>
  <p class="svc3-list-note">Tell us what you want when you book and we will quote it all together.</p></div>
</div></div></section>
<section class="svc3-section" id="process"><div class="svc3-wrap"><div class="svc3-process-grid">
  <div class="svc3-process-intro"><div class="svc3-eyebrow">How We Work</div><h2 class="svc3-h2">The order matters.</h2>
  <p>We follow the same sequence on every {e(n)} at our Arlington shop, because skipped prep shows in the finish.</p></div>
  <div class="svc3-timeline">{steps}</div>
</div></div></section>
<section class="svc3-section" id="specs"><div class="svc3-wrap"><div class="svc3-eyebrow">At a Glance</div><h2 class="svc3-h2">What you&rsquo;re booking.</h2><div class="svc3-specs">{specs}</div></div></section>
<section class="svc3-section" id="switcher"><div class="svc3-wrap"><div class="svc3-switcher-label">Explore other services</div><div class="svc3-switcher">{switch}</div></div></section>
{faq_block(n + " Questions", "What Arlington drivers ask us most.", s["faqs"])}
<section class="svc3-cta"><div class="svc3-wrap"><div class="svc3-eyebrow">Arlington, VA</div><h2>Book your<br>{e(n)}.</h2>
<p>Call the shop or send a quote request with your year, make and model.</p>
<div class="svc3-cta-row"><a href="/contact/#quote" class="svc3-btn svc3-btn-primary">Get a Quote {ARROW}</a><a href="tel:{PHONE_TEL}" class="svc3-btn svc3-btn-ghost">Call {PHONE_DISPLAY}</a></div></div></section>
</main>
"""
    offer = {"@type": "Offer", "priceCurrency": "USD", "price": str(s["schema_price"]),
             "url": SITE_URL + path, "availability": "https://schema.org/InStock"}
    svc_schema = {"@context": "https://schema.org", "@type": "Service", "name": n, "serviceType": "Auto detailing",
                  "provider": {"@id": SITE_URL + "/#business", "@type": "AutoWash", "name": NAME, "telephone": PHONE_TEL,
                               "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"}},
                  "areaServed": {"@type": "City", "name": "Arlington, VA"}, "description": s["desc"], "offers": offer}
    write(path, s["title"], s["desc"], [svc_schema, crumbs([("Home", "/"), ("Services", "/services/"), (n, path)])], body)


def price_label(s):
    return s["stats"][0][1] if s["stats"] else ""


def build_areas():
    grid = "".join(
        f'<a class="ar-card fade-up" href="/areas/{a["slug"]}/"><h3>{e(a["name"])}</h3><p>{e(a["card"])}</p><span>Learn More {ARROW}</span></a>' for a in AREAS)
    body = "<main>" + page_hero([("Home", "/"), ("Service Areas", None)], 'Detailing Near <span class="light">You</span>',
        "Arlington Premier is a drop-off shop in North Arlington. These are the neighborhoods and towns we serve most.", "wheel") + f"""
<section class="section"><h2 class="section-heading">Where Our Customers Come From</h2><p class="section-sub">All detailing happens at our shop at {STREET}.</p><div class="ar-grid">{grid}</div></section>{cta()}</main>
"""
    write("/areas/", "Service Areas | Arlington Premier Auto Detailing",
          "Auto detailing for drivers across Arlington, Ballston, Clarendon, Rosslyn, Cherrydale, McLean and Falls Church, at our North Arlington shop.",
          [crumbs([("Home", "/"), ("Service Areas", "/areas/")])], body)
    for a in AREAS:
        path = f"/areas/{a['slug']}/"
        paras = "".join(f"<p>{e(p)}</p>" for p in a["body"])
        others = "".join(f'<a href="/areas/{o["slug"]}/" class="{"current" if o["slug"]==a["slug"] else ""}">{e(o["name"])}</a>' for o in AREAS)
        b = "<main>" + page_hero([("Home", "/"), ("Service Areas", "/areas/"), (a["name"], None)],
            f'Auto Detailing Near <span class="light">{e(a["name"])}</span>', a["lede"], a["img"]) + f"""
<section class="svc3-section svc3-mix"><div class="svc3-wrap"><div class="svc3-mix-head"><div class="svc3-eyebrow">{e(a['name'])}</div><h2 class="svc3-mix-h2">{e(a['headline'])}</h2></div>
<div class="svc3-mix-row"><div class="svc3-mix-text">{paras}</div><div class="svc3-mix-media"><img src="/assets/img/{a['img2']}.jpg" alt="{e(a['alt'])}" loading="lazy"></div></div></div></section>
<section class="section pk-section"><div class="section-label">Packages</div><h2 class="section-heading">Detailing Packages for {e(a['name'])} Drivers</h2><p class="section-sub">The same posted prices for every customer.</p>{package_cards()}</section>
{faq_block("Detailing Questions from " + a["name"], "A few things drivers ask us.", a["faqs"])}
<section class="svc3-section" id="switcher"><div class="svc3-wrap"><div class="svc3-switcher-label">Other areas we serve</div><div class="svc3-switcher">{others}</div></div></section>
{cta(p="Drop off at our North Arlington shop.")}</main>
"""
        write(path, a["title"], a["desc"], [crumbs([("Home", "/"), ("Service Areas", "/areas/"), (a["name"], path)])], b)


def build_blog():
    grid = "".join(
        f'<a class="bl-card fade-up" href="/blog/{p["slug"]}/"><img src="/assets/img/{p["img"]}.jpg" alt="{e(p["alt"])}" loading="lazy"><div><span>{e(p["cat"])}</span><h2>{e(p["h1"])}</h2><p>{e(p["desc"])}</p></div></a>' for p in POSTS)
    body = "<main>" + page_hero([("Home", "/"), ("Blog", None)], 'Detailing <span class="light">Guides</span>',
        "Plain advice on keeping a car clean in Northern Virginia, from the team at Arlington Premier.", "beads", ctas=False) + f"""
<section class="section"><div class="bl-grid">{grid}</div></section>{cta()}</main>
"""
    write("/blog/", "Car Care Blog | Arlington Premier Auto Detailing",
          "Car detailing guides for Northern Virginia drivers: pricing, how often to detail, winter salt, pollen and getting a car ready to sell.",
          [crumbs([("Home", "/"), ("Blog", "/blog/")])], body)
    for p in POSTS:
        path = f"/blog/{p['slug']}/"
        content = "".join(
            f"<h2>{e(x[1:])}</h2>" if x.startswith("#") else f"<p>{e(x)}</p>" for x in p["body"])
        links = "".join(f'<li><a href="/services/{s}/">{e(n)}</a></li>' for s, n in p["links"])
        b = f"""<main><section class="post-hero"><div class="post-crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {e(p['cat'])}</div>
<h1>{e(p['h1'])}</h1><div class="post-meta"><span>{e(p['cat'])}</span><span>Updated November 2026</span></div></section>
<article class="post-body"><img class="post-img" src="/assets/img/{p['img']}.jpg" alt="{e(p['alt'])}" width="1200" height="800">{content}
<h2>Related services</h2><ul>{links}</ul></article>{cta()}</main>
"""
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["h1"], "description": p["desc"],
               "datePublished": LASTMOD, "dateModified": LASTMOD, "image": f"{SITE_URL}/assets/img/{p['img']}.jpg",
               "author": {"@type": "Organization", "name": NAME}, "publisher": {"@id": SITE_URL + "/#business", "@type": "AutoWash", "name": NAME},
               "mainEntityOfPage": SITE_URL + path}
        write(path, p["title"], p["desc"], [art, crumbs([("Home", "/"), ("Blog", "/blog/"), (p["h1"], path)])], b, "article")


def build_about():
    vals = [("High Quality Products", "Professional cleaners, conditioners, waxes and sealants chosen for the surface in front of us."),
            ("Experienced Technicians", "Your car is handled by people who work on vehicles for a living."),
            ("Attention to Detail", "Door jambs, vents, seams and glass edges get the same care as the hood."),
            ("Great Prices and Value", "Every package price is posted, so you know the cost before you call."),
            ("Customer Satisfaction", "We walk the car with you at pickup so you can see the work for yourself.")]
    g = "".join(f'<div class="th-card fade-up"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in vals)
    body = "<main>" + page_hero([("Home", "/"), ("About", None)], 'About Arlington <span class="light">Premier</span>',
        "The detailing side of TAB Motors, at the same North Arlington shop.", "polish") + f"""
<section class="svc3-section svc3-mix"><div class="svc3-wrap"><div class="svc3-mix-head"><div class="svc3-eyebrow">Our Story</div><h2 class="svc3-mix-h2">A detailing shop with a real repair shop behind it.</h2></div>
<div class="svc3-mix-row"><div class="svc3-mix-text">
<p>{NAME} is the detailing division of TAB Motors, the AAA Approved Auto Repair shop at {STREET} in Arlington. Our neighbors already trust the shop with brakes and state inspections. Now the same location handles the look and feel of the car too.</p>
<p>We built the service around one idea: nobody should have to guess what a detail costs. Every package is listed by vehicle size with the time it takes, and every add-on has a posted range. You pick what the car needs, drop it off, and pick it up clean.</p>
</div><div class="svc3-mix-media"><img src="/assets/img/shop-front.jpg" alt="TAB Motors shop on Old Dominion Dr in Arlington, VA, home of Arlington Premier Auto Detailing" loading="lazy"></div></div></div></section>
<section class="section"><div class="section-label">What You Can Expect</div><h2 class="section-heading">Why Drivers Choose Us</h2><div class="th-grid">{g}</div></section>
{cta()}</main>
"""
    write("/about/", "About Arlington Premier Auto Detailing | By TAB Motors",
          "Arlington Premier Auto Detailing is the detailing division of TAB Motors, a AAA Approved Auto Repair shop in Arlington, VA.",
          [crumbs([("Home", "/"), ("About", "/about/")])], body)


def build_contact():
    hours = "".join(f"<div><span>{d}</span><span>{h}</span></div>" for d, h in HOURS)
    body = "<main>" + page_hero([("Home", "/"), ("Contact", None)], 'Book Your <span class="light">Detail</span>',
        "Call the shop or send a quote request. Tell us the vehicle and package and we will take it from there.", "foam") + quote_section() + f"""
<section class="section ct-grid">
  <div class="ct-card"><h2>Call</h2><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
  <div class="ct-card"><h2>Email</h2><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div class="ct-card"><h2>Visit</h2><a href="{MAPS_URL}" target="_blank" rel="noopener">{STREET}<br>{CITY}, {STATE} {ZIP}</a></div>
  <div class="ct-card"><h2>Hours</h2><div class="fl-hours">{hours}</div></div>
</section>{cta()}</main>
"""
    write("/contact/", "Contact & Book | Arlington Premier Auto Detailing",
          f"Book auto detailing in Arlington, VA. Call {PHONE_DISPLAY} or request a quote. {ADDRESS}. Open Monday to Saturday.",
          [crumbs([("Home", "/"), ("Contact", "/contact/")])], body)


def write_extras():
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for p, _, _ in pages)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    lines = [f"# {NAME}", "", f"> Professional auto detailing shop in Arlington, VA. Detailing division of TAB Motors.", "",
             f"- Address: {ADDRESS}", f"- Phone: {PHONE_DISPLAY}", f"- Email: {EMAIL}",
             "- Hours: " + "; ".join(f"{d} {h}" for d, h in HOURS), "", "## Packages"]
    lines += [f"- [{p['name']}]({SITE_URL}/services/{p['slug']}/): ${p['sedan']} sedan, ${p['suv']} SUV or truck, approx. {p['time']}" for p in PACKAGES]
    lines += ["", "## Add-ons"] + [f"- [{a['name']}]({SITE_URL}/services/{a['slug']}/): {a['price']}" for a in ADDONS]
    lines += ["", "## Pages"] + [f"- [{t}]({SITE_URL}{p})" for p, t, _ in pages]
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    nf = re.sub(r'<link rel="canonical"[^>]*>\n', "", head("/404/", "Page Not Found | Arlington Premier", "That page does not exist.", [], image="og/home.jpg")).replace(
        'content="index, follow, max-image-preview:large"', 'content="noindex"') + nav() + f"""<main><section class="section nf"><h1 class="section-heading">Page Not Found</h1>
<p class="section-sub">That page does not exist. Try our <a href="/services/">services</a> or call {PHONE_DISPLAY}.</p></section></main>""" + footer()
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(nf)


def main():
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if name in ("assets", "favicon.ico"):
                continue
            t = os.path.join(OUT, name)
            shutil.rmtree(t) if os.path.isdir(t) else os.remove(t)
    build_home(); build_services_hub(); build_pricing()
    for s in SERVICES:
        build_service(s)
    build_areas(); build_blog(); build_about(); build_contact(); write_extras()
    print(len(pages), "pages")


if __name__ == "__main__":
    main()
