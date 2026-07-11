/* Render one social-share card (1200x630 PNG) per project into assets/og/,
   from tools/og-template.html and the data in js/data.js.

   This is a manual step, separate from `npm run build`, because it needs a
   Chromium binary: run `node tools/build-og.js` after adding or renaming a
   project, then commit the PNGs. Set OG_CHROME to your Chrome/Chromium path
   if it is not found automatically. tools/build-pages.js picks the card up
   automatically once assets/og/<id>.png exists. */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

let chromium;
try {
  chromium = require("playwright-core").chromium;
} catch (e) {
  console.error("playwright-core is not installed. Run `npm install` first.");
  process.exit(1);
}

const ROOT = path.join(__dirname, "..");

function findChrome() {
  const candidates = [process.env.OG_CHROME].concat(
    fs.existsSync("/opt/pw-browsers")
      ? fs.readdirSync("/opt/pw-browsers")
          .filter((d) => d.startsWith("chromium-"))
          .map((d) => path.join("/opt/pw-browsers", d, "chrome-linux", "chrome"))
      : [],
    [
      "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
  ).filter(Boolean);
  for (const c of candidates) if (fs.existsSync(c)) return c;
  throw new Error("No Chrome/Chromium found. Set OG_CHROME to your browser binary.");
}

const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(ROOT, "js", "data.js"), "utf8"), sandbox);
const P = sandbox.window.PORTFOLIO;

(async () => {
  const outDir = path.join(ROOT, "assets", "og");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: findChrome(), args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto("file://" + path.join(__dirname, "og-template.html"));

  for (let i = 0; i < P.projects.length; i++) {
    const p = P.projects[i];
    await page.evaluate(([p, i, profile]) => {
      const num = String(i + 1).padStart(2, "0");
      const set = (id, txt) => { document.getElementById(id).textContent = txt; };
      set("name", profile.name);
      set("eyebrow", "Project " + num + " · " + p.year);
      set("num", num);
      const title = document.getElementById("title");
      title.textContent = p.title;
      title.classList.toggle("small", p.title.length > 40);
      set("v", p.result.value);
      set("u", p.result.unit || "");
      set("l", p.result.label);
    }, [p, i, P.profile]);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(outDir, p.id + ".png") });
    console.log("assets/og/" + p.id + ".png");
  }
  await browser.close();
  console.log("rendered " + P.projects.length + " og cards");
})().catch((e) => { console.error(e); process.exit(1); });
