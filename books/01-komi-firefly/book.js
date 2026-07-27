/* 반딧불이 꼬미의 작은 불빛 — 책 뷰어 로직
 * file:// 에서 fetch 가 막힐 수 있어 데이터를 인라인 fallback 으로 내장한다.
 */
(function () {
  "use strict";

  // ---- 인라인 fallback 데이터 (book.json 과 동일 내용) ----
  var INLINE_BOOK = {
    "title": "반딧불이 꼬미의 작은 불빛",
    "subtitle": "가장 작은 빛이 가장 큰 용기가 되었어요",
    "author": "AI 동화 작가",
    "pages": [
      { "type": "cover", "image": "images/cover.png", "title": "반딧불이 꼬미의 작은 불빛", "subtitle": "가장 작은 빛이 가장 큰 용기가 되었어요", "author": "AI 동화 작가" },
      { "type": "scene", "number": 1, "title": "가장 작은 불빛", "body": "여름밤 풀숲에 반딧불이 꼬미가 살았어요. 친구들은 모두 크고 환한 빛을 반짝반짝 냈지만, 꼬미의 불빛은 아주 작았어요. \"내 빛은 왜 이렇게 작을까?\" 꼬미는 풀잎 뒤에 살짝 숨었어요.", "image": "images/scene_01.png", "mood": "쓸쓸함" },
      { "type": "scene", "number": 2, "title": "울고 있는 또박이", "body": "그때 어디선가 훌쩍이는 소리가 들렸어요. 아기 달팽이 또박이가 길을 잃고 울고 있었지요. \"집이 어디인지 하나도 안 보여.\" 캄캄한 밤이 무서웠던 거예요. 꼬미는 조심조심 다가갔어요.", "image": "images/scene_02.png", "mood": "걱정" },
      { "type": "scene", "number": 3, "title": "작은 빛의 길잡이", "body": "\"내가 함께 가 줄게!\" 꼬미가 작은 불빛을 밝혔어요. 큰 빛은 아니었지만, 또박이 바로 앞을 딱 비출 만큼은 되었어요. 한 걸음, 또 한 걸음. 둘은 이슬 젖은 풀숲을 나란히 걸었어요.", "image": "images/scene_03.png", "mood": "다정함" },
      { "type": "scene", "number": 4, "title": "무서운 안개 골짜기", "body": "그런데 갑자기 뽀얀 안개가 스르르 몰려왔어요. 앞이 하나도 보이지 않았어요. \"우리 이제 어떡하지?\" 또박이가 떨었어요. 꼬미도 겁이 났지만 꾹 참았어요.", "image": "images/scene_04.png", "mood": "긴장" },
      { "type": "scene", "number": 5, "title": "반달 할머니의 속삭임", "body": "그때 하늘에서 반달 할머니가 부드럽게 웃었어요. \"꼬미야, 작은 빛도 어둠 속에선 아주 잘 보인단다.\" 꼬미는 용기를 내어 불빛을 더 힘껏 밝혔어요. 그러자 노란 빛이 안개 속에서 별처럼 반짝였어요.", "image": "images/scene_05.png", "mood": "희망" },
      { "type": "scene", "number": 6, "title": "빛을 따라온 친구들", "body": "작은 불빛을 본 다른 반딧불이 친구들이 하나둘 모여들었어요. \"꼬미의 빛을 따라가자!\" 여러 불빛이 모이자 안개 골짜기가 환해졌어요. 또박이는 활짝 웃었지요.", "image": "images/scene_06.png", "mood": "설렘" },
      { "type": "scene", "number": 7, "title": "집으로 가는 길", "body": "빛의 길을 따라 또박이는 드디어 집을 찾았어요. \"고마워, 꼬미야. 네 빛이 나를 지켜 줬어.\" 또박이가 꼬미를 꼭 안아 주었어요. 꼬미의 볼이 발그레해졌어요.", "image": "images/scene_07.png", "mood": "감동" },
      { "type": "scene", "number": 8, "title": "세상에서 가장 소중한 빛", "body": "이제 꼬미는 자기 불빛이 작다고 슬퍼하지 않았어요. \"작은 빛도 누군가에겐 가장 큰 빛이 될 수 있어!\" 반달 할머니와 친구들이 다 함께 반짝반짝 웃었어요. 여름밤 풀숲은 따뜻한 빛으로 가득했답니다.", "image": "images/scene_08.png", "mood": "벅참" },
      { "type": "ending", "message": "네 안에 있는 작은 빛이, 누군가에겐 세상에서 가장 소중한 빛이란다.", "image": "images/scene_08.png" }
    ]
  };

  var book = null;
  var pages = [];
  var current = 0;

  var bookEl = document.getElementById("book");
  var indicatorEl = document.getElementById("indicator");
  var prevBtn = document.getElementById("prev");
  var nextBtn = document.getElementById("next");
  var edgePrev = document.getElementById("edgePrev");
  var edgeNext = document.getElementById("edgeNext");
  var dotsEl = document.getElementById("dots");
  var progressBar = document.getElementById("progressBar");

  // ---------- 유틸 ----------
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function imageOrFallback(src, alt, extraClass) {
    // <img> 로 넣되 onerror 시 placeholder 로 교체
    var cls = extraClass ? ' class="' + extraClass + '"' : "";
    return '<img' + cls + ' src="' + esc(src) + '" alt="' + esc(alt) +
      '" onerror="this.replaceWith(window.__mkFallback());">';
  }

  window.__mkFallback = function () {
    var d = document.createElement("div");
    d.className = "img-fallback";
    d.textContent = "이미지 준비 중…";
    return d;
  };

  // ---------- 페이지 DOM 생성 ----------
  function buildPage(p, idx) {
    var el = document.createElement("section");
    el.className = "page " + p.type;
    el.setAttribute("role", "group");
    el.setAttribute("aria-label", (idx + 1) + "번째 페이지");

    if (p.type === "cover") {
      el.style.backgroundImage = "url('" + p.image + "')";
      el.innerHTML =
        '<div class="cover-text">' +
          '<h1>' + esc(p.title) + '</h1>' +
          (p.subtitle ? '<p class="cover-sub">' + esc(p.subtitle) + '</p>' : '') +
          (p.author ? '<p class="cover-author">글·그림 ' + esc(p.author) + '</p>' : '') +
          '<span class="cover-hint">넘겨서 시작하기 <span aria-hidden="true">▶</span></span>' +
        '</div>';
    } else if (p.type === "scene") {
      el.innerHTML =
        '<div class="scene-img">' +
          imageOrFallback(p.image, (p.title || "장면") + " 삽화") +
        '</div>' +
        '<div class="scene-body">' +
          '<span class="scene-num">Scene ' + (p.number != null ? p.number : idx) + '</span>' +
          '<h2>' + esc(p.title) + '</h2>' +
          '<p>' + esc(p.body) + '</p>' +
        '</div>';
    } else if (p.type === "ending") {
      if (p.image) el.style.backgroundImage = "url('" + p.image + "')";
      el.innerHTML =
        '<div class="ending-inner">' +
          '<div class="ending-mark">— 끝 —</div>' +
          '<p>' + esc(p.message) + '</p>' +
          '<button class="restart-btn" type="button" id="restartBtn">처음부터 다시 보기</button>' +
        '</div>';
    }
    return el;
  }

  // ---------- 렌더 ----------
  function render() {
    bookEl.innerHTML = "";
    pages = book.pages.map(function (p, i) {
      var el = buildPage(p, i);
      bookEl.appendChild(el);
      return el;
    });

    // 점 인디케이터
    dotsEl.innerHTML = "";
    book.pages.forEach(function (p, i) {
      var d = document.createElement("button");
      d.className = "dot";
      d.type = "button";
      d.setAttribute("role", "tab");
      d.setAttribute("aria-label", (i + 1) + " 페이지로 이동");
      d.addEventListener("click", function () { go(i); });
      dotsEl.appendChild(d);
    });

    // 재시작 버튼
    var rb = document.getElementById("restartBtn");
    if (rb) rb.addEventListener("click", function () { go(0); });

    update(true);
  }

  // ---------- 페이지 이동 ----------
  function go(n) {
    n = Math.max(0, Math.min(book.pages.length - 1, n));
    if (n === current) return;
    var prevEl = pages[current];
    if (prevEl) {
      prevEl.classList.add("leaving");
      prevEl.classList.remove("active");
      (function (elem) {
        setTimeout(function () { elem.classList.remove("leaving"); }, 400);
      })(prevEl);
    }
    current = n;
    update(false);
    preload(current);
  }

  function next() { if (current < book.pages.length - 1) go(current + 1); }
  function prev() { if (current > 0) go(current - 1); }

  function update(initial) {
    pages.forEach(function (el, i) {
      if (i === current) el.classList.add("active");
      else if (!el.classList.contains("leaving")) el.classList.remove("active");
    });

    var total = book.pages.length;
    indicatorEl.textContent = (current + 1) + " / " + total;

    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === total - 1;
    edgePrev.disabled = current === 0;
    edgeNext.disabled = current === total - 1;

    progressBar.style.width = ((current + 1) / total * 100) + "%";

    var dots = dotsEl.querySelectorAll(".dot");
    dots.forEach(function (d, i) {
      if (i === current) { d.classList.add("active"); d.setAttribute("aria-selected", "true"); }
      else { d.classList.remove("active"); d.setAttribute("aria-selected", "false"); }
    });

    bookEl.setAttribute("aria-label", book.title + " — " + (current + 1) + " / " + total + " 페이지");
  }

  // ---------- 이미지 프리로드 (현재 ±1) ----------
  function preload(n) {
    [n - 1, n, n + 1, n + 2].forEach(function (i) {
      if (i < 0 || i >= book.pages.length) return;
      var src = book.pages[i].image;
      if (src) { var im = new Image(); im.src = src; }
    });
  }

  // ---------- 이벤트 ----------
  function bindEvents() {
    prevBtn.addEventListener("click", prev);
    nextBtn.addEventListener("click", next);
    edgePrev.addEventListener("click", prev);
    edgeNext.addEventListener("click", next);

    document.addEventListener("keydown", function (e) {
      switch (e.key) {
        case "ArrowLeft": prev(); break;
        case "ArrowRight":
        case " ":
        case "Spacebar": e.preventDefault(); next(); break;
        case "Home": go(0); break;
        case "End": go(book.pages.length - 1); break;
      }
    });

    // 터치 스와이프
    var startX = 0, startY = 0, tracking = false;
    bookEl.addEventListener("touchstart", function (e) {
      var t = e.changedTouches[0];
      startX = t.clientX; startY = t.clientY; tracking = true;
    }, { passive: true });
    bookEl.addEventListener("touchend", function (e) {
      if (!tracking) return;
      tracking = false;
      var t = e.changedTouches[0];
      var dx = t.clientX - startX, dy = t.clientY - startY;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) {
        if (dx < 0) next(); else prev();
      }
    }, { passive: true });
  }

  // ---------- 부트 ----------
  function boot(data) {
    book = data;
    document.title = book.title || "동화책";
    render();
    bindEvents();
    preload(0);
  }

  // book.json 시도 → 실패 시 인라인 fallback
  if (location.protocol === "file:") {
    boot(INLINE_BOOK);
  } else {
    fetch("book.json")
      .then(function (r) { if (!r.ok) throw new Error("no book.json"); return r.json(); })
      .then(function (data) { boot(data); })
      .catch(function () { boot(INLINE_BOOK); });
  }
})();
