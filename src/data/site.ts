// Chapter registry — mirrors main.tex's \include order.
// Titles are verbatim from the proposal (including "Accomodation").
export interface Chapter {
  num: number;
  id: string; // page route + sidebar link
  title: string;
}

export const chapters: Chapter[] = [
  { num: 1, id: 'introduction', title: 'Introduction' },
  { num: 2, id: 'organizing-committee', title: 'Organizing Committee' },
  { num: 3, id: 'italy', title: 'A few words about Italy' },
  { num: 4, id: 'getting-there', title: 'How do I get there?' },
  { num: 5, id: 'food-accomodation', title: 'Food & Accomodation' },
  { num: 6, id: 'scientific-program', title: 'Scientific program' },
  { num: 7, id: 'social-program', title: 'Social program' },
  { num: 8, id: 'transportation', title: 'Transportation' },
  { num: 9, id: 'internal-communication', title: 'Internal communication' },
  { num: 10, id: 'pr-socials', title: 'PR & Socials' },
  { num: 11, id: 'finance', title: 'Finance' },
  { num: 12, id: 'sponsorships', title: 'Sponsorship strategy' },
  { num: 13, id: 'conclusions', title: 'Conclusions' },
];
