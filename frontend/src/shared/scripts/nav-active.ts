document.addEventListener('component-loaded', (event: Event) => {
  const { src } = (event as CustomEvent<{ src: string }>).detail;
  if (!src.includes('header')) return;

  const currentPath = window.location.pathname;

  document.querySelectorAll<HTMLAnchorElement>('.header-nav .button-menu').forEach(link => {
    const linkPath = new URL(link.href, window.location.origin).pathname;
    const isHome = (currentPath === '/' || currentPath === '/index.html') && (linkPath === '/' || linkPath === '/index.html');
    const isMatch = linkPath !== '/index.html' && linkPath !== '/' && currentPath === linkPath;

    if (isHome || isMatch) link.setAttribute('aria-current', 'page');
  });
});
