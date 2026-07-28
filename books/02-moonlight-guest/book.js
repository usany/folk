/* 달빛 손님 루나와 토끼 몽이 — 책 뷰어 로직 */
(function () {
  "use strict";

  var INLINE_BOOK = {
    "title": "달빛 손님 루나와 토끼 몽이",
    "subtitle": "웃는 법을 잊은 달 정령 이야기",
    "author": "AI 동화 작가",
    "pages": [
      { "type": "cover", "image": "images/cover.png", "title": "달빛 손님 루나와 토끼 몽이", "subtitle": "웃는 법을 잊은 달 정령 이야기", "author": "AI 동화 작가" },
      { "type": "scene", "number": 1, "title": "잠이 오지 않는 밤", "body": "달맞이꽃 언덕에 사는 아기 토끼 몽이는 밤이 제일 좋았어요. 다른 토끼들이 모두 잠든 시간, 몽이는 살금살금 창문을 열고 밖을 내다보았지요.\n\n\"오늘 밤은 달님이 참 크네.\"\n노란 방울이 딸랑, 하고 작게 울렸어요. 몽이는 접힌 귀를 쫑긋 세우고 언덕을 바라보았어요.", "image": "images/scene_01.png", "mood": "따뜻한" },
      { "type": "scene", "number": 2, "title": "떨어진 달빛 한 조각", "body": "그때 하늘에서 무언가 반짝, 하고 떨어졌어요. 은빛 조각이 나비처럼 살랑살랑 내려와 달맞이꽃 위에 앉았지요.\n\n몽이는 눈을 동그랗게 떴어요. 별도 아니고, 눈도 아니었어요. 조각은 숨을 쉬듯이 천천히 밝아졌다가, 다시 어두워졌어요.", "image": "images/scene_02.png", "mood": "신비로운" },
      { "type": "scene", "number": 3, "title": "폴짝, 언덕을 올라", "body": "몽이는 바구니를 메고 문밖으로 폴짝 뛰어나갔어요. 이슬에 젖은 풀이 발바닥을 간지럽혔어요.\n\n폴짝, 폴짝, 폴짝. 언덕길을 오를 때마다 방울이 딸랑딸랑 울렸어요. 은빛 조각은 몽이를 기다리는 것처럼 천천히 언덕 위로 올라갔지요.", "image": "images/scene_03.png", "mood": "설레는" },
      { "type": "scene", "number": 4, "title": "웃는 법을 모르는 아이", "body": "언덕 위에는 은빛 아이가 앉아 있었어요. 머리카락에서 별가루가 흩날리고, 발은 땅에 닿지 않았어요.\n\n\"나는 루나야. 달에서 왔어.\"\n루나의 목소리는 종소리처럼 맑았지만, 얼굴에는 아무 표정도 없었어요.\n\"몽이야, 나는… 웃는 법을 몰라. 달에서는 아무도 웃지 않아.\"", "image": "images/scene_04.png", "mood": "놀라운" },
      { "type": "scene", "number": 5, "title": "희미해지는 빛", "body": "이야기를 나누는 동안, 루나의 빛이 조금씩 흐려졌어요. 손끝이 안개처럼 옅어졌지요.\n\n\"기쁨이 없으면 달로 돌아가는 길이 보이지 않아.\"\n루나는 텅 빈 하늘을 올려다보았어요. 은빛 길이 있어야 할 자리에 아무것도 없었어요. 몽이는 두 주먹을 꼭 쥐었어요.", "image": "images/scene_05.png", "mood": "긴장된" },
      { "type": "scene", "number": 6, "title": "몽이의 작은 선물들", "body": "몽이는 바구니를 열었어요. 폭신한 담요를 루나의 어깨에 덮어 주고, 제일 아끼던 당근 쿠키를 반으로 쪼개 나누어 주었지요.\n\n그리고 두 손을 모아 불렀어요. \"반딧불 친구들아, 도와줘!\"\n풀숲에서 반딧불이 열두 마리가 폴폴 날아와 루나의 머리 위에서 동그란 왕관처럼 반짝였어요. 루나의 입꼬리가… 아주 조금, 위로 올라갔어요.", "image": "images/scene_06.png", "mood": "감동적인" },
      { "type": "scene", "number": 7, "title": "웃음이 만든 은빛 길", "body": "루나가 처음으로 소리 내어 웃었어요. \"까르르!\"\n웃음소리가 퍼질 때마다 루나의 몸에서 빛이 쏟아졌어요. 언덕의 달맞이꽃이 모두 활짝 피어났지요.\n\n그리고 하늘에 은빛 길이 반짝, 열렸어요. 달까지 이어지는 반짝이는 계단이었어요.", "image": "images/scene_07.png", "mood": "환희의" },
      { "type": "scene", "number": 8, "title": "매일 밤, 딸랑", "body": "\"몽이야, 고마워. 이제 웃는 법을 알아.\"\n루나는 몽이의 목도리에 작은 달빛 방울 하나를 걸어 주고 은빛 계단을 올라갔어요.\n\n그날부터 몽이의 방울은 밤마다 저 혼자 딸랑, 딸랑 울렸어요. 창밖을 보면 달님이 살짝 웃고 있었지요. 몽이도 이불 속에서 마주 웃었어요.", "image": "images/scene_08.png", "mood": "평온한" },
      { "type": "ending", "message": "작은 친절 하나가 누군가의 밤을 환하게 밝혀 줄 수 있어요. 오늘 밤, 달님에게 먼저 웃어 볼까요?", "image": "images/scene_08.png" }
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

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function imageOrFallback(src, alt, extraClass) {
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

  function render() {
    bookEl.innerHTML = "";
    pages = book.pages.map(function (p, i) {
      var el = buildPage(p, i);
      bookEl.appendChild(el);
      return el;
    });

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

    var rb = document.getElementById("restartBtn");
    if (rb) rb.addEventListener("click", function () { go(0); });

    update(true);
  }

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

  function preload(n) {
    [n - 1, n, n + 1, n + 2].forEach(function (i) {
      if (i < 0 || i >= book.pages.length) return;
      var src = book.pages[i].image;
      if (src) { var im = new Image(); im.src = src; }
    });
  }

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

  function boot(data) {
    book = data;
    document.title = book.title || "동화책";
    render();
    bindEvents();
    preload(0);
  }

  if (location.protocol === "file:") {
    boot(INLINE_BOOK);
  } else {
    fetch("book.json")
      .then(function (r) { if (!r.ok) throw new Error("no book.json"); return r.json(); })
      .then(function (data) { boot(data); })
      .catch(function () { boot(INLINE_BOOK); });
  }
})();
