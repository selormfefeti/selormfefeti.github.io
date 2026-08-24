#!/usr/bin/env python3
"""Wrap the artifact fragment (index.html) into a standalone page in dist/.

index.html stays a fragment because the Artifact host supplies its own
<!doctype>/<head>/<body>. Static hosts do not, so this adds the pieces a real
deployment needs: charset, viewport, description, Open Graph, favicon.

Change SITE below once the domain is registered, then re-run.
"""
import io, os, re, shutil, urllib.parse

# --- where the site will live -------------------------------------------
# Leave DOMAIN empty to publish free on github.io. Set it once you own a
# domain, re-run, and the CNAME plus every absolute URL updates together.
GH_USER = "selormfefeti"
GH_REPO = "selormfefeti.github.io"           # user site -> shortest URL
DOMAIN  = ""                                 # e.g. "selormfefeti.com"

if DOMAIN:                                        # custom domain, served at the apex
    SITE = f"https://{DOMAIN}"
elif GH_REPO.lower() == f"{GH_USER.lower()}.github.io":   # user site, served at the root
    SITE = f"https://{GH_REPO}"
else:                                             # project site, served under a path
    SITE = f"https://{GH_USER}.github.io/{GH_REPO}"
TITLE = "Selorm Fefeti"
DESC  = ("Product Manager, ten years across AI, FinServ, and compliance platforms. "
         "Case studies on audit trail, enterprise self-service, and a data model rebuild.")

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "docs")   # GitHub Pages serves main branch /docs

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
           '<rect width="32" height="32" rx="6" fill="#8C2F2A"/>'
           '<text x="16" y="23" font-family="Georgia,serif" font-size="19" '
           'fill="#F6F7F9" text-anchor="middle">S</text></svg>')

def main():
    src = io.open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    split = src.index('<div class="shell">')
    head_frag, body = src[:split].strip(), src[split:].strip()

    # the fragment opens with its own <title>; the wrapper owns it instead
    head_frag = re.sub(r"<title>.*?</title>\s*", "", head_frag, count=1, flags=re.S)

    icon = "data:image/svg+xml," + urllib.parse.quote(FAVICON, safe="")
    head = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="author" content="{TITLE}">
<link rel="canonical" href="{SITE}/">
<link rel="icon" href="{icon}">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="{TITLE}">
<meta property="og:url" content="{SITE}/">
<meta property="og:title" content="{TITLE} - Product Manager">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{TITLE}, Product Manager">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE} - Product Manager">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/og.png">
{head_frag}"""

    os.makedirs(DIST, exist_ok=True)
    out = f"<!doctype html>\n<html lang=\"en\">\n<head>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    io.open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(out)
    for asset in ("og.png", "Selorm-Fefeti-Product-Portfolio.pdf"):
        src = os.path.join(HERE, asset)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DIST, asset))
            print(f"  docs/{asset}")
    cname = os.path.join(DIST, "CNAME")
    if DOMAIN:
        io.open(cname, "w", encoding="utf-8").write(DOMAIN + "\n")
        print(f"  docs/CNAME -> {DOMAIN}")
    elif os.path.exists(cname):
        os.remove(cname)          # a stale CNAME would break the github.io URL
    print(f"  docs/index.html  {len(out):,} bytes")
    print(f"  canonical        {SITE}")

if __name__ == "__main__":
    main()
