import { readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// Project-root-relative path to the pages source directory, shared with vite-plugin-flatten-html
export const PAGES_SOURCE_DIR = 'src/pages';

const PAGES_DIR_URL = new URL(`../${PAGES_SOURCE_DIR}/`, import.meta.url);

export interface PageEntry {
  /** Rollup input key and flattened output file name, e.g. "upload-bottle" */
  name: string;
  /** Absolute path to file, e.g. ".../src/pages/upload-bottle.html" */
  sourcePath: string;
  /** Dev-server URL path, e.g. "/src/pages/upload-bottle.html" */
  devPath: string;
  /** Production URL path, e.g. "/upload-bottle.html" */
  routePath: string;
}

export function discoverPages(): PageEntry[] {
  const pagesDirPath = fileURLToPath(PAGES_DIR_URL);

  return readdirSync(pagesDirPath, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith('.html'))
    .map((entry) => ({
      name: entry.name.replace(/\.html$/, ''),
      sourcePath: fileURLToPath(new URL(entry.name, PAGES_DIR_URL)),
      devPath: `/${PAGES_SOURCE_DIR}/${entry.name}`,
      routePath: `/${entry.name}`,
    }));
}
