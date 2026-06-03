import { writeFile } from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import sharp from 'sharp';

/* eslint-disable no-undef */

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const publicDir = join(__dirname, '../public');

async function generateStaticIcons() {
  console.log('Generating static icons from production PWA routes...');

  // Download 192x192 PWA icon and resize to 32px for favicon
  const icon192Res = await fetch('https://www.nevumo.com/icons/icon-192x192.png');
  const icon192Buffer = await icon192Res.arrayBuffer();
  const faviconBuffer = await sharp(Buffer.from(icon192Buffer))
    .resize(32, 32, { fit: 'cover' })
    .png()
    .toBuffer();
  await writeFile(join(publicDir, 'favicon.ico'), faviconBuffer);
  console.log('✓ Generated public/favicon.ico (32px)');

  // Download 512x512 PWA icon and resize to 180px for apple-touch-icon
  const icon512Res = await fetch('https://www.nevumo.com/icons/icon-512x512.png');
  const icon512Buffer = await icon512Res.arrayBuffer();
  const appleIconBuffer = await sharp(Buffer.from(icon512Buffer))
    .resize(180, 180, { fit: 'cover' })
    .png()
    .toBuffer();
  await writeFile(join(publicDir, 'apple-touch-icon.png'), appleIconBuffer);
  console.log('✓ Generated public/apple-touch-icon.png (180px)');

  console.log('Done!');
}

generateStaticIcons().catch(console.error);
