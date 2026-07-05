# Yaswanth Kosuru — Portfolio

A single-page portfolio site imported from the Claude Design project
[`Yaswanth Portfolio.dc.html`](https://claude.ai/design/p/0e300976-71d6-4e68-a0f8-d10943234e01)
and compiled into a self-contained static website.

## Run it

It's plain static HTML — just serve the folder:

```bash
python3 -m http.server 8137
# open http://localhost:8137
```

(Opening `index.html` directly via `file://` also works, but a server is
recommended so the resume PDF and logo load with correct paths.)

## Structure

```
index.html                     # the compiled, self-contained site (open this)
assets/
  hero.css                      # header + hero stylesheet (mobile-first, grid/flex)
uploads/
  yklogo-removebg-preview.png   # logo (nav + footer)
  resume.pdf                    # linked resume
source/
  Yaswanth Portfolio.dc.html    # original Claude Design (.dc.html) source
  support.js                    # the Design-Craft runtime the source relied on
build.py                        # regenerates index.html from the .dc.html source
```

## How it was built

The original `.dc.html` is a Claude Design-Craft document: it uses custom
`<x-dc>` / `<helmet>` wrappers, `<sc-for>` template loops, and `{{ }}`
interpolation, all rendered at runtime by React via `support.js`.

`build.py` expands those loops and placeholders against the data defined in the
source's component, inlines the interaction JS (Lenis smooth scroll + the neon
cursor spotlight on the big name), and emits a dependency-free `index.html`.
Re-run it after editing the source:

```bash
python3 build.py
```

## Notes

- Fonts (Google Fonts), the Lenis smooth-scroll library (jsDelivr CDN), and the
  work/experience imagery (Unsplash) load from their CDNs, so the page needs a
  network connection to look complete. Everything else is local.
- The contact form has no backend — "Send request" opens a pre-filled email to
  `yaswanthkosuru999@gmail.com`.
