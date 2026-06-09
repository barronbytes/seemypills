import { defineConfig } from 'vite';

export default defineConfig({
  root: '.', // Keeps the root directory as frontend/
  build: {
    rollupOptions: {
      input: {
        // 1. Define every physical HTML page as an explicit entry point using standard URL paths
        main: new URL('index.html', import.meta.url).pathname,
        notFound: new URL('404.html', import.meta.url).pathname,
      },
    },
  },
});