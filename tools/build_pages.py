"""Build privacy.html, terms.html, 404.html, robots.txt, sitemap.xml and site.webmanifest.

Run from the project root:  python -I tools/build_pages.py
"""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://obsidianstudiodesigns.github.io/Thatch-Clean-Marloth/"
UPDATED = "November 2026"
WA = "https://wa.me/27825631277?text=Hi%20Andre%2C%20I%27d%20like%20a%20free%20quote%20for%20thatch%20cleaning."


def page(slug, title, desc, body, robots="index, follow"):
    canon = BASE + (slug if slug != "404.html" else "")
    return f"""<!DOCTYPE html>
<html lang="en-ZA" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
{'' if slug == '404.html' else f'<link rel="canonical" href="{canon}">'}
<meta name="theme-color" content="#0c2a52">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Thatch Clean Marloth">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}assets/img/og-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="icon" href="{'/Thatch-Clean-Marloth/' if slug == '404.html' else ''}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{'/Thatch-Clean-Marloth/' if slug == '404.html' else ''}favicon-32.png">
<link rel="apple-touch-icon" href="{'/Thatch-Clean-Marloth/' if slug == '404.html' else ''}apple-touch-icon.png">
<link rel="manifest" href="{'/Thatch-Clean-Marloth/' if slug == '404.html' else ''}site.webmanifest">
{'<base href="/Thatch-Clean-Marloth/">' if slug == '404.html' else ''}
<link rel="stylesheet" href="assets/css/style.css?v=2">
<script>document.documentElement.classList.replace('no-js','js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header{'' if slug == '404.html' else ' is-solid'}">
  <div class="wrap bar">
    <a class="brand" href="./" aria-label="Thatch Clean Marloth, home">
      <img class="logo-light" src="assets/img/logo-header-light.svg" alt="Thatch Clean, eco thatch cleaning specialists" width="211" height="66">
      <img class="logo-dark" src="assets/img/logo-header.svg" alt="" width="211" height="66" aria-hidden="true">
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="./#services">Services</a>
      <a href="./#process">How it works</a>
      <a href="./#faq">FAQ</a>
      <a class="btn btn--gold" href="{WA}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="assets/icons.svg#i-whatsapp-logo"></use></svg>Get a free quote</a>
    </nav>
    <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">
      <svg class="icon i-menu" aria-hidden="true"><use href="assets/icons.svg#i-list"></use></svg>
      <svg class="icon i-close" aria-hidden="true"><use href="assets/icons.svg#i-x"></use></svg>
    </button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer__bottom" style="margin-top:0;border-top:0;padding-top:0">
      <span>&copy; <span id="yr">{date.today().year}</span> Thatch Clean Marloth. <a href="privacy.html">Privacy policy</a> &nbsp; <a href="terms.html">Terms of use</a></span>
      <span class="credit">Website designed by <a href="https://obsidianstudiodesigns.co.za/" target="_blank" rel="noopener">Obsidian Studio Designs</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js?v=2" defer></script>
</body>
</html>
"""


PRIVACY = f"""<div class="legal-head"><div class="wrap"><h1>Privacy policy</h1><p>Protection of Personal Information Act, 2013 (POPIA). Last updated {UPDATED}.</p></div></div>
<div class="wrap legal">
<p>Thatch Clean Marloth ("Thatch Clean", "we", "us") cleans, fumigates and restores thatch and timber in Marloth Park. This policy explains what personal information we collect when you contact us or ask for a quote, why we need it, and the rights you have under POPIA.</p>

<h2>1. Who is responsible</h2>
<p>The responsible party is Thatch Clean, owned and run by Andre Wiid, Marloth Park, Mpumalanga. Andre is also our Information Officer. You can reach him on <a href="tel:+27825631277">082 563 1277</a> (call or WhatsApp) or at <a href="mailto:wiidandre59@gmail.com">wiidandre59@gmail.com</a>.</p>

<h2>2. What we collect</h2>
<ul>
<li>Your name, phone or WhatsApp number and email address.</li>
<li>The address or area of the property, and details about the work you need (for example the size of the thatch area, photos you send us and when it was last cleaned).</li>
<li>Records of quotes, bookings, invoices and payments.</li>
</ul>
<p>This website does not take payments and does not ask for card or banking details.</p>

<h2>3. How the quote form works</h2>
<p>The quote form on this website does not store anything on a server. When you press "Send on WhatsApp", your browser opens WhatsApp with your message filled in, and nothing is sent until you send it yourself. Messages you send us on WhatsApp are also handled under WhatsApp's own privacy terms.</p>

<h2>4. Why we use it</h2>
<ul>
<li>To reply to your enquiry, visit the property and give you a quote.</li>
<li>To schedule and carry out the work, and to follow up afterwards.</li>
<li>To keep the accounting and tax records the law requires.</li>
</ul>
<p>We only use your information for these purposes. We do not sell or rent it, and we will not send you marketing messages without your consent.</p>

<h2>5. Who we share it with</h2>
<p>We share your information only when we need to: with team members working on your job, with service providers we rely on to run the business (such as our phone, email and accounting providers), or when the law requires it.</p>

<h2>6. How long we keep it</h2>
<p>Enquiries that do not lead to work are deleted within 12 months. Quotes, invoices and job records are kept for as long as tax law requires (currently five years), then deleted.</p>

<h2>7. Keeping it safe</h2>
<p>We take reasonable steps to protect your information against loss, misuse and unauthorised access, including password-protected devices and accounts.</p>

<h2>8. This website</h2>
<p>This website does not use advertising cookies or tracking analytics, and it does not ask you to log in. It is hosted on GitHub Pages, which may keep basic technical logs (such as IP addresses) to keep the service secure. Links to WhatsApp, Facebook and email open services that have their own privacy policies.</p>

<h2>9. Your rights</h2>
<p>Under POPIA you may ask what personal information we hold about you, ask us to correct or delete it, object to how we use it, and withdraw consent you have given. Contact Andre using the details above. If you are not happy with our response you may complain to the Information Regulator (South Africa) at <a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>

<h2>10. Changes</h2>
<p>We may update this policy from time to time. The latest version will always be on this page.</p>
</div>"""

