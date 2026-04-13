### Search Website (Google-style) — CS50W Project 0

A clean, multi-page **search UI** that routes users to real Google results using the correct query parameters for:

- **Standard search**
- **“I’m Feeling Lucky”**
- **Image search**
- **Advanced search** (multiple criteria mapped to Google’s advanced parameters)

This project demonstrates solid fundamentals in **semantic page structure, CSS layout, and vanilla JavaScript DOM + URL construction**, delivered as a dependency-free static site.

---

### Why this is interesting (for employers)

- **Real integration surface**: the UI doesn’t “fake” results—it constructs URLs that Google understands and navigates there.
- **Multiple product flows**: separate pages for standard, image, and advanced search—mirrors a real-world feature split.
- **Readable, minimal stack**: no frameworks, no build tooling—just clear HTML/CSS/JS with straightforward logic.

---

### Pages

- **`index.html`**: Standard search + “I’m Feeling Lucky”, with navigation to the other modes.
- **`image.html`**: Image search mode.
- **`advanced.html`**: Advanced search form with four criteria fields.

---

### How it works (technical overview)

The behavior lives in **`script.js`**, which reads user input(s) from the DOM and sets `window.location.href` to Google endpoints:

- **Standard Search**: `https://www.google.com/search?q=<query>`
- **Feeling Lucky**: `https://www.google.com/search?q=<query>&btnI=I`
- **Image Search**: `https://www.google.com/search?q=<query>&udm=2`
- **Advanced Search**:
  - `as_q` (all these words)
  - `as_epq` (exact phrase)
  - `as_oq` (any of these words)
  - `as_eq` (none of these words)

Styling is shared via **`styles.css`**.

---

### Run locally

This is a static site—no install step required.

- **Option A (simplest)**: open `index.html` in your browser.
- **Option B (recommended)**: serve as a static site (avoids any browser file URL quirks).

```bash
cd "search"
python3 -m http.server 8000
```

Then open `http://localhost:8000` and click into `index.html`.

---

### Project structure

```text
.
├── index.html        # standard search + lucky
├── image.html        # image search
├── advanced.html     # advanced search fields
├── styles.css        # shared styling
└── script.js         # redirects + query param wiring
```

---

### UX notes / improvement roadmap

If you’re reviewing this as an employer, here are a few concrete, high-impact next steps I would tackle to bring it closer to production-quality:

- **Accessibility**: add proper `<label>` elements (or `aria-label`) for inputs; ensure keyboard-first submission works naturally.
- **HTML semantics**: avoid nesting `<button>` inside `<a>`; use either a styled link or a button with navigation, not both.
- **URL safety**: encode user input with `encodeURIComponent()` to handle spaces and special characters robustly.
- **Responsive layout**: replace absolute positioning with a flex/grid layout to scale cleanly across screen sizes.

---

### Tech stack

- **HTML5**
- **CSS3**
- **JavaScript (vanilla)**

---

### Screenshots (optional)

Add screenshots to a `screenshots/` folder and link them here:

- `screenshots/home.png`
- `screenshots/image.png`
- `screenshots/advanced.png`

---

### Author

Built by **Islambek Karagulov** as part of **CS50’s Web Programming with Python and JavaScript (Project 0)**.

