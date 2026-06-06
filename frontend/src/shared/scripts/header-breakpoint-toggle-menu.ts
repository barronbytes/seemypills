// Depends on: src/core/component-loader.ts
// Listens for the `component-loaded` CustomEvent (bubbled to document) dispatched by
// ComponentLoader after it injects a component's HTML. Filters to only run when the
// header component finishes loading.
document.addEventListener('component-loaded', (event: Event) => {
  const { src } = (event as CustomEvent<{ src: string }>).detail;

  // Only activate toggle behavior after the header component has loaded.
  if (!src.includes('header')) return;

  // id: #mobile-section — the collapsible nav block shown on mobile/tablet
  const mobileMenu = document.querySelector<HTMLElement>('#mobile-section');
  // class: .toggle-menu.open  — hamburger button that opens the mobile menu
  const openBtn = document.querySelector<HTMLElement>('.toggle-menu.open');
  // class: .toggle-menu.close — X button that closes the mobile menu
  const closeBtn = document.querySelector<HTMLElement>('.toggle-menu.close');

  if (!mobileMenu || !openBtn || !closeBtn) {
    console.error('Toggle elements not found after component load.');
    return;
  }

  openBtn.addEventListener('click', () => {
    mobileMenu.setAttribute('data-visible', 'true');
    openBtn.setAttribute('aria-expanded', 'true');
    closeBtn.setAttribute('aria-expanded', 'true');
  });

  closeBtn.addEventListener('click', () => {
    mobileMenu.setAttribute('data-visible', 'false');
    openBtn.setAttribute('aria-expanded', 'false');
    closeBtn.setAttribute('aria-expanded', 'false');
    openBtn.focus(); // return focus to the trigger button for keyboard users
  });
});
