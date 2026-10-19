const { chromium } = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + '/playwright' : 'playwright');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const http = require('node:http');
(async()=>{
 const app=require('node:path').join(__dirname, '..', '_app') + require('node:path').sep;
 const server=http.createServer((req,res)=>{
  const f=req.url==='/'?'index.html':req.url.slice(1);
  if(!['index.html','app.js','app.css'].includes(f)){res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type',f.endsWith('.js')?'application/javascript':f.endsWith('.css')?'text/css':'text/html');
  res.setHeader('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'");
  res.end(fs.readFileSync(app+f,'utf8').replace('{{TOKEN}}','qa-token'));
 });
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({executablePath:process.env.NOERA_BROWSER_PATH || undefined,headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const page=await browser.newPage({acceptDownloads:true}); const errors=[]; page.on('pageerror',e=>errors.push(e.message));
 const root='http://127.0.0.1:'+server.address().port;
 const ticks='638962000000000000';
 let content='# Documento\r\n\r\n**Prueba**\r\n'; let pendingSave=null; let slowResolve=null; let gets=0; let filesFail=true;
 const tree=[{type:'dir',name:'Proyecto',path:'Proyecto',mtime:ticks,children:[
  {type:'file',name:'nota.md',path:'Proyecto/nota.md',ext:'.md',mtime:ticks,size:30},
  {type:'file',name:'otro.txt',path:'Proyecto/otro.txt',ext:'.txt',mtime:ticks,size:8}
 ]}];
 await page.route('**/api/**',async route=>{
  const req=route.request(); const u=new URL(req.url());
  assert.equal(req.headers()['x-noera-token'],'qa-token');
  const json=o=>route.fulfill({json:o});
  if(u.pathname==='/api/tree')return json({tree,allowedExt:['.md','.txt','.json']});
  if(u.pathname==='/api/folder/meta')return json({taggedFolders:{}});
  if(u.pathname==='/api/file' && req.method()==='GET'){
   if(u.searchParams.get('path')==='Proyecto/otro.txt' && slowResolve) await new Promise(r=>{slowResolve=r;});
   return json({path:u.searchParams.get('path'),name:u.searchParams.get('path').split('/').pop(),content,mtime:ticks,size:30});
  }
  if(u.pathname==='/api/file' && req.method()==='PUT'){
   content=req.postData(); await new Promise(r=>{pendingSave=r;}); return json({mtime:ticks,size:content.length});
  }
  if(['/api/download','/api/zip','/api/noera/zip'].includes(u.pathname))return route.fulfill({body:'qa-content',contentType:'application/octet-stream'});
  if(u.pathname==='/api/noera/files'){gets++;return filesFail ? route.fulfill({status:500,json:{error:'fallo simulado'}}) : json({files:[{name:'app.js',path:'_app/app.js',content:'const test = true;',size:18,mtime:ticks}]});}
  if(u.pathname==='/api/noera/changelog')return json([]);
  return route.fulfill({status:404,json:{error:'Endpoint simulado no disponible'}});
 });
 try {
  await page.addInitScript(()=>localStorage.setItem('noera.exp','{broken'));
  await page.goto(root); await page.getByRole('heading',{name:'Central Noera'}).waitFor();
  console.log('PASS arranque con almacenamiento inválido');
  await page.locator('.card').click({button:'right'});
  await page.getByRole('menuitem',{name:'Descargar como ZIP'}).waitFor();
  let dl=page.waitForEvent('download'); await page.getByRole('menuitem',{name:'Descargar como ZIP'}).click(); assert.equal((await dl).suggestedFilename(),'Proyecto.zip');
  console.log('PASS descarga ZIP desde tarjeta');
  await page.locator('.card').click();
  await page.locator('.frow[data-item-path="Proyecto/nota.md"]').click({button:'right'});
  dl=page.waitForEvent('download'); await page.getByRole('menuitem',{name:'Descargar archivo',exact:true}).click(); assert.equal((await dl).suggestedFilename(),'nota.md');
  console.log('PASS descarga individual desde lista');
  await page.locator('.frow[data-item-path="Proyecto/nota.md"]').click(); await page.locator('.md h1').waitFor();
  await page.getByRole('button',{name:'Editar',exact:true}).click(); await page.locator('#editor').fill('primera\nversión');
  await page.getByRole('button',{name:'Guardar',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#btn-save').disabled);
  await page.locator('#editor').fill('segunda\nversión');
  while(!pendingSave)await new Promise(r=>setTimeout(r,10)); pendingSave();
  await page.getByRole('button',{name:'Guardar',exact:true}).waitFor({state:'visible'});
  await page.waitForFunction(()=>!document.querySelector('#btn-save').disabled);
  assert.equal(content,'primera\r\nversión'); await page.getByText('Sin guardar',{exact:true}).waitFor();
  console.log('PASS edición durante guardado y conservación CRLF');
  await page.locator('#tree [data-path="Proyecto"] > .row').click(); await page.getByRole('button',{name:'Descartar',exact:true}).click();
  await page.locator('.flist').waitFor();
  await page.locator('#tree [data-path="Proyecto"] > .row .chev').click();
  slowResolve=true;
  await page.locator('.frow[data-item-path="Proyecto/otro.txt"]').click();
  while(typeof slowResolve!=='function')await new Promise(r=>setTimeout(r,10));
  await page.locator('#tree [data-path="Proyecto/nota.md"] > .row').click(); await page.locator('.reader').waitFor();
  const releaseSlow=slowResolve; slowResolve=null; releaseSlow(); await page.waitForTimeout(150);
  assert.equal(await page.locator('#crumbs .cur').innerText(),'nota.md');
  console.log('PASS respuesta antigua descartada al navegar');
  content='[x](https://example.org/**x**/~~y~~)\n\n<script>window.hacked=true</script>\n\n<img src=x onerror=alert(1)>';
  await page.locator('#tree [data-path="Proyecto/otro.txt"] > .row').click();
  await page.locator('#tree [data-path="Proyecto/nota.md"] > .row').click(); await page.locator('.md a').waitFor();
  assert.equal(await page.locator('.md a').getAttribute('href'),'https://example.org/**x**/~~y~~');
  assert.equal(await page.locator('.md script,.md img').count(),0);
  console.log('PASS Markdown escapa HTML y conserva URL con formato');
  await page.getByRole('button',{name:'Código de Noera',exact:true}).click(); await page.getByText('Error cargando archivos de Noera: fallo simulado',{exact:true}).first().waitFor();
  await page.waitForTimeout(250); assert.equal(gets,1);
  await page.getByRole('button',{name:/Cambios Realizados/}).click(); await page.locator('.emptybox').filter({hasText:'Sin cambios registrados.'}).waitFor();
  console.log('PASS código Noera sin bucles de petición en error o lista vacía');
  filesFail=false;
  await page.getByRole('button',{name:/Archivos en Tiempo Real/}).click();
  await page.getByRole('button',{name:'Reintentar',exact:true}).click();
  await page.locator('.live-code-pre').waitFor(); assert.equal(gets,2);
  console.log('PASS reintento y visor de código fuente');
  await page.locator('#tree [data-path="Proyecto/nota.md"]').focus();
  await page.keyboard.press('Shift+F10');
  dl=page.waitForEvent('download'); await page.getByRole('menuitem',{name:'Descargar archivo',exact:true}).click(); assert.equal((await dl).suggestedFilename(),'nota.md');
  console.log('PASS descarga desde árbol y menú con teclado');
  await page.setViewportSize({width:390,height:700});
  await page.getByRole('button',{name:'Noera',exact:true}).click();
  await page.locator('.card').click({button:'right'});
  const menu=await page.locator('#ctx').boundingBox(); assert.ok(menu.x>=0 && menu.y>=0 && menu.x+menu.width<=390 && menu.y+menu.height<=700);
  console.log('PASS menú contextual dentro de pantalla móvil');
  assert.deepEqual(errors,[]); console.log('PASS sin excepciones JavaScript');
 }catch(e){console.error('PAGE',await page.locator('#viewer').innerText());console.error('ERRORS',errors);throw e;}finally{await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1});
