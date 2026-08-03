let currentPage = 0;
let bookData = null;
let currentAudio = null;
let autoAdvance = true;
let autoPlayNext = false;

// Inline fallback data if fetch fails
const fallbackData = {
  "title": "토끼가 들려주는 토끼와 거북이",
  "subtitle": "우리가 몰랐던 토끼와 거북이 이야기의 숨겨진 진실",
  "author": "토끼 (1인칭 증언)",
  "tone": "dark satire, unreliable-narrator testimony",
  "closingLine": "네가 알고 있는 그 이야기 진실이니?",
  "pages": [
    {"type":"cover","number":0,"image":"images/cover.png","title":"토끼가 들려주는 토끼와 거북이","subtitle":"우리가 몰랐던 토끼와 거북이 이야기의 숨겨진 진실"},
    {"type":"scene","number":1,"title":"말을 거는 토끼","body":"저기 실례지만 내 이야기 좀 들어봐. 어쩌면 너는 이미 나에 대해서 들어봤을지 몰라. 내가 살고 있는 이 마을은 토끼와 거북이가 달리기 시합을 한 것으로 유명해. 내가 바로 그 유명한 토끼지. 하지만 네가 알고있는 이야기, 그거 사실이 아니야.","image":"images/scene_01.png","emotion":"조심스러운 호소, 은밀함"},
    {"type":"scene","number":2,"title":"토끼를 찾아온 깡패 거북이 무리","body":"내가 살고 있는 이 곳에는 마을 동물들이라면 누구나 아는 깡패 거북이 무리가 있어. 이들은 마을을 엉망으로 만들고 다니지. 마을 동물들 누구나 깡패 거북이 무리를 피해다녀. 얼마 전에 그 깡패 거북이 무리가 나를 찾아왔어.","image":"images/scene_02.png.jpg","emotion":"위협, 압도"},
    {"type":"scene","number":3,"title":"두목 거북이의 달리기 시합 협박","body":"\"어이 토끼. 나랑 달리기 시합 한번 하자. 거절하면 귀를 뜯어버릴거야.\"라고 두목 거북이가 말했지. 달리기 시합 제안이라기보다는 사실상 협박이었어. 너라면 거절할 수 있을 것 같아? 어쩔 수 없이 떨면서 \"알겠어요.\"라고 답했지.","image":"images/scene_03.png","emotion":"공포, 굴복"},
    {"type":"scene","number":4,"title":"운명의 날","body":"두목 거북이가 나오라는 날짜에 마을 언덕 아래에 나왔어. 한참을 있다가 \"형님 오셨습니까.\"라는 부하 거북이 무리의 우렁찬 목소리와 함께 두목 거북이도 등장했지. 경주 코스는 간단했어. 언덕을 올라가 나무를 반환점으로 돌아서 출발 장소로 다시 내려오면 도착.","image":"images/scene_04.png","emotion":"의식화된 위압, 고립"},
    {"type":"scene","number":5,"title":"시작된 달리기 시합","body":"카운트다운과 함께 달리기 시합이 시작됐어. 나는 빨리 경주를 끝내고 깡패 거북이 무리로부터 해방되고 싶어 처음부터 전속력으로 달렸어. 언덕을 한참 올라가는데 혼자 달리고 있는 기분이 들었어. 뒤를 돌아보니 두목 거북이는 여전히 출발선 근처에 있었지.","image":"images/scene_05.png","emotion":"필사적 질주, 불길한 위화감"},
    {"type":"scene","number":6,"title":"토끼의 기절","body":"반환점인 언덕 위 나무를 도는데 내 뒷덜미를 누군가 잡았어. 어쩌면 출발선에서 보이지 않았던 다른 부하 거북이들이 나무 뒤에 있었던 거야. 내 뒷덜미를 잡고는 \"지금 장난하냐?\"라고 말하곤 갑자기 나를 때리기 시작했지. 얼마나 맞았을까 그 충격에 나는 기절을 했어.","image":"images/scene_06.png","emotion":"매복, 충격"},
    {"type":"scene","number":7,"title":"두목 거북이의 우승","body":"깨어나니 나는 언덕 나무 아래에 버려져 있었어. 경주는 두목 거북이의 우승으로 이미 끝나 있었지. 달리기 시합을 멀리서 지켜본 마을 동물들에 의하면 내가 기절해 있는 동안 두목 거북이가 언덕을 올라 반환점을 돌고 내려갔대. \"역시 대단하십니다\"라며 아부하는 부하 거북이들의 헹가래까지 우승 세레모니로 받았다고 하더군.","image":"images/scene_07.png.jpg","emotion":"버려짐, 잔인한 대비"},
    {"type":"scene","number":8,"title":"마을 서점","body":"두목 거북이와의 달리기 사건 이후에 남은 건 상처뿐이었지만 나는 이것을 잊기 위해 계속 노력했어. \"아 내가 재수가 없었구나. 좋은 날이 오겠지.\"하고 말이야. 그런데 어느날 우연히 마을 서점에 갔다가 깜짝 놀랐어.","image":"images/scene_08.png.jpg","emotion":"일상 속 불시의 충격"},
    {"type":"scene","number":9,"title":"두목 거북이의 자서전","body":"베스트셀러 목록에 두목 거북이가 쓴 자서전이 있었어. 제목은 '토끼와 거북이'. 너희가 지금까지 알던 내용이 담긴 책이었지. 성실한 거북이가 게으른 토끼를 경주에서 이긴 바로 그 이야기 말이야.","image":"images/scene_09.png","emotion":"압도적 배신감"},
    {"type":"scene","number":10,"title":"거짓된 자서전의 내용","body":"모든 내용이 거짓이었어. 언덕 위에서 부하 거북이들에게 맞아 기절한 진실은 없애고 거북이를 얕보며 낮잠을 자다 노력파 거북이에게 경주에서 진 것처럼 꾸며져 있었지. 깡패 거북이 무리에게 당한 것도 억울한데 나는 한순간에 세상의 비웃음거리가 되었어.","image":"images/scene_10.png","emotion":"조작된 진실, 조롱"},
    {"type":"scene","number":11,"title":"토끼의 억울함","body":"우리 마을의 동물들은 깡패 거북이 무리가 두려워 무엇이 진실이 알면서도 모른채하고 있어. 나도 깡패 거북이 무리가 나를 다시 찾아올까봐 숨어있지만 내 억울함을 알리고 싶어. 너희라도 내가 피해자인 이 진실을 꼭 알아줘!","image":"images/scene_11.png","emotion":"간절한 호소, 고립된 진실"},
    {"type":"ending","number":12,"title":"끝","message":"네가 알고 있는 그 이야기 진실이니?","image":"images/scene_11.png"}
  ]
};

