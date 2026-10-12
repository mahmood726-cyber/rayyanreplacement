from pathlib import Path
p=Path('screenr.html');t=p.read_text()
old='<div class="modal active" id="sensitivityModal">\n      <div class="modal-content" style="max-width: 1000px; max-height: 90vh; overflow-y: auto;">'
new='<div class="modal-overlay active" id="sensitivityModal" role="dialog" aria-modal="true" aria-label="Sensitivity analyses">\n      <div class="modal" style="max-width: 1000px; max-height: 90vh;">'
assert t.count(old)==1;p.write_text(t.replace(old,new,1))
p=Path('tests/plot-regressions/plots.mjs');t=p.read_text()
old='await expect(g).toBeVisible();await expect.poll'
new='await expect(g).toBeVisible();await g.scrollIntoViewIfNeeded();await expect(g).toBeInViewport();await expect.poll'
assert t.count(old)==1;t=t.replace(old,new,1)
old='r.passed.push(name);\n   await page.setViewportSize'
new='''r.passed.push(name);
   if(name==='sensitivity') {
     await expect(page.locator('#sensitivityModal')).toBeInViewport();
     expect(await page.locator('#sensitivityModal').evaluate(e=>getComputedStyle(e).position)).toBe('fixed');
     await page.locator('#sensitivityModal button[onclick*="cumulative"]').click();
     await expect(page.locator('#sensitivityTab_cumulative svg')).toHaveCount(2);
     for(let i=0;i<2;i++)await graphic(page,`#sensitivityTab_cumulative svg:nth-of-type(${i+1})`);
     await page.locator('#sensitivityModal button[onclick*="leaveOneOut"]').click();
     await graphic(page,'#sensitivityTab_leaveOneOut svg');
   }
   await page.setViewportSize'''
assert t.count(old)==1;t=t.replace(old,new,1);p.write_text(t)
