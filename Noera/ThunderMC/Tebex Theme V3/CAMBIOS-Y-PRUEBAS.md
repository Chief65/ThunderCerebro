# Tebex Theme V3 — revisión y correcciones

Fecha: 15 de octubre de 2026. Este ZIP mantiene las páginas y el diseño de la V3. No se ha publicado ni se ha ejecutado una transacción real.

## Cambios funcionales

- Un único controlador de producto/carrito reemplaza los listeners duplicados. Impide dobles altas y cancela respuestas de producto obsoletas.
- El drawer obtiene cantidades, moneda e importes de HTML renderizado por el servidor. Se elimina el cálculo de totales desde precios de texto y la suma optimista de badges.
- Cambiar cantidad utiliza un único POST nativo /checkout/update con todos los campos. Disminuir cantidad NO llama a eliminar el producto. La recarga confirma a la vez cantidades, precio e ident de pago.
- Un error HTTP, rechazo de Tebex o ausencia de estado confirmado no se presenta como una compra añadida ni provoca un reintento automático de una operación incierta.
- Las opciones/precios personalizados continúan por el formulario nativo de Tebex. La compra única y la suscripción tienen enlaces diferentes. Los paquetes no comprables para la cuenta quedan bloqueados y los invitados pueden abrir login.
- Login Java/Bedrock utiliza POST nativo; se eliminan las recargas de falso éxito del fetch. Prefijo Bedrock tomado de config(bedrockPrefix), no un punto fijo. Selección de plataforma, preview y teclado siguen disponibles.
- Pago deshabilitado hasta aceptar las dos casillas, con enlaces a las condiciones y privacidad oficiales. Carrito vacío/sin ident presenta un estado explícito. No hay enlace circular de pago hacia la misma cesta.
- Se evita inventar impuestos incluidos, precios o nombres de usuario. Las tarjetas manuales de portada conservan sus IDs y muestran “Ver precio”: el importe confirmado se consulta en el detalle real.
- El regalo permanece desactivado como en V3 hasta verificar el flujo de destinatario del backend.

## Dependencias recuperadas

El ZIP recibido tenía 26 archivos y omitía las plantillas Twig y las imágenes que referencia. Se recuperaron 60 archivos de la exportación original disponible y se adaptaron login, cabecera, carrito y footer a estos controladores. No son versiones nuevas recuperadas del servidor: proceden de tu primer ZIP.

Las imágenes lite.png, star.png y mega.png no estaban en ninguno de los dos ZIP. Sus referencias usan el icono cat_rangos.webp existente como sustituto, sin inventar imágenes de marca.

cat_icon_bag.png y cat_sample_icon.png contenían datos WebP. Ahora son PNG reales con exactamente los mismos píxeles RGBA decodificados.

## Seguridad, accesibilidad y presentación

- Escape explícito de nombres e identidades, mensajes del servidor como texto y creación segura del popup de confirmación. Se conservan descripciones/CMS raw del administrador para no romper su HTML.
- Foco, cierre y control de teclado en login/drawer; carrito cerrado hidden/inert; enlaces reales de detalle si falla el JS; cierre sin esperar animationend.
- Botones de pausa y paginación accesibles, reducción de movimiento y parada de carrusel al ocultar la pestaña, enfocar o pasar el ratón.
- Header móvil ajustado y espaciador medido con ResizeObserver. Correcciones de contraste y anchuras flex/grid; sin desbordamiento en los tamaños probados.
- Rutas asset() de Tebex, canonical por página sin query, OG property correcto, H1 de tienda y noindex del checkout. Se retiran JSON-LD de buscador/producto/FAQ sin datos confirmados.
- Se eliminan temporizadores que se reiniciaban en cada carga, estadísticas de jugadores de muestra y fallback comercial de páginas CMS vacías.
- Mensajes de plataforma nativos y accesibles: no dependen de Toastify. Fuentes reducidas a las cuatro familias del tema. SimpleBar fijado a 6.3.3. Los controladores críticos no dependen de jQuery/Axios para inicializarse.
- Analytics opcional del tema solo carga tras consentimiento. Preferencias de privacidad permiten cambiar la elección. Esto no controla scripts inyectados directamente por la plataforma u otros proveedores.
- Footer oficial Tebex visible y enlaces legales oficiales preservados. Esto no certifica cumplimiento legal o del EULA.

## Referencia de desarrollo

preview_server.js era un simulador con paquetes, precios y sesión de prueba; eliminaba sintaxis Twig mediante regex y no validaba Tebex. Se conserva de forma inerte en Referencia-preview/preview_server.js.txt. No es un servidor de producción ni se utilizó como prueba de compatibilidad real.

## Validación realizada

