/* Encrypt the private study notes into study.html.

   The study page decrypts its notes in the browser with Web Crypto:
   PBKDF2 (SHA-256, 310k iterations) derives an AES-256-GCM key from the
   password, and the notes are stored as base64 SALT / IV / DATA constants.
   This script is the other half: it takes a plaintext notes fragment and a
   password and rewrites those three constants in place. The notes source and
   the password are NEVER committed; only the encrypted study.html is.

   Usage:
     STUDY_PASSWORD='your-password' node tools/build-study.js path/to/notes.html

   The notes file is an HTML fragment using the study page's own classes
   (.s-card, .s-say, .s-chips, and so on); it is injected into the room. */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ITER = 310000;
const notesPath = process.argv[2];
const htmlPath = process.argv[3] || path.join(__dirname, "..", "study.html");
const password = process.env.STUDY_PASSWORD;

if (!notesPath) {
  console.error("usage: STUDY_PASSWORD='...' node tools/build-study.js <notes.html> [study.html]");
  process.exit(1);
}
if (!password) {
  console.error("error: set the STUDY_PASSWORD environment variable (it is never written to disk).");
  process.exit(1);
}

const notes = fs.readFileSync(notesPath, "utf8");
if (notes.indexOf("—") !== -1) {
  console.error("error: the notes contain an em dash. This portfolio uses none; fix it before encrypting.");
  process.exit(1);
}

const salt = crypto.randomBytes(16);
const iv = crypto.randomBytes(12);
const key = crypto.pbkdf2Sync(password, salt, ITER, 32, "sha256");

const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
const ct = Buffer.concat([cipher.update(notes, "utf8"), cipher.final()]);
const tag = cipher.getAuthTag(); // Web Crypto expects ciphertext||tag
const data = Buffer.concat([ct, tag]);

const consts =
  'var SALT = "' + salt.toString("base64") + '", IV = "' + iv.toString("base64") +
  '", DATA = "' + data.toString("base64") + '", ITER = ' + ITER + ";";

let html = fs.readFileSync(htmlPath, "utf8");
const re = /var SALT = "[^"]*", IV = "[^"]*", DATA = "[^"]*", ITER = \d+;/;
if (!re.test(html)) {
  console.error("error: could not find the SALT/IV/DATA/ITER line in " + htmlPath);
  process.exit(1);
}
html = html.replace(re, consts);
fs.writeFileSync(htmlPath, html);

console.log("Encrypted " + notes.length + " chars of notes into " + path.relative(process.cwd(), htmlPath) + ".");
console.log("Verify by opening the page and entering the password.");
