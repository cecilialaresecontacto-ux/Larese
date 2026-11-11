const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1500, height: 1800 } });
  p.on('console', m => console.log('console:', m.text()));
  p.on('pageerror', e => console.log('error:', e.message));
  for (const f of ['blanco', 'mascara']) {
    await p.goto(`http://localhost:8765/viales.html?fondo=blanco&${f}=1`);
    await p.waitForFunction(() => window.LISTO === true, null, { timeout: 120000 });
    await p.locator('canvas').screenshot({ path: `render-${f}.png` });
  }
  await b.close();
})();
