const fs = require('fs');
const path = require('path');

// Прост PNG генератор - създава оранжев квадрат с буква "N"
function generateSimplePNG(size, outputPath) {
  // PNG signature
  const signature = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);

  // IHDR chunk
  const width = size;
  const height = size;
  const bitDepth = 8;
  const colorType = 2; // RGB
  const ihdrData = Buffer.alloc(13);
  ihdrData.writeUInt32BE(width, 0);
  ihdrData.writeUInt32BE(height, 4);
  ihdrData.writeUInt8(bitDepth, 8);
  ihdrData.writeUInt8(colorType, 9);
  ihdrData.writeUInt8(0, 10); // compression
  ihdrData.writeUInt8(0, 11); // filter
  ihdrData.writeUInt8(0, 12); // interlace

  const ihdrChunk = createChunk('IHDR', ihdrData);

  // IDAT chunk - създаваме пикселни данни
  // Оранжев цвят: #f97316 = RGB(249, 115, 22)
  const orangeR = 249;
  const orangeG = 115;
  const orangeB = 22;

  // Бял цвят за текста
  const whiteR = 255;
  const whiteG = 255;
  const whiteB = 255;

  // Създаваме растерни данни (всеки ред започва с filter byte 0)
  const rowLength = 1 + width * 3; // filter byte + RGB за всеки пиксел
  const imageData = Buffer.alloc(height * rowLength);

  // Попълваме с оранжев цвят
  for (let y = 0; y < height; y++) {
    const rowOffset = y * rowLength;
    imageData[rowOffset] = 0; // filter byte
    for (let x = 0; x < width; x++) {
      const pixelOffset = rowOffset + 1 + x * 3;
      imageData[pixelOffset] = orangeR;
      imageData[pixelOffset + 1] = orangeG;
      imageData[pixelOffset + 2] = orangeB;
    }
  }

  // Добавяме буква "N" в центъра (проста реализация)
  const textSize = Math.floor(size * 0.5);
  const centerX = Math.floor((width - textSize) / 2);
  const centerY = Math.floor((height - Math.floor(textSize * 1.2)) / 2);

  // Рисуваме проста "N" - три линии
  const lineWidth = Math.max(2, Math.floor(size / 20));
  
  // Лява вертикална линия
  for (let y = centerY; y < centerY + textSize; y++) {
    for (let x = centerX; x < centerX + lineWidth; x++) {
      if (y >= 0 && y < height && x >= 0 && x < width) {
        const pixelOffset = y * rowLength + 1 + x * 3;
        imageData[pixelOffset] = whiteR;
        imageData[pixelOffset + 1] = whiteG;
        imageData[pixelOffset + 2] = whiteB;
      }
    }
  }

  // Дясна вертикална линия
  for (let y = centerY; y < centerY + textSize; y++) {
    for (let x = centerX + textSize - lineWidth; x < centerX + textSize; x++) {
      if (y >= 0 && y < height && x >= 0 && x < width) {
        const pixelOffset = y * rowLength + 1 + x * 3;
        imageData[pixelOffset] = whiteR;
        imageData[pixelOffset + 1] = whiteG;
        imageData[pixelOffset + 2] = whiteB;
      }
    }
  }

  // Диагонална линия (проста)
  for (let i = 0; i < textSize; i++) {
    const y = centerY + i;
    const xStart = centerX + Math.floor((i / textSize) * (textSize - lineWidth));
    for (let x = xStart; x < xStart + lineWidth; x++) {
      if (y >= 0 && y < height && x >= 0 && x < width) {
        const pixelOffset = y * rowLength + 1 + x * 3;
        imageData[pixelOffset] = whiteR;
        imageData[pixelOffset + 1] = whiteG;
        imageData[pixelOffset + 2] = whiteB;
      }
    }
  }

  // Компресираме данните
  const zlib = require('zlib');
  const compressed = zlib.deflateSync(imageData);
  const idatChunk = createChunk('IDAT', compressed);

  // IEND chunk
  const iendChunk = createChunk('IEND', Buffer.alloc(0));

  // Сглобяваме PNG файла
  const pngBuffer = Buffer.concat([signature, ihdrChunk, idatChunk, iendChunk]);
  fs.writeFileSync(outputPath, pngBuffer);
}

function createChunk(type, data) {
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);
  
  const typeBuffer = Buffer.from(type, 'ascii');
  
  const crcBuffer = Buffer.alloc(4);
  const crcData = Buffer.concat([typeBuffer, data]);
  crcBuffer.writeUInt32BE(crc32(crcData), 0);
  
  return Buffer.concat([length, typeBuffer, data, crcBuffer]);
}

// Проста CRC32 реализация
function crc32(buffer) {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let j = 0; j < 8; j++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[i] = c >>> 0;
  }

  let crc = 0xFFFFFFFF;
  for (let i = 0; i < buffer.length; i++) {
    crc = table[(crc ^ buffer[i]) & 0xFF] ^ (crc >>> 8);
  }
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

// Генерираме иконите
const iconsDir = path.join(__dirname, '..', 'public', 'icons');

console.log('Generating 192x192 icon...');
generateSimplePNG(192, path.join(iconsDir, 'icon-192x192.png'));

console.log('Generating 512x512 icon...');
generateSimplePNG(512, path.join(iconsDir, 'icon-512x512.png'));

console.log('Icons generated successfully!');
