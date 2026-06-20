/* Compile the portfolio's JSX sources to plain React.createElement JS.
   Usage: node tools/build.js   (run after editing any js/*.jsx file) */
const fs = require("fs");
const path = require("path");
const babel = require("@babel/core");

const jsDir = path.join(__dirname, "..", "js");
const entries = ["app", "sections"];

for (const name of entries) {
  const src = path.join(jsDir, name + ".jsx");
  if (!fs.existsSync(src)) continue;
  const { code } = babel.transformSync(fs.readFileSync(src, "utf8"), {
    presets: [["@babel/preset-react", { runtime: "classic", pure: true }]],
    compact: false,
    comments: true,
  });
  const banner =
    `/* COMPILED from js/${name}.jsx. Do not edit directly; edit the .jsx and recompile. */\n`;
  fs.writeFileSync(path.join(jsDir, name + ".js"), banner + code + "\n");
  console.log("compiled js/" + name + ".jsx -> js/" + name + ".js");
}
