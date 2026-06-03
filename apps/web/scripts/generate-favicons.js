import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import toIco from 'to-ico';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const svgPath = path.join(__dirname, '../public/nevumo_favicon.svg');
const output32 = path.join(__dirname, '../public/favicon-32x32.png');
const output16 = path.join(__dirname, '../public/favicon-16x16.png');
const outputApple = path.join(__dirname, '../public/apple-touch-icon.png');
const outputApplePre = path.join(__dirname, '../public/apple-touch-icon-precomposed.png');
const outputApple76 = path.join(__dirname, '../public/apple-touch-icon-76x76.png');
const outputApple120 = path.join(__dirname, '../public/apple-touch-icon-120x120.png');
const outputApple152 = path.join(__dirname, '../public/apple-touch-icon-152x152.png');
const outputIco = path.join(__dirname, '../public/favicon.ico');

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

    // Generate 180x180 apple-touch-icon.png
    await sharp(svgPath)
      .resize(180, 180)
      .png()
      .toFile(outputApple);
    console.log('Generated apple-touch-icon.png');

    // Generate 180x180 apple-touch-icon-precomposed.png (same as above)
    await sharp(svgPath)
      .resize(180, 180)
      .png()
      .toFile(outputApplePre);
    console.log('Generated apple-touch-icon-precomposed.png');

    // Generate 76x76 apple-touch-icon
    await sharp(svgPath)
      .resize(76, 76)
      .png()
      .toFile(outputApple76);
    console.log('Generated apple-touch-icon-76x76.png');

    // Generate 120x120 apple-touch-icon
    await sharp(svgPath)
      .resize(120, 120)
      .png()
      .toFile(outputApple120);
    console.log('Generated apple-touch-icon-120x120.png');

    // Generate 152x152 apple-touch-icon
    await sharp(svgPath)
      .resize(152, 152)
      .png()
      .toFile(outputApple152);
    console.log('Generated apple-touch-icon-152x152.png');

    // Generate favicon.ico using to-ico (embed 16x16 and 32x32)
    const buffer16 = fs.readFileSync(output16);
    const buffer32 = fs.readFileSync(output32);
    const icoBuffer = await toIco([buffer16, buffer32]);
    fs.writeFileSync(outputIco, icoBuffer);
    console.log('Generated favicon.ico');

    // Check file sizes
    const size32 = fs.statSync(output32).size;
    const size16 = fs.statSync(output16).size;
    const sizeApple = fs.statSync(outputApple).size;
    const sizeApplePre = fs.statSync(outputApplePre).size;
    const sizeApple76 = fs.statSync(outputApple76).size;
    const sizeApple120 = fs.statSync(outputApple120).size;
    const sizeApple152 = fs.statSync(outputApple152).size;
    const sizeIco = fs.statSync(outputIco).size;
    console.log(`favicon-32x32.png: ${size32} bytes`);
    console.log(`favicon-16x16.png: ${size16} bytes`);
    console.log(`apple-touch-icon.png: ${sizeApple} bytes`);
    console.log(`apple-touch-icon-precomposed.png: ${sizeApplePre} bytes`);
    console.log(`apple-touch-icon-76x76.png: ${sizeApple76} bytes`);
    console.log(`apple-touch-icon-120x120.png: ${sizeApple120} bytes`);
    console.log(`apple-touch-icon-152x152.png: ${sizeApple152} bytes`);
    console.log(`favicon.ico: ${sizeIco} bytes`);

    if (sizeIco < 3000) {
      console.warn(`WARNING: favicon.ico is only ${sizeIco} bytes (expected > 3000 bytes)`);
    }
  } catch (error) {
    console.error('Error generating favicons:', error);
    process.exit(1);
  }
}

generateFavicons();
