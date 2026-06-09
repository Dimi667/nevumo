import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const swPath = path.join(__dirname, '../public/sw.js');
const workerPath = path.join(__dirname, '../worker/index.js');

if (!fs.existsSync(swPath)) {
  console.warn('[append-sw] WARNING: sw.js not found at:', swPath, '— skipping');
  process.exit(0);
}

if (!fs.existsSync(workerPath)) {
  console.error('[append-sw] ERROR: worker/index.js not found at:', workerPath);
  process.exit(1);
}

const MARKER = '// [NEVUMO-CUSTOM-SW]';
let sw = fs.readFileSync(swPath, 'utf8');
const customHandlers = fs.readFileSync(workerPath, 'utf8');

// Remove previously appended handlers (idempotent)
if (sw.includes(MARKER)) {
  sw = sw.substring(0, sw.indexOf(MARKER));
}

fs.writeFileSync(swPath, sw + '\n\n' + MARKER + '\n' + customHandlers);
console.log('[append-sw] Successfully appended push handlers to sw.js');
