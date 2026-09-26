import sharp from 'sharp';

async function cropGifBottom() {
  const metadata = await sharp('stampede_cropped.gif', { animated: true }).metadata();
  const currentHeight = metadata.pageHeight || metadata.height;
  const cutBottom = Math.floor(currentHeight * 0.20); // 2/10 = 20%
  const finalHeight = currentHeight - cutBottom;

  console.log(`Altura actual: ${currentHeight}px. Recortando 2/10 de abajo (${cutBottom}px). Nueva altura final: ${finalHeight}px`);

  await sharp('stampede_cropped.gif', { animated: true })
    .extract({
      left: 0,
      top: 0,
      width: metadata.width,
      height: finalHeight
    })
    .gif()
    .toFile('stampede_final.gif');

  console.log('GIF recortado con éxito -> stampede_final.gif');
}

cropGifBottom().catch(console.error);
