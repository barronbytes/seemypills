---
description: Create a UI Component in `./frontend/src/shared/components/`
argument-hint: Component file path | Component file name | Component summary
---

## Content

Parse $ARGUMENTS to get the following values:

- [filepath]: Component file path
- [filename]: Component name from $ARGUMENTS
- [summary]: Component summary from $ARGUMENTS

** CRITICAL RULE:** Do not create new file paths without asking first if [FILEPATH] does not exist

## Task

Make a UI component according to the [filepath], [filename], and [summary] provided, following these guidelines:

- Convert [filepath] (if present) and filename into lowercase letters with hypens between words
- Create the component file in `./frontend/src/shared/components/[filepath]/[filename].html`
  - Resolve filepath to avoid `./frontend/src/shared/components/some-path//some-name.html` for nested [filepath] values
- Reference the [summary] when making the component

## Guidelines

### Accessibility

- All interactive elements must have descriptive `aria-label` attributes
- Buttons that toggle state must manage `aria-expanded` (see `menu-toggle.ts` for the pattern)
- `header.html` must include a skip navigation link using the `.skip-nav-link` class that targets the main content landmark
- Use `.sr-only` for any text that should be read by screen readers but not visible on screen
- All text/background color pairings must meet WCAG AAA contrast ratios (7:1 minimum)
- Use native HTML5 elements (`<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`, `<article>`, `<button>`, etc.) over `<div>` whenever a more specific tag applies
- Never reinvent what the browser handles natively

### Layout

- Use only CSS Grid and Flexbox for layout structure
  - Already setup some class names in CSS Grid (`.grid`, `.grid-center`, etc.) and Flexbox (`.flex`, `.flex-center`, etc.) for use
- Never use floats, `position` hacks, or inline `display` overrides to achieve layout
- Vertically stacked elements must be separated by multiples of 16px — use `--gutter-row-1` (16px) as the base unit
- Horizontally adjacent elements must be separated by multiples of 10px — use `--gutter-col-padding` (10px) as the base unit
- Default inner padding for components is `var(--gutter-row-padding) var(--gutter-col-padding)` (8px top/bottom, 10px left/right)
- Borders follow the `.button-main` pattern from `layout.css`:
  - Default: `0.1rem solid <color>` with matching `background-color`
  - Hover: border color shifts to `--gray-900`, background inverts to `--logo-blue`, text to `--gray-100`
  - Use `border-radius: 0.5rem` and `transition: background-color 200ms ease-in-out`
  - Colors may vary by component context but the structural pattern must be followed

### IDs and Class Names (General)

- Do not create new IDs or class names without asking first
- `layout.css` already covers most layout, spacing, color, and button needs — check it before adding anything new
- When a new component-specific name is needed, ask before creating it and follow the existing naming pattern: lowercase, hyphen-separated, descriptive (e.g. `service-card`, `toggle-menu`)

### IDs and Class Names (header.html only)

- `menu-toggle.ts` targets these specific selectors — they must be present and unchanged:
  - `#mobile-section` — the collapsible nav block
  - `.toggle-menu.open` — the hamburger button that opens the menu
  - `.toggle-menu.close` — the X button that closes the menu
- Do not rename or restructure these because they are defined in `menu-toggle.ts` and must remain unchanged

### Responsive Design

- Always pull values from the CSS custom properties defined in `layout.css` — do not hardcode px values
- Use a mobile first design with approved media query breakpoints:
  - mobile views: `--breakpoint-4` (mobile portrait), `--breakpoint-6` (mobile landscape)
  - tablet views: `--breakpoint-9` (tablet portrait), `--breakpoint-12` (tablet landscape)
  - laptop views: `--breakpoint-14` (laptop)
- Use gutter variables for all spacing: `--gutter-col-*` for horizontal, `--gutter-row-*` for vertical

### Colors

- Always pull values from the CSS custom properties defined in `layout.css` — do not hardcode color or font values
- Always verify contrast ratios meet WCAG AAA (7:1) for all text/background pairs
- Use color scale variables (`--gray-100` through `--gray-900`, `--red-*`, `--green-*`, `--blue-*`, `--orange-*`, `--logo-background`, `--logo-blue`, `--logo-yellow`) — never raw hex values
- Apply the 60-30-10 rule: 60% neutral canvas backgrounds, 30% structural text and secondary containers, 10% accent (`--logo-yellow`, `--logo-blue`) reserved for primary actions and critical feedback


## Variants

A variant is a meaningful visual or behavioral difference in a component that serves a distinct use case. Do not create a variant just because a color or size changes — only extract a variant when the difference changes how or where the component is used.

Common variant triggers:
- State: default, loading, error, empty, success
- Hierarchy: primary action vs. secondary action
- Context: standalone use vs. embedded in another component

When adding a variant, name it clearly after its purpose (e.g. `primary`, `secondary`, `loading`) not after its appearance (e.g. `blue`, `large`).

## Testing