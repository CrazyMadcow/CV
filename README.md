# Kwangwoo Jang — Academic GitHub Pages

A lightweight academic portfolio for aerospace guidance, control, autonomous flight, and UAM research.

## 1. Fastest deployment

### Option A — Personal GitHub Pages domain

1. Create a GitHub repository named exactly:
   `<YOUR_GITHUB_USERNAME>.github.io`
2. Upload every file in this folder to the repository root.
3. Commit to the `main` branch.
4. Go to:
   `Settings → Pages`
5. Under **Build and deployment**, choose:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
6. Save.
7. After a few minutes, open:
   `https://<YOUR_GITHUB_USERNAME>.github.io`

No Jekyll or build environment is required.

---

## 2. Replace the placeholders

### Profile photo

Replace:

`assets/img/profile.svg`

with your own image, for example:

`assets/img/profile.jpg`

and change this line in `index.html`:

```html
<img class="avatar" src="assets/img/profile.jpg" ... />
```

Recommended:
- square crop
- neutral background
- 800×800 px or larger

### Project images

Replace these placeholder files:

- `assets/img/hoverbike.svg`
- `assets/img/tiltrotor.svg`
- `assets/img/collision.svg`
- `assets/img/mppi.svg`

with public-cleared project images.

**Important for ADD / defense-related work:** publish only photographs, figures, performance numbers, and videos that are already cleared for public release.

---

## 3. Add the final CV

Put your final CV here:

`files/Kwangwoo_Jang_CV.pdf`

The CV button already points to that path.

Optionally add:

`files/Kwangwoo_Jang_Research_Statement.pdf`

and then add a Research Statement button near the CV button.

---

## 4. Update these fields before publishing

Search `index.html` for:

- `CrazyMadCow` — verify GitHub username
- `kwjang@etri.re.kr` — verify preferred public email
- `Air Mobility Research Division` — verify official current unit name
- publication author lists / metadata
- project wording
- current employment start date if you want to show it

---

## 5. Recommended long-term structure

Keep the homepage concise. Use it as:
- research identity
- 3–4 flagship projects
- selected publications
- experience / education
- links to Scholar / CV / GitHub

Avoid putting every conference and every minor project on the homepage.
Google Scholar and the PDF CV can hold the complete lists.

---

## 6. Custom domain (optional)

Later you can connect a domain such as:

`kwangwoojang.com`

from GitHub Pages settings.

---

## 7. Local preview

From this folder:

```bash
python -m http.server 8000
```

Then open:

`http://localhost:8000`
