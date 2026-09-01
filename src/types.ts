// ─────────────────────────────────────────────────────────────
// Library types (library.ts, library.json)
// ─────────────────────────────────────────────────────────────

export interface BookManifestEntry {
  id: string;
  title: string;
  subtitle: string;
  url: string;
  cover: string;
  pages: number;
  style: string;
}

export interface LibraryManifest {
  title: string;
  subtitle: string;
  books: BookManifestEntry[];
}

// ─────────────────────────────────────────────────────────────
// Book viewer types (book.ts, book.json)
// ─────────────────────────────────────────────────────────────

export interface CoverPage {
  type: "cover";
  number: number;
  image: string;
  title: string;
  subtitle: string;
}

export interface ScenePage {
  type: "scene";
  number: number;
  title: string;
  body: string;
  image: string;
  emotion: string;
}

export interface EndingPage {
  type: "ending";
  number: number;
  title: string;
  message: string;
  image: string;
}

export type PageData = CoverPage | ScenePage | EndingPage;

export interface BookData {
  title: string;
  subtitle: string;
  author: string;
  tone: string;
  closingLine: string;
  pages: PageData[];
}