# Standard procedure

How this portfolio is built and kept up to date, start to finish. It is written
so the same steps can be repeated for the next project without re-deciding
anything. If you only read one thing, read the checklist at the bottom.

The house rules that never change:

- **No em dashes, anywhere.** Not in copy, code, comments, data, or notes. Use
  a comma, a colon, or a full stop. Ranges use an en dash (1985 to 2024 is
  written `1985–2024`). Check before every commit (see step 6).
- **Every number traces back to open data and tested code.** Nothing on the
  site is hand-typed from memory; it comes from a committed dataset produced by
  a reproducible pipeline whose statistics are unit-tested and run in CI.
- **Honesty over a big headline.** If the data cannot settle a question, the
  write-up says so. That judgement is the portfolio's main selling point.

## The shape of a project

Each project is a self-contained folder (`cyclone-risk/`, `sea-level/`, and so
on) with the same skeleton:

```
<project>/
  README.md          plain-English write-up, results, method, limitations, update log
  build_dataset.py   reads raw drops, writes clean CSVs + data/source-library.csv
  analysis.py        computes the statistics, writes summary CSVs
  viz.py             draws the charts into charts/
  stats_utils.py     shared, hand-written statistics (BYTE-IDENTICAL across projects)
  test_stats.py      validates stats_utils against known values
  test_project.py    tests the project-specific pipeline
  data/              committed CLEAN datasets only (never raw drops)
  charts/            committed PNG charts
```

`stats_utils.py` must be byte-identical in every project. CI diffs them all
against `rainfall-decline/stats_utils.py` and fails on any difference.

## Where raw data lives

Raw source files are **staged, never committed**. They go into
`dropzone/<project>/`, which `dropzone/.gitignore` ignores wholesale (only the
folder, its `.gitkeep`, and `DROP_FILES_HERE.md` are tracked). `build_dataset.py`
reads from there by content, so filenames do not matter. Once a project is
complete, its cleaned outputs in `<project>/data/` are the record;
`DROP_FILES_HERE.md` documents how to re-download the raw inputs to re-run from
scratch. If raw drops ever end up tracked (a web upload can bypass the ignore
rule), remove them with `git rm`: the repo should match its own `.gitignore`.

## The site (front page + per-project pages)

`index.html` boots a small React app (loaded from a CDN) that reads plain data
objects. The front page is a light landing page: the hero, the stat band, the
project index cards, and the contact card. Each project's full story lives on
its own generated page at `projects/<id>.html`, with its own title, meta
description and social tags, so a single project can be shared by URL. The
moving parts:

- `js/data.js` (`window.PORTFOLIO`): the profile, the stat band, and the
  ordered list of project stories. **This is the file you edit to add or change
  a project.**
- `js/chartdata.js` (`window.CHARTDATA`): one minified JSON object of the
  numbers behind every interactive chart, keyed by `vizKey`. It is generated,
  so edit it with a script, not by hand (see below).
- `js/sections.jsx` and `js/app.jsx`: the components. **Edit the `.jsx`, never
  the `.js`.** Compile with `npm run build` (runs `tools/build.js` then
  `tools/build-pages.js`), which regenerates `js/sections.js`, `js/app.js`,
  every `projects/<id>.html`, and `sitemap.xml`.
- `projects/<id>.html`: one generated page per story. **Never edit these by
  hand**; they are written by `tools/build-pages.js` from `js/data.js`. Each
  page sets `window.PROJECT_ID` and loads only the data files that story needs
  (`mapdata.js`, `scrollydata.js`, `aasbdata.js` are skipped where unused).
- `portfolio.css` / `styles.css` / `tokens/`: the styling.

### Adding a completed project to the site

1. **Add the story object** to the `projects` array in `js/data.js`, in
   narrative order (physical-risk stories first, the disclosure review last).
   Copy the shape of an existing entry. The fields that matter:
   `id`, `title`, `year`, `status`, `icon` (must exist in `js/icons.js`),
   `summary`, `result` (the index-card stat), `headline`, `body`, `findings`
   (the stat blocks), `meaning` (the "why it matters"), `resources` (links back
   to the README, data, and charts), `dataset` (the sortable table), `vizKey`,
   `viz` (the chart list), `tags`, and `updates` (the timeline, see below).