- Compilación de 56 archivos de plantilla/script con Twig.js 3.0.0; casos de las cinco páginas principales, invitado, cesta vacía/grande, precio cero, suscripción, ambos tipos, opciones, precio personalizado y producto bloqueado. Twig.js no es el sandbox PHP real de Tebex.
- Sintaxis de los scripts ya renderizados comprobada con node --check, además de main.js, Swiper y privacy.js.
- Chromium 153: portada/catálogo visibles sin los CDNs de jQuery/Axios; texto con comillas/HTML escapado; doble clic genera una sola alta; cambio de cantidad produce un único POST; error de alta no muestra éxito; invitado abre login sin modal tapándolo; casillas impiden abrir el componente de pago simulado.
- Chromium: analítica no solicitada antes del consentimiento o al rechazar; carga al aceptar y flag de desactivación al retirar el consentimiento.
- Portada sin desbordamiento horizontal a 320, 390, 768, 1280 y 2560 px. Revisión visual de 390 y 1280 px.
- Sin includes obligatorios ni assets literales ausentes. Integridad CRC del ZIP y comparación de cada archivo empaquetado con el directorio final.
- Los endpoints de Tebex, el SDK de pago y servicios externos se simularon en estas pruebas. No son mediciones de Core Web Vitals reales ni pruebas en Firefox, Safari, iOS/Android físicos.

## Validar en Tebex antes de publicar

1. Confirmar que los IDs 1–11 del catálogo manual corresponden a los productos anunciados. Se conservaron los que traía V3; no se inventó un mapeo nuevo. Beneficios, bonus, vigencia y entrega deben coincidir con el panel/plugin.
2. Probar una compra permitida por tu entorno de pruebas: login Java/Bedrock, compra única, suscripción, opciones, cupón válido/inválido, cantidades permitidas, importe final e impuestos.
3. Confirmar la respuesta de /checkout/update y del alta, los datos basket.ident/package.type/disableQuantity en el contexto de la cuenta y los mensajes/headers retornados por Tebex.
4. Publicar contenido real en las páginas CMS. Las páginas vacías ahora lo indican; no se rellenan con políticas o testimonios ficticios. Verificar términos, reembolsos, datos/consentimiento, ventajas competitivas y moneda de acuerdo con las reglas aplicables.
5. Subir también las dependencias restauradas en Assets y conservar las opciones del panel que no están exportadas. Añadir las ilustraciones reales de LITE/STAR/MEGA si quieres sustituir el icono genérico.
6. Validar la versión real del motor/sandbox de Tebex y hacer una pasada móvil real. Algunas funciones o campos son condicionales a la cuenta; este ZIP no cambia las reglas del checkout alojado.

## Archivos de V3 modificados

- category.html
- checkout.html
- cmspage.html
- index.html
- layout.html
- package.html
- Assets/categorytiered.html
- Assets/function.checkout.js
- Assets/function.featuredProducts.js
- Assets/function.giftcard.js
- Assets/function.initModals.js
- Assets/function.loginModal.js
- Assets/function.productModal.js
- Assets/function.storeFunctions.js
- Assets/function.utils.js
- Assets/main.js
- Assets/quote.html
- Assets/style.css

## Archivos recuperados de la primera exportación

- Assets/favicon.png
- Assets/hero_keys.png
- Assets/mc_bedrock_minimal.svg
- Assets/ref1.png
- Assets/layout.categoryImageItems.twig
- Assets/layout.login_modal.twig
- Assets/cat_packs.webp
- Assets/stylePreferences.twig
- Assets/logo_tienda_ref1_badge.jpg
- Assets/hero_starter_pack.png
- Assets/head.twig
- Assets/price.twig
- Assets/discount.twig
- Assets/externals_scripts.twig
- Assets/slide3_bg.png
- Assets/navigation.twig
- Assets/layout.votepage.twig
- Assets/logo_rey_esqueleto_v2.jpg
- Assets/app.twig
- Assets/header.twig
- Assets/cat_otros.webp
- Assets/mc_dirt_dark.svg
- Assets/cat_club_vip.webp
- Assets/package-media.twig
- Assets/function.serverRequest.twig
- Assets/logo_rey_esqueleto.jpg
- Assets/layout.cryptowidget.twig
- Assets/hero_character.png
- Assets/layout.footer.twig
- Assets/sidebar.twig
- Assets/footer.twig
- Assets/tiered-actions.twig
- Assets/package-actions.twig
- Assets/layout.basket.twig
- Assets/logo_tienda_oficial.jpg
- Assets/externals_assets.twig
- Assets/logo_rey_esqueleto_final.jpg
- Assets/cat_rangos.webp
- Assets/languageConfig.twig
- Assets/hero_club_thunder.webp
- Assets/quantityAddon.twig
- Assets/package-entry.twig
- Assets/layout.patrons.twig
- Assets/layout.sidebar.twig
- Assets/slide2_bg.png
- Assets/layout.topbar.twig
- Assets/layout.categoryListItems.twig
- Assets/layout.header.twig
- Assets/cat_icon_bag.png
- Assets/function.exportedFunctions.twig
- Assets/constants.twig
- Assets/thunder_logo.png
- Assets/config.twig
- Assets/thunder_full_logo.png
- Assets/cat_sample_icon.png
- Assets/spawn_bg.png
- Assets/layout.announcement.twig
- Assets/cat_llaves.webp
- Assets/mc_deepslate_ores.svg
- Assets/banner_tienda_oficial.jpg
