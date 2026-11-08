const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 900, height: 900 }, deviceScaleFactor: 3 });
  await p.goto('file://' + process.cwd() + '/vial3.html');
  await p.waitForTimeout(400);
  await p.locator('#escena').screenshot({ path: 'viales3.png', omitBackground: true });
  await b.close();
})();
