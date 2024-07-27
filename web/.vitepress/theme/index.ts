import { h } from 'vue';
import DefaultTheme from 'vitepress/theme';
import type { Theme } from 'vitepress';
import './style.css';
import './assets/custom.css';
import LatestFeatures from '../../components/LatestFeatures.vue';
import SecurityInfo from '../../components/SecurityInfo.vue';
import LinksComponent from '../../components/LinksComponent.vue';
import ModelIdentifierTable from '../../components/ModelIdentifierTable.vue';

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // You can use layout slots if needed
    });
  },
  enhanceApp({ app, router, siteData }) {
    app.component('LatestFeatures', LatestFeatures);
    app.component('SecurityInfo', SecurityInfo);
    app.component('LinksComponent', LinksComponent);
    app.component('ModelIdentifierTable', ModelIdentifierTable);
    // No need to add routes here
  },
} satisfies Theme;
