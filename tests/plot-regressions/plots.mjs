import { chromium, expect } from '@playwright/test';
import fs from 'node:fs/promises';
const out='artifacts/screenr-plots';await fs.mkdir(out,{recursive:true});const browser=await chromium.launch(),results=[];
async function graphic(page,selector){const g=page.locator(selector).first();await expect(g).toBeVisible();await g.scrollIntoViewIfNeeded();await expect(g).toBeInViewport();await expect.poll(()=>g.locator('path,circle,rect,line,polygon').count()).toBeGreaterThan(2);expect(await g.evaluate(el=>[...el.querySelectorAll('*')].flatMap(m=>[...m.attributes].filter(a=>/^(d|points|cx|cy|r|x|y|x1|x2|y1|y2|width|height)$/.test(a.name)&&/NaN|Infinity/.test(a.value)).map(a=>a.value)))).toEqual([]);}
try{for(const width of [1280,390]){
 const ctx=await browser.newContext({viewport:{width,height:950}}),page=await ctx.newPage(),r={width,passed:[],errors:[]};
 await page.addInitScript(()=>localStorage.setItem('screenr_wizard_seen','true'));
 page.on('pageerror',e=>r.errors.push(e.message));page.on('dialog',d=>d.accept());page.setDefaultTimeout(20000);
 try{
  await page.goto('http://127.0.0.1:8080/screenr.html',{waitUntil:'load'});
  await page.evaluate(()=>loadExampleDataset());
  await expect(page.locator('#recordList .record-item')).toHaveCount(13);
  expect(await page.evaluate(()=>records.every(rec=>getDecisionForRecord(rec.id)?.status==='include'&&!!getPreferredExtractionData(rec.id).effect))).toBe(true);
  const before=await page.evaluate(()=>JSON.stringify({records,decisions:[...decisions],extractions:[...extractions],settings:state.metaSettings}));
  for(const [name,open,close,selector] of [
   ['forest','showMetaAnalysis','closeMetaModal','#metaContent svg'],
   ['prisma','showPRISMA','closePrismaModal','#prismaContent svg'],
   ['funnel','showFunnelPlot','closeFunnelModal','#funnelSvg'],
   ['sensitivity','showSensitivityAnalysis','closeSensitivityModal','#sensitivityModal svg']]){
   await page.evaluate(fn=>window[fn](),open);await graphic(page,selector);r.passed.push(name);
   if(name==='sensitivity') {
     await expect(page.locator('#sensitivityModal')).toBeInViewport();
     expect(await page.locator('#sensitivityModal').evaluate(e=>getComputedStyle(e).position)).toBe('fixed');
     await page.locator('#sensitivityModal button[onclick*="cumulative"]').click();
     await expect(page.locator('#sensitivityTab_cumulative svg')).toHaveCount(2);
     for(let i=0;i<2;i++)await graphic(page,`#sensitivityTab_cumulative svg:nth-of-type(${i+1})`);
     await page.locator('#sensitivityModal button[onclick*="leaveOneOut"]').click();
     await graphic(page,'#sensitivityTab_leaveOneOut svg');
   }
   await page.setViewportSize({width:width+20,height:970});await graphic(page,selector);
   await page.screenshot({path:out+'/'+name+'-'+width+'.png',fullPage:false});
   await page.evaluate(fn=>window[fn](),close);
  }
  expect(await page.evaluate(()=>JSON.stringify({records,decisions:[...decisions],extractions:[...extractions],settings:state.metaSettings}))).toBe(before);
  // Sensitivity must read edited canonical extractions, not stale demo-only fields.
  const count=await page.evaluate(()=>{decisions.get(records[0].id).final='exclude';return records.length-1;});
  await page.evaluate(()=>showSensitivityAnalysis());await graphic(page,'#sensitivityModal svg');
  await expect(page.locator('#sensitivityModal')).toContainText(String(count));
  expect(r.errors).toEqual([]);
 }catch(e){r.failure=e.stack;await page.screenshot({path:out+'/failure-'+width+'.png'}).catch(()=>{});throw e;}
 finally{results.push(r);await fs.writeFile(out+'/results.json',JSON.stringify(results,null,2));await ctx.close();}
}}finally{await browser.close();}
console.log(JSON.stringify(results));