TERMS = f"""<div class="legal-head"><div class="wrap"><h1>Terms of use</h1><p>Last updated {UPDATED}.</p></div></div>
<div class="wrap legal">
<p>These terms apply to your use of this website and to quotes from Thatch Clean Marloth ("Thatch Clean", "we", "us"). By using the website you accept them.</p>

<h2>1. About the information on this site</h2>
<p>We describe our services as accurately as we can, but the information here is general. The exact scope, method and price of any job are set out in the written quote we give you for your property. Some photographs on this website are illustrative and show the kind of work and setting we deal with, not a specific client's property.</p>

<h2>2. Quotes</h2>
<ul>
<li>Quotes are free and are based on what we see on site and what you tell us.</li>
<li>Unless the quote says otherwise, it is valid for 30 days.</li>
<li>If we find something during the work that the quote could not reasonably have covered (for example damaged thatch or rotten timber), we will tell you and agree any extra work and cost with you before going ahead.</li>
</ul>

<h2>3. Bookings and access</h2>
<p>Thatch cleaning runs over two visits: fumigation the day before, and cleaning and the freshener mist the next day. Please give us safe access to the areas being treated and let us know about pets, people with allergies or respiratory conditions, and anything fragile near the work area, so we can plan around them.</p>

<h2>4. Payment</h2>
<p>Payment terms are stated on your quote or invoice.</p>

<h2>5. Our responsibility</h2>
<p>We work carefully and take reasonable steps to protect your property. As far as the law allows, we are not responsible for loss caused by the existing condition of the thatch or timber, or by events outside our control. Nothing in these terms limits your rights under the Consumer Protection Act, 2008.</p>

<h2>6. Website content</h2>
<p>The text, design and images on this website belong to Thatch Clean or its designers and may not be copied for commercial use without permission. Links to other websites are provided for convenience; we are not responsible for their content.</p>

<h2>7. Privacy</h2>
<p>How we handle your personal information is explained in our <a href="privacy.html">privacy policy</a>.</p>

<h2>8. Law</h2>
<p>These terms are governed by the laws of the Republic of South Africa.</p>

<h2>9. Contact</h2>
<p>Andre Wiid, Thatch Clean, Marloth Park. <a href="tel:+27825631277">082 563 1277</a> or <a href="mailto:wiidandre59@gmail.com">wiidandre59@gmail.com</a>.</p>
</div>"""

NF = f"""<div class="nf"><div>
<h1>This page has gone missing.</h1>
<p>The link may be old, or the page may have moved. Everything you need is on the home page.</p>
<a class="btn btn--gold" href="./">Back to the home page<svg class="icon arrow" aria-hidden="true"><use href="assets/icons.svg#i-arrow-right"></use></svg></a>
</div></div>"""


def main():
    out = {
        "privacy.html": page("privacy.html", "Privacy policy | Thatch Clean Marloth",
                             "How Thatch Clean Marloth collects, uses and protects your personal information under POPIA.", PRIVACY),
        "terms.html": page("terms.html", "Terms of use | Thatch Clean Marloth",
                           "Terms for using the Thatch Clean Marloth website and for quotes on thatch cleaning and timber work.", TERMS),
        "404.html": page("404.html", "Page not found | Thatch Clean Marloth",
                         "This page could not be found.", NF, robots="noindex"),
    }
    for fn, html in out.items():
        open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(html)

    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n")

    today = date.today().isoformat()
    urls = [("", "1.0", "monthly"), ("privacy.html", "0.3", "yearly"), ("terms.html", "0.3", "yearly")]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, pri, freq in urls:
        xml.append(f"  <url>\n    <loc>{BASE}{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>")
        if path == "":
            xml.append(f"    <image:image><image:loc>{BASE}assets/img/hero-wide-1536.webp</image:loc></image:image>")
            xml.append(f"    <image:image><image:loc>{BASE}assets/img/og-share.jpg</image:loc></image:image>")
        xml.append("  </url>")
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(xml) + "\n")

    manifest = {
        "name": "Thatch Clean Marloth",
        "short_name": "Thatch Clean",
        "description": "Thatch cleaning, fumigation and timber restoration in Marloth Park.",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#0c2a52",
        "theme_color": "#0c2a52",
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    open(os.path.join(ROOT, "site.webmanifest"), "w").write(json.dumps(manifest, indent=2) + "\n")
    print("pages built")


if __name__ == "__main__":
    main()
