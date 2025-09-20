const puppeteer = require('puppeteer');

const pages = [
  { name: 'Dashboard', url: 'http://localhost:5174/' },
  { name: 'macOS Sequoia', url: 'http://localhost:5174/macos/sequoia' },
  { name: 'macOS Sonoma', url: 'http://localhost:5174/macos/sonoma' },
  { name: 'macOS Tahoe', url: 'http://localhost:5174/macos/tahoe' },
  { name: 'iOS 18', url: 'http://localhost:5174/ios/ios18' },
  { name: 'iOS 26', url: 'http://localhost:5174/ios/ios26' },
  { name: 'tvOS 18', url: 'http://localhost:5174/tvos/tvos18' },
  { name: 'tvOS 26', url: 'http://localhost:5174/tvos/tvos26' },
  { name: 'watchOS 11', url: 'http://localhost:5174/watchos/watchos11' },
  { name: 'watchOS 26', url: 'http://localhost:5174/watchos/watchos26' },
  { name: 'visionOS 2', url: 'http://localhost:5174/visionos/visionos2' },
  { name: 'visionOS 26', url: 'http://localhost:5174/visionos/visionos26' },
  { name: 'Safari 18', url: 'http://localhost:5174/safari/safari18' }
];

async function testPagePerformance() {
  console.log('🚀 Starting SOFA Dashboard Performance Test\n');
  
  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox'] 
  });
  
  const results = [];
  
  for (const page of pages) {
    try {
      console.log(`Testing: ${page.name}...`);
      
      const tab = await browser.newPage();
      
      // Enable performance monitoring
      await tab.coverage.startJSCoverage();
      await tab.coverage.startCSSCoverage();
      
      const startTime = Date.now();
      
      // Navigate and wait for network idle
      await tab.goto(page.url, { 
        waitUntil: 'networkidle0',
        timeout: 30000 
      });
      
      const loadTime = Date.now() - startTime;
      
      // Check for console errors
      const logs = await tab.evaluate(() => {
        return {
          errors: window.console.errors || [],
          warnings: window.console.warnings || []
        };
      });
      
      // Take performance metrics
      const metrics = await tab.metrics();
      
      // Check for specific elements
      const elements = await tab.evaluate(() => {
        const issues = [];
        
        // Check for missing images
        const images = document.querySelectorAll('img');
        images.forEach(img => {
          if (img.naturalWidth === 0) {
            issues.push(`Missing image: ${img.src}`);
          }
        });
        
        // Check for invisible text (flash of invisible text)
        const textElements = document.querySelectorAll('h1, h2, h3, .text-lg, .text-base');
        textElements.forEach(el => {
          const style = window.getComputedStyle(el);
          if (style.color === 'transparent' && !style.background.includes('gradient')) {
            issues.push(`Transparent text without gradient: ${el.tagName}`);
          }
        });
        
        // Check for layout shifts
        const animations = document.getAnimations();
        const activeAnimations = animations.filter(anim => 
          anim.playState === 'running' || anim.playState === 'pending'
        );
        
        return {
          issues,
          activeAnimations: activeAnimations.length,
          loadedImages: images.length,
          visibleElements: textElements.length
        };
      });
      
      results.push({
        page: page.name,
        url: page.url,
        loadTime,
        metrics: {
          jsHeapUsedSize: Math.round(metrics.JSHeapUsedSize / 1024 / 1024 * 100) / 100,
          domElements: metrics.Nodes,
          jsEventListeners: metrics.JSEventListeners
        },
        elements,
        status: loadTime < 3000 ? '✅ Good' : loadTime < 5000 ? '⚠️ Slow' : '❌ Poor'
      });
      
      await tab.close();
      
    } catch (error) {
      console.error(`Error testing ${page.name}:`, error.message);
      results.push({
        page: page.name,
        error: error.message,
        status: '❌ Error'
      });
    }
  }
  
  await browser.close();
  
  // Print results
  console.log('\n📊 Performance Test Results:\n');
  
  results.forEach(result => {
    console.log(`${result.status} ${result.page}`);
    console.log(`   Load Time: ${result.loadTime}ms`);
    if (result.metrics) {
      console.log(`   JS Heap: ${result.metrics.jsHeapUsedSize}MB`);
      console.log(`   DOM Nodes: ${result.metrics.domElements}`);
      console.log(`   Images: ${result.elements.loadedImages}`);
    }
    if (result.elements && result.elements.issues.length > 0) {
      console.log(`   Issues: ${result.elements.issues.length}`);
      result.elements.issues.slice(0, 3).forEach(issue => {
        console.log(`     - ${issue}`);
      });
    }
    console.log('');
  });
  
  // Summary
  const avgLoadTime = results
    .filter(r => r.loadTime)
    .reduce((sum, r) => sum + r.loadTime, 0) / results.filter(r => r.loadTime).length;
    
  console.log(`📈 Average Load Time: ${Math.round(avgLoadTime)}ms`);
  console.log(`🎯 Total Pages Tested: ${results.length}`);
  console.log(`✅ Successful Loads: ${results.filter(r => r.status.includes('✅')).length}`);
}

// Run the test
testPagePerformance().catch(console.error);