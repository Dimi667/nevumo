import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const svgPath = path.join(__dirname, '../public/nevumo_favicon.svg');
const output32 = path.join(__dirname, '../public/favicon-32x32.png');
const output16 = path.join(__dirname, '../public/favicon-16x16.png');

async function generateFavicons() {
  try {
    // Generate 32x32 PNG
    await sharp(svgPath)
      .resize(32, 32)
      .png()
      .toFile(output32);
    console.log('Generated favicon-32x32.png');

    // Generate 16x16 PNG
    await sharp(svgPath)
      .resize(16, 16)
      .png()
      .toFile(output16);
    console.log('Generated favicon-16x16.png');

    // Check file sizes
    const size32 = fs.statSync(output32).size;
    const size16 = fs.statSync(output16).size;
    console.log(`favicon-32x32.png: ${size32} bytes`);
    console.log(`favicon-16x16.png: ${size16} bytes`);
  } catch (error) {
    console.error('Error generating favicons:', error);
    process.exit(1);
  }
}

generateFavicons();
