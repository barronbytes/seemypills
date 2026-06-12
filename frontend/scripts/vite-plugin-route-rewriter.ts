import type { Connect, Plugin } from 'vite';
import type { PageEntry } from './vite-util-discover-pages';

// Dev-only: rewrites clean production paths (/foo.html) to their src/pages/ source files
export function routeRewriterPlugin(pages: PageEntry[]): Plugin {
  return {
    name: 'local-html-page-rewrites',
    configureServer(server) {
      const rewritePageRoutes: Connect.NextHandleFunction = (req, _res, next) => {
        const page = pages.find((entry) => entry.routePath === req.url);
        if (page) {
          req.url = page.devPath;
        }
        next();
      };

      server.middlewares.use(rewritePageRoutes);
    },
  };
}
