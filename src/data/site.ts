// Chapter registry — mirrors main.tex's \include order.
// Titles, descriptions, and leads are verbatim from the proposal
// (including "Accomodation").
export interface Chapter {
  num: number;
  id: string; // page route + sidebar link
  title: string;
  /** Meta description used by Layout (also feeds og:description). */
  description: string;
  /** Optional lead paragraph shown under the chapter title (ChapterHead). */
  lead?: string;
}

export const chapters: Chapter[] = [
  {
    num: 1,
    id: 'introduction',
    title: 'Introduction',
    description:
      'The Italian Association of Physics Students (AISF): who we are and the activities of TC Italy, host of ICPS 2028.',
  },
  {
    num: 2,
    id: 'organizing-committee',
    title: 'Organizing Committee',
    description:
      'The ICPS 2028 Organizing Committee — 28 students from universities across Italy, structured into seven teams.',
    lead: 'The Organizing Committee currently consists of 28 students from universities across Italy, bringing together diverse academic backgrounds, physics field knowledge, and regional representation. Each member has already contributed to previous AISF events, committed to other scientific engagement, or both.',
  },
  {
    num: 3,
    id: 'italy',
    title: 'A few words about Italy',
    description: 'The host cities of ICPS 2028 — a few words about Italy, Torino, and Milano.',
    lead: 'Located in Southern Europe, Italy shares borders with France, Switzerland, Austria, and Slovenia, while its central position in the Mediterranean Sea makes it easily accessible from Europe, North Africa, and West Asia. This strategic location has made Italy a crossroads of different cultures, ideas, trade, and scientific exchange for centuries. Every Italian region bears its own unique history and culture, enriched by the diverse peoples who have crossed it. This intricate web of different legacies ultimately gives rise to a feeling of complex uniqueness, characterizing every possible location on the Italian map.',
  },
  {
    num: 4,
    id: 'getting-there',
    title: 'How do I get there?',
    description:
      'How to reach Torino and Milano — by plane, train, bus, and car, plus visa requirements.',
  },
  {
    num: 5,
    id: 'food-accomodation',
    title: 'Food & Accomodation',
    description:
      'Food and accommodation for ICPS 2028: programs, venues, and menus in Milano and Torino.',
  },
  {
    num: 6,
    id: 'scientific-program',
    title: 'Scientific program',
    description:
      'The scientific program of ICPS 2028 — thematic tracks and keynote speakers, roundtable discussions, workshops, scientific lab visits and student contributions across Torino and Milano.',
    lead: 'The scientific program of the conference is designed as a journey through the core questions of modern physics. Moving beyond the boundaries of isolated subfields, the program encourages an intellectual journey where the laws of the subatomic world, the patterns of complexity, and the architecture of the cosmos continuously echo and challenge one another.',
  },
  {
    num: 7,
    id: 'social-program',
    title: 'Social program',
    description:
      'The ICPS 2028 social program: opening ceremony, excursion day, Milano treasure hunt, FantaICPS, Nations Party and unforgettable evenings in Milano and Torino.',
    lead: 'If the scientific program has already sparked your curiosity, just wait until you discover what we have prepared for the Social Program!',
  },
  {
    num: 8,
    id: 'transportation',
    title: 'Transportation',
    description:
      'Sustainability and mobility strategy for ICPS 2028: public transport in Milano and Torino and the transfer between the two host cities.',
    lead: "The Organizing Committee is fully committed to minimizing the environmental impact of ICPS 2028 and maximizing the event's sustainability. Consequently, the utilization of Public Transport (TPL - Trasporto Pubblico Locale) is heavily encouraged and considered as the primary mode of transportation throughout the conference. All participants are strongly advised to use public transportation for their journeys to and from airports, as well as for all daily urban movements. The Organizing Committee will provide them with multi-day passes. The use of private charter buses will be treated strictly as an exception, limited only to specific instances where reaching research laboratories or excursion venues via public transportation is impossible.",
  },
  {
    num: 9,
    id: 'internal-communication',
    title: 'Internal communication',
    description:
      'How ICPS 2028 will keep participants informed and connected: newsletters, the conference handbook and digital platform, internet access, phone connections, accessibility and inclusion measures, and medical emergencies.',
  },
  {
    num: 10,
    id: 'pr-socials',
    title: 'PR & Socials',
    description:
      'PR and socials strategy for ICPS 2028: values and mission statement, visual identity, editorial line and social engagement, communication offices and media connections, and legal and privacy considerations.',
  },
  {
    num: 11,
    id: 'finance',
    title: 'Finance',
    description: 'ICPS 2028 project proposal — Finance chapter.',
    lead: 'To ensure a comprehensive and resilient financial overview for ICPS28, the following section outlines our financial planning structured across two distinct attendance scenarios: a 500 participants model and a 400 participants model.',
  },
  {
    num: 12,
    id: 'sponsorships',
    title: 'Sponsorship strategy',
    description: 'ICPS 2028 project proposal — Sponsorship strategy chapter.',
  },
  {
    num: 13,
    id: 'conclusions',
    title: 'Conclusions',
    description: 'ICPS 2028 project proposal — Conclusions chapter.',
    lead: 'Throughout this proposal, we have presented a conference designed around complementary scientific themes, enriched by interactive formats and a social program celebrating the cultural heritage of the two cities it would be hosted by. Every aspect of the conference has been conceived to encourage interaction and strengthen the international network that makes IAPS such a unique organization.',
  },
];
