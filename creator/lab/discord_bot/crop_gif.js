import sharp from 'sharp';

async function cropGif() {
  const metadata = await sharp('stampede.gif', { animated: true }).metadata();
  console.log('Dimensiones originales:', metadata.width, 'x', metadata.height, 'Páginas:', metadata.pages);

  const originalHeight = metadata.pageHeight || metadata.height;
  const cutTop = Math.floor(originalHeight / 3);
  const newHeight = originalHeight - cutTop;

  console.log(`Recortando 1/3 superior (${cutTop}px). Nueva altura: ${newHeight}px`);

  await sharp('stampede.gif', { animated: true })
    .extract({
      left: 0,
      top: cutTop,
      width: metadata.width,
      height: newHeight
    })
    .gif()
    .toFile('stampede_cropped.gif');

  console.log('GIF recortado con éxito -> stampede_cropped.gif');
}

cropGif().catch(console.error);