function setupAudioManager() {
  const audioContainer = document.createElement('div');
  audioContainer.id = 'audio-manager';
  audioContainer.style.display = 'none';
  document.body.appendChild(audioContainer);
  return audioContainer;
}

const audioManager = setupAudioManager();

function toggleAudio(audio, button, status) {
  if (audio.paused) {
    audio.play().catch(err => {
      status.textContent = '(재생 실패)';
      status.style.color = '#e74c3c';
    });
  } else {
    audio.pause();
  }
}

function setupAudioElement(audioFile) {
  let audio = audioManager.querySelector('audio');
  if (!audio) {
    audio = document.createElement('audio');
    audioManager.appendChild(audio);
  }
  audio.src = audioFile;
  return audio;
}

async function loadBook() {
  try {
    const response = await fetch('book.json');
    if (!response.ok) throw new Error('Failed to fetch');
    bookData = await response.json();
  } catch (error) {
    console.log('Using fallback data:', error.message);
    bookData = fallbackData;
  }
  render();
  setupDots();
}

function render() {
  const book = document.getElementById('book');
  book.innerHTML = '';

  const page = bookData.pages[currentPage];
  const pageEl = document.createElement('div');
  pageEl.className = `page ${page.type} active`;

  if (page.type === 'cover') {
    pageEl.innerHTML = `
      <div class="cover-content">
        <h1>${page.title}</h1>
        <p class="subtitle">${page.subtitle}</p>
        <button class="cover-play-btn" id="coverPlayBtn">🎧 제목 듣고 시작하기</button>
      </div>
    `;

    setTimeout(() => {
      const coverPlayBtn = document.getElementById('coverPlayBtn');
      if (coverPlayBtn) {
        coverPlayBtn.onclick = () => {
          const coverAudio = setupAudioElement('audio/cover_speech.mp3');

          // Clear any previous listeners
          coverAudio.onended = null;
          coverAudio.onerror = null;

          // Update button state during playback
          coverAudio.onplay = () => {
            coverPlayBtn.textContent = '⏸ 재생 중...';
            coverPlayBtn.disabled = true;
          };

          coverAudio.onpause = () => {
            coverPlayBtn.textContent = '🎧 제목 듣고 시작하기';
            coverPlayBtn.disabled = false;
          };

          // Chain to first scene audio when cover speech ends
          coverAudio.onended = () => {
            const firstSceneIndex = bookData.pages.findIndex(p => p.type === 'scene');
            if (firstSceneIndex !== -1) {
              currentPage = firstSceneIndex;
              render();

              // Wait for page to render, then auto-play first scene audio
              setTimeout(() => {
                const playBtn = document.getElementById('playBtn');
                if (playBtn) {
                  playBtn.click();
                }
              }, 100);
            }
          };

          // Error handling
          coverAudio.onerror = () => {
            coverPlayBtn.textContent = '🎧 제목 듣고 시작하기';
            coverPlayBtn.disabled = false;
            // Still advance to first scene on error
            const firstSceneIndex = bookData.pages.findIndex(p => p.type === 'scene');
            if (firstSceneIndex !== -1) {
              currentPage = firstSceneIndex;
              render();
            }
          };

          // Start playback
          coverAudio.play().catch(err => {
            console.error('Failed to play cover speech:', err);
            // Fallback: advance anyway
            const firstSceneIndex = bookData.pages.findIndex(p => p.type === 'scene');
            if (firstSceneIndex !== -1) {
              currentPage = firstSceneIndex;
              render();
            }
          });
        };
      }
    }, 0);
  } else if (page.type === 'scene') {
    const audioFile = `audio/page_${String(page.number).padStart(2, '0')}.mp3`;

    // Split text into words for highlighting
    const words = page.body.split(/(\s+)/);
    const highlightedBody = words.map((word, i) => {
      if (word.trim()) {
        return `<span class="word" data-index="${Math.floor(i/2)}">${word}</span>`;
      }
      return word;
    }).join('');

    pageEl.innerHTML = `
      <div class="scene-image">
        <img src="${page.image}" alt="${page.title}" loading="lazy">
      </div>
      <div class="scene-text">
        <h2 class="scene-title">${page.title}</h2>
        <div class="audio-controls">
          <button class="play-button" id="playBtn" aria-label="재생">🔊 읽어주기</button>
          <span class="audio-status" id="audioStatus"></span>
        </div>
        <p class="scene-body" id="sceneBody">${highlightedBody}</p>
        <div class="scene-emotion">${page.emotion}</div>
      </div>
    `;

    setTimeout(() => {
      const playBtn = document.getElementById('playBtn');
      const status = document.getElementById('audioStatus');
      const sceneBody = document.getElementById('sceneBody');
      const audio = setupAudioElement(audioFile);

      if (playBtn && audio) {
        playBtn.onclick = () => toggleAudio(audio, playBtn, status);

        // Click on words to rewind speech
        if (sceneBody) {
          const words = sceneBody.querySelectorAll('.word');
          words.forEach(word => {
            word.style.cursor = 'pointer';
            word.onclick = (e) => {
              e.stopPropagation();
              if (!audio.paused || audio.duration) {
                const wordIndex = parseInt(word.getAttribute('data-index'));
                const progress = wordIndex / (words.length - 1 || 1);
                const seekTime = Math.max(0, progress * audio.duration);
                audio.currentTime = seekTime;
                if (audio.paused) {
                  audio.play();
                }
              }
            };
          });
        }

        // Clean all old listeners
        audio.onplay = null;
        audio.onpause = null;
        audio.onended = null;
        audio.onerror = null;

        audio.onplay = () => {
          playBtn.textContent = '⏸ 중지';
          if (currentAudio && currentAudio !== audio) {
            currentAudio.pause();
          }
          currentAudio = audio;
        };

        audio.onpause = () => {
          playBtn.textContent = '🔊 읽어주기';
        };

        audio.ontimeupdate = () => {
          const sceneBody = document.getElementById('sceneBody');
          if (sceneBody && audio.duration) {
            const progress = audio.currentTime / audio.duration;
            const words = sceneBody.querySelectorAll('.word');
            const currentWordIndex = Math.floor(progress * words.length);

            words.forEach((word, index) => {
              word.classList.toggle('active', index < currentWordIndex);
            });
          }
        };

        audio.onended = () => {
          playBtn.textContent = '🔊 읽어주기';
          playBtn.style.visibility = 'hidden';
          if (autoAdvance && currentPage < bookData.pages.length - 1) {
            autoPlayNext = true;
            setTimeout(() => nextPage(), 1000);
          }
        };

        audio.onerror = () => {
          status.textContent = '(오디오 파일 없음)';
          status.style.color = '#999';
          playBtn.disabled = true;
          playBtn.style.opacity = '0.5';
        };

        // Auto-play if we came from the previous page's audio ending
        if (autoPlayNext) {
          setTimeout(() => {
            audio.play().catch(() => {
              autoPlayNext = false;
            });
            autoPlayNext = false;
          }, 100);
        }
      }
    }, 0);
  } else if (page.type === 'ending') {
    pageEl.innerHTML = `
      <div class="ending-content">
        <div class="ending-message">${page.message}</div>
      </div>
    `;
  }

  book.appendChild(pageEl);
  updateControls();
}

