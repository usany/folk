import type { BookManifestEntry, LibraryManifest } from "./src/types.js";

// ─────────────────────────────────────────────────────────────
// Fallback manifest (used when library.json fetch fails)
// ─────────────────────────────────────────────────────────────

const FALLBACK_MANIFEST: LibraryManifest = {
  title: "달빛 도서관",
  subtitle: "AI가 그린 동화책 모음",
  books: [
    {
      id: "01-rabbit-tale",
      title: "토끼가 들려주는 토끼와 거북이",
      subtitle: "우리가 몰랐던 토끼와 거북이 이야기의 숨겨진 진실",
      url: "./books/01-rabbit-tale/index.html",
      cover: "./books/01-rabbit-tale/images/cover.png",
      pages: 12,
      style: "dark satire",
    },
  ],
};

// ─────────────────────────────────────────────────────────────
// Load manifest from JSON (or fallback)
// ─────────────────────────────────────────────────────────────

async function loadLibrary(): Promise<LibraryManifest> {
  try {
    const response = await fetch("./books/library.json");
    if (!response.ok) throw new Error("Failed to load manifest");
    return (await response.json()) as LibraryManifest;
  } catch (error: unknown) {
    console.warn("Using fallback manifest:", error);
    return FALLBACK_MANIFEST;
  }
}

// ─────────────────────────────────────────────────────────────
// Render book grid
// ─────────────────────────────────────────────────────────────

function renderBooks(manifest: LibraryManifest): void {
  const grid = document.getElementById("book-grid") as HTMLElement | null;
  if (!grid) return;

  if (!manifest.books || manifest.books.length === 0) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1;">
        <h2>아직 책이 없습니다</h2>
        <p>동화책을 추가하면 여기에 표시됩니다.</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = manifest.books
    .map((book) => createBookCard(book))
    .join("");
}

function createBookCard(book: BookManifestEntry): string {
  const coverUrl = book.cover || "./placeholder.png";
  const pageCount = book.pages ? `${book.pages}p` : "📖";
  const style = book.style
    ? `<span class="badge">${escapeHtml(book.style)}</span>`
    : "";

  return `
    <a class="book-card" href="${escapeHtml(book.url)}" tabindex="0">
      <div class="card-cover" style="background-image:url('${escapeHtml(coverUrl)}')"></div>
      <div class="card-info">
        <h2>${escapeHtml(book.title)}</h2>
        <p class="card-subtitle">${escapeHtml(book.subtitle || "")}</p>
        <div class="card-meta">
          <span class="badge">${pageCount}</span>
          ${style}
        </div>
      </div>
    </a>
  `;
}

function escapeHtml(text: string): string {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// ─────────────────────────────────────────────────────────────
// Initialize on DOM ready
// ─────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", async () => {
  const manifest = await loadLibrary();
  renderBooks(manifest);
});