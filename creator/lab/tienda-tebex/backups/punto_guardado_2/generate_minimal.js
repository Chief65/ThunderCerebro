const fs = require('fs');

// Generamos textura estilo Bedrock / Slate Minimalista de 32x32 píxeles, homogénea, ultra sutil
const svgBedrockMinimal = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 16 16" shape-rendering="crispEdges">
  <rect width="16" height="16" fill="#090d16"/>
  <!-- Micro textura casi imperceptible tipo bedrock oscuro -->
  <rect x="1" y="1" width="1" height="1" fill="#0c111c"/>
  <rect x="5" y="0" width="1" height="1" fill="#0b0f19"/>
  <rect x="10" y="2" width="1" height="1" fill="#0c111c"/>
  <rect x="14" y="1" width="1" height="1" fill="#0b0f19"/>
  <rect x="3" y="4" width="1" height="1" fill="#0b0f19"/>
  <rect x="8" y="5" width="1" height="1" fill="#0c111c"/>
  <rect x="12" y="4" width="1" height="1" fill="#0b0f19"/>
  <rect x="0" y="7" width="1" height="1" fill="#0c111c"/>
  <rect x="6" y="8" width="1" height="1" fill="#0b0f19"/>
  <rect x="15" y="7" width="1" height="1" fill="#0c111c"/>
  <rect x="2" y="10" width="1" height="1" fill="#0b0f19"/>
  <rect x="9" y="11" width="1" height="1" fill="#0c111c"/>
  <rect x="13" y="10" width="1" height="1" fill="#0b0f19"/>
  <rect x="4" y="13" width="1" height="1" fill="#0c111c"/>
  <rect x="7" y="14" width="1" height="1" fill="#0b0f19"/>
  <rect x="11" y="14" width="1" height="1" fill="#0c111c"/>
</svg>`;

fs.writeFileSync('C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/tienda-tebex/Assets/mc_bedrock_minimal.svg', svgBedrockMinimal, 'utf8');
console.log('Textura Bedrock Minimal generada');
