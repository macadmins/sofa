const puppeteer = require('puppeteer');

async function deepMobileAnalysis() {
  console.log('🔬 Deep Mobile Layout Analysis\n');
  
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  // iPhone SE viewport for maximum constraints
  await page.setViewport({ 
    width: 375, 
    height: 667,
    isMobile: true,
    deviceScaleFactor: 2
  });
  
  await page.goto('http://localhost:5174/', { waitUntil: 'networkidle0' });
  
  const analysis = await page.evaluate(() => {
    const results = {};
    
    // 1. Analyze the wide timeline element
    const timelineElement = document.querySelector('.flex.gap-3.pb-2');
    if (timelineElement) {
      const rect = timelineElement.getBoundingClientRect();
      const style = window.getComputedStyle(timelineElement);
      results.timeline = {
        width: rect.width,
        left: rect.left,
        right: window.innerWidth - rect.right,
        overflow: rect.width > window.innerWidth,
        parent: timelineElement.parentElement?.className,
        styles: {
          width: style.width,
          minWidth: style.minWidth,
          maxWidth: style.maxWidth,
          overflow: style.overflow,
          overflowX: style.overflowX
        }
      };
    }
    
    // 2. Analyze dashboard container
    const dashContainer = document.querySelector('.dashboard-container');
    if (dashContainer) {
      const rect = dashContainer.getBoundingClientRect();
      const style = window.getComputedStyle(dashContainer);
      results.dashboardContainer = {
        width: rect.width,
        left: rect.left,
        right: window.innerWidth - rect.right,
        styles: {
          margin: style.margin,
          padding: style.padding,
          maxWidth: style.maxWidth,
          boxSizing: style.boxSizing
        }
      };
    }
    
    // 3. Analyze Bento grid
    const bentoGrid = document.querySelector('.bento-grid');
    if (bentoGrid) {
      const rect = bentoGrid.getBoundingClientRect();
      const style = window.getComputedStyle(bentoGrid);
      results.bentoGrid = {
        width: rect.width,
        left: rect.left,
        right: window.innerWidth - rect.right,
        styles: {
          margin: style.margin,
          padding: style.padding,
          gap: style.gap,
          gridTemplateColumns: style.gridTemplateColumns
        }
      };
    }
    
    // 4. Analyze platform navigation
    const platformNav = document.querySelector('.flex.flex-wrap.justify-center.gap-3.mb-12');
    if (platformNav) {
      const rect = platformNav.getBoundingClientRect();
      const style = window.getComputedStyle(platformNav);
      results.platformNav = {
        width: rect.width,
        left: rect.left,
        right: window.innerWidth - rect.right,
        styles: {
          justifyContent: style.justifyContent,
          gap: style.gap,
          margin: style.margin,
          padding: style.padding
        }
      };
    }
    
    // 5. Check for any elements with negative margins
    const allElements = document.querySelectorAll('*');
    const negativeMargins = [];
    allElements.forEach(el => {
      const style = window.getComputedStyle(el);
      if (style.marginLeft.includes('-') || style.marginRight.includes('-')) {
        negativeMargins.push({
          tag: el.tagName,
          class: el.className,
          marginLeft: style.marginLeft,
          marginRight: style.marginRight
        });
      }
    });
    results.negativeMargins = negativeMargins.slice(0, 10);
    
    // 6. Check viewport meta tag
    const viewportMeta = document.querySelector('meta[name="viewport"]');
    results.viewport = viewportMeta ? viewportMeta.content : 'No viewport meta found';
    
    return results;
  });
  
  console.log('📊 Deep Analysis Results:\n');
  
  console.log('1. TIMELINE ELEMENT (causing 2108px overflow):');
  if (analysis.timeline) {
    console.log(`   Width: ${analysis.timeline.width}px`);
    console.log(`   Position: left=${analysis.timeline.left}px, right=${analysis.timeline.right}px`);
    console.log(`   Parent: ${analysis.timeline.parent}`);
    console.log(`   Overflow-X: ${analysis.timeline.styles.overflowX}`);
    console.log(`   Min-Width: ${analysis.timeline.styles.minWidth}`);
  }
  
  console.log('\n2. DASHBOARD CONTAINER:');
  if (analysis.dashboardContainer) {
    console.log(`   Width: ${analysis.dashboardContainer.width}px`);
    console.log(`   Position: left=${analysis.dashboardContainer.left}px, right=${analysis.dashboardContainer.right}px`);
    console.log(`   Margin: ${analysis.dashboardContainer.styles.margin}`);
    console.log(`   Padding: ${analysis.dashboardContainer.styles.padding}`);
    console.log(`   Max-Width: ${analysis.dashboardContainer.styles.maxWidth}`);
  }
  
  console.log('\n3. BENTO GRID:');
  if (analysis.bentoGrid) {
    console.log(`   Width: ${analysis.bentoGrid.width}px`);
    console.log(`   Position: left=${analysis.bentoGrid.left}px, right=${analysis.bentoGrid.right}px`);
    console.log(`   Margin: ${analysis.bentoGrid.styles.margin}`);
    console.log(`   Gap: ${analysis.bentoGrid.styles.gap}`);
  }
  
  console.log('\n4. PLATFORM NAVIGATION:');
  if (analysis.platformNav) {
    console.log(`   Width: ${analysis.platformNav.width}px`);
    console.log(`   Position: left=${analysis.platformNav.left}px, right=${analysis.platformNav.right}px`);
    console.log(`   Justify: ${analysis.platformNav.styles.justifyContent}`);
    console.log(`   Gap: ${analysis.platformNav.styles.gap}`);
  }
  
  console.log('\n5. NEGATIVE MARGINS:');
  if (analysis.negativeMargins.length > 0) {
    analysis.negativeMargins.forEach(el => {
      console.log(`   ${el.tag}.${el.class}: left=${el.marginLeft}, right=${el.marginRight}`);
    });
  } else {
    console.log('   No negative margins found');
  }
  
  console.log(`\n6. VIEWPORT META: ${analysis.viewport}`);
  
  // Calculate spacing imbalance
  if (analysis.dashboardContainer) {
    const leftSpace = analysis.dashboardContainer.left;
    const rightSpace = analysis.dashboardContainer.right;
    const imbalance = Math.abs(leftSpace - rightSpace);
    
    console.log(`\n📏 SPACING ANALYSIS:`);
    console.log(`   Left space: ${leftSpace}px`);
    console.log(`   Right space: ${rightSpace}px`);
    console.log(`   Imbalance: ${imbalance}px`);
    
    if (imbalance > 5) {
      console.log(`   ❌ ISSUE: ${imbalance}px spacing difference detected`);
    } else {
      console.log(`   ✅ BALANCED: Spacing within acceptable range`);
    }
  }
  
  await browser.close();
}

deepMobileAnalysis().catch(console.error);