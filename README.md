# Nova M&A Club website

`index.html` is the whole site in one file, with photos and font included. Open it in any browser. To put it online, upload that one file to any static host, such as Netlify Drop, GitHub Pages or Vercel.

## Before you publish

Open `src/index.html`, search for **"Edit these four values"** near the bottom, and fill in:

- `contactEmail`: the club inbox. It appears on the page, and the form opens the visitor's email app addressed to it.
- `formEndpoint` (optional): a form service URL, such as Formspree. When it is set, the form sends messages directly instead.

Then rebuild (see below). Until one of the two is set, the form tells visitors to message the club on LinkedIn.

## Swapping in your own photos

Replace a file in `src/assets/` with a new photo **under the same name**, then rebuild. Use WebP or JPG, roughly the shape listed here:

| File | Where it shows | Shape |
| --- | --- | --- |
| hero-club.webp, hero-group.webp, hero-trio.webp | First screen, cross-fading | Wide (16:10), people in the lower two thirds |
| about-pair.webp | About, under "Our vision" | 16:10 |
| opening-session.webp | "Our mission" (the picture that opens to full screen) | 16:9, dark |
| research-accretion.webp | What we do → Deal research | A page from a deal brief |
| tab-sessions.webp, tab-legal.webp, tab-community.webp | The other three tabs | 4:3 |
| card-bnp-workshop.webp | Sessions, large picture | 16:9 |
| card-bnp-team.webp, card-carlyle.webp | Sessions, two smaller pictures | 16:10 |
| join-portrait.webp | Joining the club | Portrait (4:5) |
| contact-campus.webp | Get in touch, background | Wide, dark |

To change what a photo says to screen readers, edit its `alt` text in `src/index.html`.

## Rebuild

```
python3 build.py
```

This writes `dist/index.html`, the single file you publish.
