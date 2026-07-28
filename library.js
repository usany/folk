// Fallback library data in case JSON fetch fails
const fallbackLibrary = {
  library: {
    title: "달빛 도서관",
    tagline: "AI가 그린 동화책 모음",
    github: "https://github.com/revfactory/fairy-tale-moonlight-library"
  },
  books: []
};

async function initializeLibrary() {
  try {
    const response = await fetch('books/library.json');
    if (!response.ok) throw new Error('Failed to load library.json');
    return await response.json();
  } catch (error) {
    console.warn('Could not load library.json, using fallback:', error);
    return fallbackLibrary;
  }
}

function createBookCard(book) {
  const card = document.createElement('a');
  card.className = 'book-card';
  card.href = book.url;
  card.title = book.title;

  const cover = document.createElement('div');
  cover.className = 'card-cover';
  cover.style.backgroundImage = `url('${book.cover}')`;

  // Add placeholder class and error handling
  const img = new Image();
  img.onerror = () => {
    cover.classList.add('placeholder');
    cover.textContent = '📖';
  };
  img.src = book.cover;

  const info = document.createElement('div');
  info.className = 'card-info';

  const title = document.createElement('h2');
  title.textContent = book.title;

  const subtitle = document.createElement('p');
  subtitle.className = 'card-subtitle';
  subtitle.textContent = book.subtitle;

  const meta = document.createElement('div');
  meta.className = 'card-meta';

  const pagesBadge = document.createElement('span');
  pagesBadge.className = 'badge';
  pagesBadge.textContent = `${book.pages}p`;

  const styleBadge = document.createElement('span');
  styleBadge.className = 'badge';
  styleBadge.textContent = book.style;

  meta.appendChild(pagesBadge);
  meta.appendChild(styleBadge);

  info.appendChild(title);
  info.appendChild(subtitle);
  info.appendChild(meta);

  card.appendChild(cover);
  card.appendChild(info);

  return card;
}

async function renderLibrary() {
  const data = await initializeLibrary();
  const bookGrid = document.getElementById('book-grid');
  const emptyState = document.getElementById('empty-state');

  // Update page metadata
  const siteTitle = document.getElementById('site-title');
  const tagline = document.getElementById('tagline');
  const githubLink = document.getElementById('github-link');

  if (siteTitle) siteTitle.textContent = data.library.title;
  if (tagline) tagline.textContent = data.library.tagline;
  if (githubLink) githubLink.href = data.library.github;

  // Render books
  if (data.books && data.books.length > 0) {
    bookGrid.innerHTML = '';
    data.books.forEach(book => {
      const card = createBookCard(book);
      bookGrid.appendChild(card);
    });
    emptyState.style.display = 'none';
  } else {
    bookGrid.innerHTML = '';
    emptyState.style.display = 'block';
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', renderLibrary);
