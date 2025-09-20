const puppeteer = require('puppeteer');

async function testMobileLayout() {
  console.log('📱 Testing Mobile Layout Issues\n');
  
  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox'] 
  });
  
  const page = await browser.newPage();
  
  // Set mobile viewport
  await page.setViewport({ 
    width: 375, 
    height: 667,
    isMobile: true,
    deviceScaleFactor: 2
  });
  
  const testPages = [
    'http://localhost:5174/',
    'http://localhost:5174/macos/sequoia'
  ];
  
  for (const url of testPages) {
    console.log(`\n🔍 Testing: ${url}`);
    
    await page.goto(url, { waitUntil: 'networkidle0' });
    
    // Analyze layout issues
    const layoutIssues = await page.evaluate(() => {
      const issues = [];
      const body = document.body;
      const container = document.querySelector('.dashboard-container') || 
                       document.querySelector('.features-container') ||
                       document.querySelector('main');
      
      // Check body overflow
      const bodyStyle = window.getComputedStyle(body);
      if (bodyStyle.overflowX === 'scroll' || body.scrollWidth > body.clientWidth) {
        issues.push(`Body horizontal overflow: ${body.scrollWidth}px width vs ${body.clientWidth}px viewport`);
      }
      
      // Check container positioning
      if (container) {
        const containerStyle = window.getComputedStyle(container);
        const containerRect = container.getBoundingClientRect();
        
        issues.push(`Container margins: left=${containerStyle.marginLeft}, right=${containerStyle.marginRight}`);
        issues.push(`Container padding: left=${containerStyle.paddingLeft}, right=${containerStyle.paddingRight}`);
        issues.push(`Container position: left=${containerRect.left}px, right=${window.innerWidth - containerRect.right}px`);
      }
      
      // Check for wide elements
      const allElements = document.querySelectorAll('*');
      const wideElements = [];
      
      allElements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.width > window.innerWidth && rect.width > 0) {
          wideElements.push({
            tag: el.tagName,
            class: el.className,
            width: rect.width,
            id: el.id
          });
        }
      });
      
      if (wideElements.length > 0) {
        issues.push(`Wide elements causing overflow:`);
        wideElements.slice(0, 5).forEach(el => {
          issues.push(`  - ${el.tag}.${el.class}: ${el.width}px`);
        });
      }
      
      // Check Bento grid specifically
      const bentoGrid = document.querySelector('.bento-grid');
      if (bentoGrid) {
        const bentoStyle = window.getComputedStyle(bentoGrid);
        const bentoRect = bentoGrid.getBoundingClientRect();
        issues.push(`Bento grid: width=${bentoRect.width}px, margins=${bentoStyle.margin}`);
      }
      
      // Check platform buttons
      const platformBtns = document.querySelector('.flex.flex-wrap.justify-center');
      if (platformBtns) {
        const btnRect = platformBtns.getBoundingClientRect();
        issues.push(`Platform buttons: width=${btnRect.width}px, left=${btnRect.left}px`);
      }
      
      return {
        viewportWidth: window.innerWidth,
        bodyWidth: body.scrollWidth,
        issues
      };
    });
    
    console.log(`Viewport: ${layoutIssues.viewportWidth}px`);
    console.log(`Body width: ${layoutIssues.bodyWidth}px`);
    
    if (layoutIssues.bodyWidth > layoutIssues.viewportWidth) {
      console.log(`❌ OVERFLOW: Body is ${layoutIssues.bodyWidth - layoutIssues.viewportWidth}px too wide`);
    }
    
    console.log('\nLayout Analysis:');
    layoutIssues.issues.forEach(issue => {
      console.log(`  ${issue}`);
    });
  }
  
  await browser.close();
}

testMobileLayout().catch(console.error);