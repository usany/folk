/* ============================================================
   꼬마 고슴도치 두리의 첫 밤마실 — 페이지 넘김 로직
   빌드 의존성 없음. book.json 을 fetch 하여 렌더링.
   file:// 로 직접 열어도 동작하도록 fetch 실패 시 폴백 포함.
   ============================================================ */

(function () {
  "use strict";

  var state = { pages: [], index: 0, meta: {} };
  var lastDir = 1;

  var el = {
    track: document.getElementById("page-track"),
    prev: document.getElementById("prev"),
    next: document.getElementById("next"),
    edgePrev: document.getElementById("edge-prev"),
    edgeNext: document.getElementById("edge-next"),
    indicator: document.getElementById("indicator"),
    progressFill: document.getElementById("progress-fill"),
    progress: document.getElementById("progress"),
    pageTitle: document.getElementById("page-title"),
    tocBtn: document.getElementById("toc-btn"),
    tocClose: document.getElementById("toc-close"),
    tocPanel: document.getElementById("toc-panel"),
    tocOverlay: document.getElementById("toc-overlay"),
    tocList: document.getElementById("toc-list"),
    restartBtn: document.getElementById("restart-btn"),
    themeBtn: document.getElementById("theme-btn"),
    book: document.getElementById("book")
  };

  /* ---------- 유틸 ---------- */
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function imageBlock(src, alt) {
    var safeAlt = esc(alt || "동화 삽화");
    // 이미지 로드 실패 시 placeholder 로 대체
    return (
      '<div class="page-image">' +
      '<img src="' + esc(src) + '" alt="' + safeAlt + '" ' +
      "onerror=\"this.onerror=null;this.style.display='none';" +
      "this.parentNode.insertAdjacentHTML('beforeend'," +
      "'<div class=&quot;img-placeholder&quot;>그림 준비 중이에요</div>');\">" +
      "</div>"
    );
  }

  /* ---------- 페이지 렌더링 ---------- */
  function renderPage(page, i) {
    var wrap = document.createElement("section");
    wrap.className = "page " + page.type;
    wrap.setAttribute("role", "group");
    wrap.setAttribute("aria-roledescription", "페이지");
    wrap.setAttribute("aria-label", (i + 1) + " / " + state.pages.length);

    if (page.type === "cover") {
      wrap.innerHTML =
        imageBlock(page.image, page.title + " 표지") +
        '<div class="cover-overlay">' +
        '<h1 class="cover-title">' + esc(page.title) + "</h1>" +
        (page.subtitle ? '<p class="cover-subtitle">' + esc(page.subtitle) + "</p>" : "") +
        (page.author ? '<p class="cover-author">글·그림 · ' + esc(page.author) + "</p>" : "") +
        '<p class="cover-hint">넘겨서 시작하기 →</p>' +
        "</div>";
    } else if (page.type === "ending") {
      wrap.innerHTML =
        imageBlock(page.image, "이야기의 마지막 장면") +
        '<div class="ending-overlay">' +
        '<div class="ending-badge">— 끝 —</div>' +
        '<p class="ending-message">' + esc(page.message) + "</p>" +
        '<button class="restart-cta" type="button" data-action="restart">처음부터 다시 보기 ⟲</button>' +
        "</div>";
    } else {
      wrap.innerHTML =
        imageBlock(page.image, "장면 " + page.number + ": " + page.title) +
        '<div class="page-text">' +
        '<span class="scene-no">장면 ' + esc(page.number) + "</span>" +
        '<h2 class="scene-title">' + esc(page.title) + "</h2>" +
        '<p class="scene-body">' + esc(page.body) + "</p>" +
        (page.mood ? '<span class="scene-mood">✦ ' + esc(page.mood) + "</span>" : "") +
        "</div>";
    }
    return wrap;
  }

  function buildPages() {
    el.track.innerHTML = "";
    state.pages.forEach(function (p, i) {
      el.track.appendChild(renderPage(p, i));
    });
    el.track.querySelectorAll('[data-action="restart"]').forEach(function (b) {
      b.addEventListener("click", function () { goTo(0); });
    });
  }

  /* ---------- 목차 ---------- */
  function pageLabel(p) {
    if (p.type === "cover") return "표지";
    if (p.type === "ending") return "끝";
    return p.title;
  }

  function buildToc() {
    el.tocList.innerHTML = "";
    state.pages.forEach(function (p, i) {
      var li = document.createElement("li");
      li.className = "toc-item";
      li.dataset.index = i;
      var label =
        p.type === "cover" ? "표지" :
        p.type === "ending" ? "이야기의 끝" :
        "장면 " + p.number + ". " + p.title;
      var num = p.type === "scene" ? p.number : (p.type === "cover" ? "★" : "끝");
      li.innerHTML =
        '<span class="toc-num">' + esc(num) + "</span>" +
        '<span class="toc-text">' + esc(label) + "</span>";
      li.addEventListener("click", function () {
        goTo(i);
        closeToc();
      });
      el.tocList.appendChild(li);
    });
  }

  function markTocCurrent() {
    var items = el.tocList.children;
    for (var i = 0; i < items.length; i++) {
      items[i].classList.toggle("current", Number(items[i].dataset.index) === state.index);
    }
  }

  function openToc() {
    el.tocPanel.classList.add("open");
    el.tocPanel.setAttribute("aria-hidden", "false");
    el.tocOverlay.classList.add("show");
  }
  function closeToc() {
    el.tocPanel.classList.remove("open");
    el.tocPanel.setAttribute("aria-hidden", "true");
    el.tocOverlay.classList.remove("show");
  }

  /* ---------- 네비게이션 ---------- */
  function update() {
    var pages = el.track.children;
    for (var i = 0; i < pages.length; i++) {
      var pg = pages[i];
      if (i === state.index) {
        pg.style.setProperty("--enter-x", (lastDir >= 0 ? "40px" : "-40px"));
        pg.classList.add("active");
      } else {
        pg.classList.remove("active");
      }
    }

    var total = state.pages.length;
    el.indicator.textContent = (state.index + 1) + " / " + total;
    var pct = total > 1 ? (state.index / (total - 1)) * 100 : 100;
    el.progressFill.style.width = pct + "%";
    el.progress.setAttribute("aria-valuenow", String(Math.round(pct)));

    el.pageTitle.textContent = pageLabel(state.pages[state.index]);

    el.prev.disabled = state.index === 0;
    el.next.disabled = state.index === total - 1;
    el.edgePrev.disabled = state.index === 0;
    el.edgeNext.disabled = state.index === total - 1;

    markTocCurrent();

    try {
      history.replaceState(null, "", "#p" + (state.index + 1));
    } catch (e) { /* file:// 환경 무시 */ }
  }

  function goTo(i) {
    i = Math.max(0, Math.min(state.pages.length - 1, i));
    if (i === state.index) return;
    lastDir = i > state.index ? 1 : -1;
    state.index = i;
    update();
  }
  function nextPage() { goTo(state.index + 1); }
  function prevPage() { goTo(state.index - 1); }

  /* ---------- 이벤트 바인딩 ---------- */
  function bindEvents() {
    el.next.addEventListener("click", nextPage);
    el.prev.addEventListener("click", prevPage);
    el.edgeNext.addEventListener("click", nextPage);
    el.edgePrev.addEventListener("click", prevPage);

    el.tocBtn.addEventListener("click", openToc);
    el.tocClose.addEventListener("click", closeToc);
    el.tocOverlay.addEventListener("click", closeToc);
    el.restartBtn.addEventListener("click", function () { goTo(0); });
    el.themeBtn.addEventListener("click", toggleTheme);

    document.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") {
        e.preventDefault(); nextPage();
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault(); prevPage();
      } else if (e.key === "Home") {
        e.preventDefault(); goTo(0);
      } else if (e.key === "End") {
        e.preventDefault(); goTo(state.pages.length - 1);
      } else if (e.key === "Escape") {
        closeToc();
      }
    });

    // 터치 스와이프
    var sx = 0, sy = 0, tracking = false;
    el.book.addEventListener("touchstart", function (e) {
      if (e.touches.length !== 1) return;
      sx = e.touches[0].clientX; sy = e.touches[0].clientY; tracking = true;
    }, { passive: true });
    el.book.addEventListener("touchend", function (e) {
      if (!tracking) return;
      tracking = false;
      var t = e.changedTouches[0];
      var dx = t.clientX - sx, dy = t.clientY - sy;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
        if (dx < 0) nextPage(); else prevPage();
      }
    }, { passive: true });
  }

  /* ---------- 테마 ---------- */
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    el.themeBtn.textContent = theme === "light" ? "☀️" : "🌙";
    el.themeBtn.setAttribute("title", theme === "light" ? "어둡게" : "밝게");
    try { localStorage.setItem("duri-theme", theme); } catch (e) {}
  }
  function toggleTheme() {
    var cur = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
    applyTheme(cur === "light" ? "dark" : "light");
  }
  function initTheme() {
    var saved = null;
    try { saved = localStorage.getItem("duri-theme"); } catch (e) {}
    if (!saved) {
      saved = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches
        ? "light" : "dark";
    }
    applyTheme(saved);
  }

  /* ---------- 초기화 ---------- */
  function start(data) {
    state.meta = data;
    state.pages = data.pages || [];
    document.title = data.title || document.title;

    buildPages();
    buildToc();
    bindEvents();
    initTheme();

    // URL 해시로 시작 페이지 복원
    var m = /^#p(\d+)$/.exec(location.hash);
    if (m) {
      var n = parseInt(m[1], 10) - 1;
      if (n >= 0 && n < state.pages.length) state.index = n;
    }
    update();
    el.book.focus();
  }

  // book.json 을 우선 fetch. file:// 등으로 실패하면 인라인 폴백 사용.
  fetch("book.json")
    .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(start)
    .catch(function () {
      if (window.BOOK_DATA) {
        start(window.BOOK_DATA);
      } else {
        el.track.innerHTML =
          '<section class="page scene active"><div class="page-text">' +
          '<h2 class="scene-title">책을 불러오지 못했어요</h2>' +
          '<p class="scene-body">로컬 파일(file://)에서 직접 열면 브라우저 보안 정책 때문에 ' +
          'book.json 을 읽지 못할 수 있어요. 간단한 로컬 서버로 열어주세요.<br><br>' +
          '예) 이 폴더에서 <b>python3 -m http.server</b> 실행 후 ' +
          'http://localhost:8000 접속.</p></div></section>';
      }
    });
})();
