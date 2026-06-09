// Custom element: <component-loader src="...path/to/component.html">
// Fetches the HTML file at `src`, injects it as innerHTML, then dispatches `component-loaded`.
class ComponentLoader extends HTMLElement {
  connectedCallback() {
    const src = this.getAttribute('src');
    if (!src) return;

    fetch(src)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.text();
      })
      .then(html => {
        this.innerHTML = html;
        // bubbles: true so listeners on `document` (e.g. menu-toggle.ts) can receive this event
        // without needing a direct reference to this element.
        // detail.src lets listeners filter by which component finished loading.
        this.dispatchEvent(new CustomEvent('component-loaded', {
          bubbles: true,
          detail: { src }
        }));
      })
      .catch(err => {
        console.error(`ComponentLoader error (${src}):`, err);
        
        // 1. Check if the app is running locally in development mode
        if (import.meta.env.DEV) {
          window.location.href = '/src/pages/404.html';
        } else {
          // 2. Fall back to the flat root layout when deployed live on AWS production
          window.location.href = '/404.html';
        }
      });
  }
}

customElements.define('component-loader', ComponentLoader);
