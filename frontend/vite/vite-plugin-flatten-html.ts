import type { Plugin } from 'vite';
import { PAGES_SOURCE_DIR } from './vite-util-discover-pages';

const PAGES_OUTPUT_PREFIX = `${PAGES_SOURCE_DIR}/`;

// Relocates built HTML pages from src/pages/ to the dist root so production paths stay clean
export function flattenHtmlOutputPlugin(): Plugin {
  return {
    name: 'flatten-page-html-output',
    // Runs after vite:build-html (which emits HTML into the bundle) so the entries exist to rename
    enforce: 'post',
    generateBundle(_options, bundle) {
      for (const fileName of Object.keys(bundle)) {
        const file = bundle[fileName];
        if (fileName.startsWith(PAGES_OUTPUT_PREFIX) && file.type === 'asset') {
          this.emitFile({
            type: 'asset',
            fileName: fileName.slice(PAGES_OUTPUT_PREFIX.length),
            source: file.source,
          });
          delete bundle[fileName];
        }
      }
    },
  };
}