function updateControls() {
  const totalPages = bookData.pages.length;
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const indicator = document.getElementById('indicator');

  prevBtn.disabled = currentPage === 0;
  nextBtn.disabled = currentPage === totalPages - 1;
  indicator.textContent = `${currentPage + 1} / ${totalPages}`;

  updateDots();
}

function setupDots() {
  const dotsContainer = document.getElementById('dots');
  const totalPages = bookData.pages.length;

  for (let i = 0; i < totalPages; i++) {
    const dot = document.createElement('div');
    dot.className = 'dot';
    if (i === currentPage) dot.classList.add('active');
    dot.addEventListener('click', () => {
      currentPage = i;
      render();
    });
    dotsContainer.appendChild(dot);
  }
}

function updateDots() {
  const dots = document.querySelectorAll('.dot');
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === currentPage);
  });
}

function goToPage(n) {
  const totalPages = bookData.pages.length;
  if (n >= 0 && n < totalPages) {
    currentPage = n;
    render();
  }
}

function nextPage() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
  goToPage(currentPage + 1);
}

function prevPage() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
  goToPage(currentPage - 1);
}

document.getElementById('next').addEventListener('click', nextPage);
document.getElementById('prev').addEventListener('click', prevPage);

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') {
    e.preventDefault();
    nextPage();
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault();
    prevPage();
  } else if (e.key === 'Home') {
    e.preventDefault();
    goToPage(0);
  } else if (e.key === 'End') {
    e.preventDefault();
    goToPage(bookData.pages.length - 1);
  }
});

let touchStartX = 0;
document.getElementById('book').addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
});

document.getElementById('book').addEventListener('touchend', (e) => {
  const touchEndX = e.changedTouches[0].clientX;
  if (touchStartX - touchEndX > 50) nextPage();
  if (touchEndX - touchStartX > 50) prevPage();
});

loadBook();
