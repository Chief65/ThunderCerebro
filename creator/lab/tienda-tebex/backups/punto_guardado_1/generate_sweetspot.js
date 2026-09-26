const fs = require('fs');

// Textura Bedrock en punto medio exacto (subtle pero perceptible, tonos #0d121f a #101726 sobre #090d16)
const svgBedrockSweetspot = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 16 16" shape-rendering="crispEdges">
  <rect width="16" height="16" fill="#090d16"/>
  <!-- Micro variaciones tonales en punto medio de opacidad -->
  <rect x="0" y="0" width="2" height="1" fill="#0e1321"/>
  <rect x="5" y="0" width="1" height="1" fill="#101726"/>
  <rect x="10" y="1" width="2" height="1" fill="#0c111c"/>
  <rect x="14" y="0" width="2" height="1" fill="#0f1523"/>
  
  <rect x="2" y="2" width="2" height="1" fill="#0f1422"/>
  <rect x="7" y="3" width="2" height="1" fill="#0c111c"/>
  <rect x="12" y="2" width="1" height="1" fill="#101726"/>

  <rect x="0" y="5" width="1" height="1" fill="#101726"/>
  <rect x="4" y="4" width="2" height="1" fill="#0d121f"/>
  <rect x="9" y="5" width="2" height="1" fill="#0f1422"/>
  <rect x="13" y="4" width="2" height="1" fill="#0c111c"/>

  <rect x="1" y="7" width="2" height="1" fill="#0c111c"/>
  <rect x="6" y="7" width="2" height="1" fill="#101726"/>
  <rect x="11" y="6" width="2" height="1" fill="#0e1321"/>
  <rect x="15" y="7" width="1" height="1" fill="#0f1422"/>

  <rect x="3" y="9" width="2" height="1" fill="#0f1523"/>
  <rect x="8" y="10" width="1" height="1" fill="#101726"/>
  <rect x="12" y="9" width="2" height="1" fill="#0c111c"/>

  <rect x="0" y="11" width="2" height="1" fill="#0f1422"/>
  <rect x="5" y="12" width="2" height="1" fill="#0d121f"/>
  <rect x="10" y="11" width="2" height="1" fill="#101726"/>
  <rect x="14" y="12" width="2" height="1" fill="#0e1321"/>

  <rect x="2" y="14" width="2" height="1" fill="#0c111c"/>
  <rect x="7" y="14" width="2" height="1" fill="#0f1422"/>
  <rect x="11" y="15" width="2" height="1" fill="#0d121f"/>
  <rect x="15" y="14" width="1" height="1" fill="#101726"/>
</svg>`;

fs.writeFileSync('C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/tienda-tebex/Assets/mc_bedrock_minimal.svg', svgBedrockSweetspot, 'utf8');
console.log('Textura ajustada al punto medio óptimo');