2. **Add its chart data** under a new `vizKey` in `js/chartdata.js`. Compute it
   from the project's committed CSVs with a small script rather than by hand,
   for example: parse the JSON out of the single line, add the key, write it
   back minified. Chart shapes: a line chart takes
   `{points:[[x,y],...], trend:[x0,y0,x1,y1], ylabel, unit}`; a bar chart takes
   `{bars:[{label,value}], ylabel, unit}`; grouped bars add `keys`.
3. **Update the surrounding copy** if the count changed: the stat band and
   `intro` in `js/data.js`, the project-count sentence in the stories intro in
   `js/sections.jsx`, and the `description` / `og` / `twitter` meta in
   `index.html` (per-project meta is generated for you).
4. **Recompile and regenerate:** `npm run build`. This also writes the new
   `projects/<id>.html` page and refreshes `sitemap.xml`; commit them.
5. **Verify it renders** (see step 5 below).

## The update log (how a project evolved)

Every project carries a short, chronological history at the foot of its story
and at the foot of its README, so a reader can see what we found after
publishing and why each finding earned an update.

- **On the site:** an `updates` array on the project in `js/data.js`. Each entry
  is `{ date, title, found, change }`, oldest first. `found` says what we
  learned; `change` says what we did about it. The component renders them as a
  dated timeline under "How this project evolved".
- **In the README:** an `## Update log` section at the end, same entries in the
  same order, one paragraph each: `**<date> · <title>.** <what we found>
  <what we changed>`.

Only record real history. A brand-new project can have a single "First
published" entry.

## The private study page

`study.html` holds interview-prep notes, encrypted in the browser. The notes are
AES-256-GCM encrypted with a key derived from a password by PBKDF2 (SHA-256,
310k iterations), so nothing readable ships in the repo, and the page is not
linked from the site.

To update the notes:

1. Edit the plaintext notes fragment (an HTML fragment using the study page's
   own classes: `.s-card`, `.s-say`, `.s-chips`, `.s-qa`, and so on). **Keep
   this file out of the repo**; encrypting it is the whole point.
2. Re-encrypt into the page:

   ```bash
   STUDY_PASSWORD='your-password' node tools/build-study.js path/to/notes.html
   ```

   The generator rewrites the `SALT` / `IV` / `DATA` constants in `study.html`
   in place. It refuses to run on notes containing an em dash. The password is
   read from the environment and never written to disk.
3. Verify by opening `study.html` and entering the password.

## Verifying before you commit

1. **Build:** `npm run build` compiles cleanly and regenerates the `.js`.
2. **Data wiring:** load `js/data.js` and `js/chartdata.js` in Node and assert
   every project's `viz` keys resolve in `CHARTDATA`, and the project count and
   stats are right.
3. **Render:** the site pulls React from a CDN, so to render it offline, point
   the two script tags at local `react`/`react-dom` UMD builds, serve the folder
   over HTTP (not `file://`, which trips CORS on the crossorigin scripts), and
   load it with headless Chromium. Confirm the index cards link to the right
   pages, the new project's own page renders its charts, table and update
   timeline with no console errors, and its prev/next links point at its
   neighbours.
4. **Python side:** run each project's `test_stats.py` and `test_project.py`,
   and check `stats_utils.py` is byte-identical across projects. This is what CI
   (`.github/workflows/tests.yml`) enforces on every push and pull request.
5. **Em dashes:** confirm there are none, in every form:

   ```bash
   git grep -lP "\xe2\x80\x94"           # literal em dash
   git grep -lE 'mdash|&#8212|\\u2014'   # entity / escaped forms
   ```

## Git and pull requests

- Work on a feature branch, never straight on `main`.
- Commit messages: a short imperative subject, then a body explaining what and
  why. Keep secrets and passwords out of commits, PR bodies, and code comments.
- Open a draft pull request once the branch is pushed.

## The checklist

- [ ] Raw data staged in `dropzone/<project>/`, not committed.
- [ ] Clean CSVs and charts committed under `<project>/`.
- [ ] `stats_utils.py` byte-identical; tests pass locally.
- [ ] Story object added to `js/data.js`; chart data added to `js/chartdata.js`.
- [ ] Stat band, intro, stories-intro count, and `index.html` meta updated.
- [ ] `projects/<id>.html` generated and committed; `sitemap.xml` refreshed.
- [ ] `updates` timeline on the site and an `## Update log` in the README.
- [ ] `npm run build` run; `.jsx` edited, not `.js`.
- [ ] Site rendered headlessly with no errors; all charts and tables present.
- [ ] Study page re-encrypted if the notes changed.
- [ ] Zero em dashes, checked in every form.
- [ ] Draft pull request opened.
