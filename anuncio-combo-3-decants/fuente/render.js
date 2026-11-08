const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.cwd() + '/frascos.html');
  await p.waitForTimeout(300);
  await p.locator('#escena').screenshot({ path: 'frascos.png', omitBackground: true });
  await b.close();
})();
