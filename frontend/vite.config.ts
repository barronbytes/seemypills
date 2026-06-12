import { defineConfig } from 'vitest/config';
import type { Connect } from 'vite';

export default defineConfig({
  root: '.', // Keeps the root directory as frontend/
  
  // Configure the development server to map production paths back to source paths
  server: {
    open: true,
    proxy: {}, // Placeholder if you need to bypass backend API cors later
  },
  
  // Force Vite to treat this as a true Multi-Page Application (MPA) in development
  appType: 'mpa', 

  // Vite plugins: dev-only routing rewrite, plus build-time HTML output flattening
  plugins: [
    {
      name: 'local-html-page-rewrites',
      configureServer(server) {
        // Rewrites the clean production path to the actual source file location during local testing
        const rewriteUploadBottlePath: Connect.NextHandleFunction = (req, _res, next) => {
          if (req.url === '/upload-bottle.html') {
            req.url = '/src/pages/upload-bottle.html';
          }
          next();
        };

        server.middlewares.use(rewriteUploadBottlePath);
      },
    },
    {
      name: 'flatten-page-html-output',
      // Relocates built HTML pages from src/pages/ to the dist root so production paths stay clean
      generateBundle(_options, bundle) {
        for (const fileName in bundle) {
          if (fileName.startsWith('src/pages/')) {
            const flattenedFileName = fileName.replace('src/pages/', '');
            bundle[fileName].fileName = flattenedFileName;
            bundle[flattenedFileName] = bundle[fileName];
            delete bundle[fileName];
          }
        }
      },
    },
  ],

  test: {
    env: {
      VITE_API_BASE_URL: 'http://localhost:8000',
    },
  },
  build: {
    rollupOptions: {
      input: {
        // Map entry keys to explicit root-level output endpoints
        main: new URL('index.html', import.meta.url).pathname,
        '404': new URL('404.html', import.meta.url).pathname,
        'upload-bottle': new URL('src/pages/upload-bottle.html', import.meta.url).pathname,
      },
      output: {
        // Ensure compiled HTML structures flatten into clean asset targets
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },
});