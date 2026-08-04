// Stable kebab-case ids for Open Design element targeting (`data-od-id`).
// Used by repeated components so review/comment tools can pin feedback to a
// specific instance (e.g. `speaker-fabiola-gianotti`).
export const slugify = (value: string): string =>
  value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // strip accents (e.g. L'Huillier → lhuillier)
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
