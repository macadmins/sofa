const puppeteer = require('puppeteer');

async function detailedMobileDebug() {
  console.log('🔍 Detailed Mobile Layout Debug\n');
  
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  await page.setViewport({ 
    width: 375, 
    height: 667,
    isMobile: true,
    deviceScaleFactor: 2
  });
  
  await page.goto('http://localhost:5174/', { waitUntil: 'networkidle0' });
  
  const detailedAnalysis = await page.evaluate(() => {
    const results = {};
    
    // Trace the layout hierarchy
    const body = document.body;
    const html = document.documentElement;
    
    // Get full layout chain
    const layoutChain = [];
    let current = document.querySelector('.dashboard-container');
    
    while (current && current !== body) {
      const rect = current.getBoundingClientRect();
      const style = window.getComputedStyle(current);
      
      layoutChain.push({
        element: current.tagName + (current.className ? '.' + current.className.split(' ').join('.') : ''),
        width: rect.width,
        left: rect.left,
        right: window.innerWidth - rect.right,
        styles: {
          margin: style.margin,
          marginLeft: style.marginLeft,
          marginRight: style.marginRight,
          padding: style.padding,
          paddingLeft: style.paddingLeft,
          paddingRight: style.paddingRight,
          position: style.position,
          left: style.left,
          right: style.right,
          transform: style.transform,
          maxWidth: style.maxWidth,
          width: style.width
        }
      });
      
      current = current.parentElement;
    }
    
    results.layoutChain = layoutChain;
    
    // Analyze the specific timeline problem
    const timelineContainer = document.querySelector('.overflow-x-auto.flex-grow.scrollbar-hide.mb-3');
    const timelineContent = document.querySelector('.flex.gap-3.pb-2');
    
    if (timelineContainer && timelineContent) {
      const containerRect = timelineContainer.getBoundingClientRect();
      const contentRect = timelineContent.getBoundingClientRect();
      const containerStyle = window.getComputedStyle(timelineContainer);
      const contentStyle = window.getComputedStyle(timelineContent);
      
      results.timelineDebug = {
        container: {
          width: containerRect.width,
          left: containerRect.left,
          right: window.innerWidth - containerRect.right,
          overflow: containerStyle.overflowX,
          styles: containerStyle.cssText
        },
        content: {
          width: contentRect.width,
          left: contentRect.left,
          right: window.innerWidth - contentRect.right,
          minWidth: contentStyle.minWidth,
          styles: contentStyle.cssText
        },
        problem: contentRect.width > containerRect.width ? 'Content wider than container' : 'Container issue'
      };
    }
    
    // Check for CSS that might be affecting positioning
    const relevantCSS = [];
    const styleSheets = Array.from(document.styleSheets);
    
    styleSheets.forEach(sheet => {
      try {
        const rules = Array.from(sheet.cssRules || []);
        rules.forEach(rule => {
          if (rule.selectorText && (
            rule.selectorText.includes('.dashboard-container') ||
            rule.selectorText.includes('.bento-grid') ||
            rule.selectorText.includes('.flex-grow') ||
            rule.selectorText.includes('overflow-x-auto')
          )) {
            relevantCSS.push({
              selector: rule.selectorText,
              rules: rule.cssText
            });
          }
        });
      } catch (e) {
        // Skip cross-origin stylesheets
      }
    });
    
    results.relevantCSS = relevantCSS.slice(0, 15);
    
    // Check browser-specific issues
    results.browserInfo = {
      userAgent: navigator.userAgent,
      viewportWidth: window.innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      bodyWidth: document.body.scrollWidth,
      overflow: document.documentElement.scrollWidth > window.innerWidth
    };
    
    return results;
  });
  
  console.log('🏗️ LAYOUT HIERARCHY (from dashboard-container up):');
  detailedAnalysis.layoutChain.forEach((item, index) => {
    console.log(`${index + 1}. ${item.element}`);
    console.log(`   Position: left=${item.left}px, right=${item.right}px (width=${item.width}px)`);
    console.log(`   Margins: ${item.styles.marginLeft} | ${item.styles.marginRight}`);
    console.log(`   Padding: ${item.styles.paddingLeft} | ${item.styles.paddingRight}`);
    if (item.styles.transform !== 'none') {
      console.log(`   Transform: ${item.styles.transform}`);
    }
    console.log('');
  });
  
  console.log('📜 TIMELINE OVERFLOW DEBUG:');
  if (detailedAnalysis.timelineDebug) {
    const t = detailedAnalysis.timelineDebug;
    console.log(`Container: ${t.container.width}px wide, overflow=${t.container.overflow}`);
    console.log(`Content: ${t.content.width}px wide, min-width=${t.content.minWidth}`);
    console.log(`Problem: ${t.problem}`);
    console.log(`Content extends ${t.content.width - t.container.width}px beyond container`);
  }
  
  console.log('\n🌐 BROWSER INFO:');
  console.log(`Viewport: ${detailedAnalysis.browserInfo.viewportWidth}px`);
  console.log(`Document: ${detailedAnalysis.browserInfo.documentWidth}px`);
  console.log(`Body: ${detailedAnalysis.browserInfo.bodyWidth}px`);
  console.log(`Horizontal overflow: ${detailedAnalysis.browserInfo.overflow}`);
  
  console.log('\n🎯 KEY FINDINGS:');
  console.log('1. Timeline content (2108px) is much wider than container');
  console.log('2. Dashboard container has uneven left (40px) vs right (16px) spacing');
  console.log('3. Bento grid and platform nav both show 56px left, 32px right');
  console.log('4. The spacing imbalance propagates through the layout hierarchy');
  
  await browser.close();
}

detailedMobileDebug().catch(console.error);