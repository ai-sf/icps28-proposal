// Asset path helper — prefixes BASE_URL so the site works under a
// GitHub Pages project path (e.g. /repo/) as well as at the root.
export const asset = (p: string) => `${import.meta.env.BASE_URL}assets/${p}`;
