import { defineConfig } from 'vitest/config';
import { discoverPages } from './vite/vite-util-discover-pages';
import { routeRewriterPlugin } from './vite/vite-plugin-route-rewriter';
import { flattenHtmlOutputPlugin } from './vite/vite-plugin-flatten-html';

const pages = discoverPages();
const pageInputs = Object.fromEntries(
  pages.map((page): [string, string] => [page.name, page.sourcePath]),
);

export default defineConfig({
  root: '.', // Keeps the root directory as frontend/

  server: {
    open: true,
    proxy: {}, // Placeholder if you need to bypass backend API cors later
  },

  // Force Vite to treat this as a true Multi-Page Application (MPA) in development
  appType: 'mpa',

  plugins: [routeRewriterPlugin(pages), flattenHtmlOutputPlugin()],

  test: {
    env: {
      VITE_API_BASE_URL: 'http://localhost:8000',
    },
  },
  
  build: {
    rollupOptions: {
      input: {
        // Root-level entries; every other page is discovered from src/pages/
        main: new URL('index.html', import.meta.url).pathname,
        '404': new URL('404.html', import.meta.url).pathname,
        ...pageInputs,
      },
      output: {
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },
});
