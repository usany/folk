# QA 검증 보고서 — 꼬마 고슴도치 두리의 첫 밤마실

## 요약
- **전체 상태: PARTIAL**
- 검증 완료: 2026-07-11
- 대상 책: `books/03-default-story/` (표지 + 8장면 + 엔딩 = 10페이지)
- 한 줄 결론: 시나리오·본문·뷰어·네비게이션은 모두 완벽히 정합하나, **이미지 9장이 실제 수채화 일러스트가 아니라 그라디언트 placeholder** 라서 시각 품질 기준을 통과하지 못함.

---

## 섹션별 판정

| # | 섹션 | 판정 | 근거 |
|---|------|------|------|
| 1 | Story-to-Page Matching | **PASS** | 8장면 전부 title/body 일치, 총 10페이지 |
| 2 | Image-to-Page Matching | **PASS (파일 매핑)** | cover + scene_01~08 전부 존재, book.js 매핑 정확 |
| 3 | Navigation Integrity | **PASS** | 카운터·진행바·목차·file:// 폴백 모두 정상 |
| 4 | Visual Consistency | **FAIL** | 이미지가 실제 일러스트가 아닌 placeholder |
| 5 | Critical Issues | **PARTIAL** | 깨진 링크 없음, 단 이미지 콘텐츠 부재 |

---

## 경계면 검증 결과

| 경계면 | 항목 | 결과 | 비고 |
|--------|------|------|------|
| 시나리오↔프롬프트 | 장면 수 (8) | PASS | prompts 9개 = 표지1 + 장면8 |
| 시나리오↔뷰어 | 페이지 수 = 8+2 = 10 | PASS | book.json.pages 길이 10 |
| 시나리오↔뷰어 | 장면 title 일치 | PASS | 8/8 완전 일치 |
| 시나리오↔뷰어 | 장면 body 일치 | PASS | 8/8 일치 (직선따옴표→곡선따옴표 정규화만 차이, 의미 동일) |
| 프롬프트↔이미지 | 파일 존재 | PASS | cover.png + scene_01~08.png 9장 전부 존재 |
| 프롬프트↔이미지 | 파일 유효성 | PARTIAL | 유효한 800x1000 PNG이나 **내용이 placeholder** |
| 뷰어↔자원 | book.json 이미지 경로 | PASS | 10개 경로 전부 실제 파일과 매칭 |
| 뷰어↔자원 | book.json ≡ book.data.js | PASS | 두 데이터 완전 동일 (fetch/폴백 일관) |
| 뷰어↔자원 | 외부 의존성 | PASS(명시) | Google Fonts(Gowun Dodum/Gaegu)만 외부, style.css는 외부참조 0 |
| 정적 실행성 | file:// 폴백 | PASS | fetch 실패 시 window.BOOK_DATA 폴백 + 서버 안내 문구 |

---

## 섹션 1 — Story-to-Page Matching: PASS
- 시나리오 `01_storyteller_scenario.json` 8장면 ↔ book.json scene 페이지 8개 1:1 매칭.
- 8장면 모두 **title 완전 일치, body 완전 일치** (스크립트 교차검증 완료).
- 페이지 구성: cover(1) + scene(8) + ending(1) = **정확히 10페이지**.
- 엔딩 메시지는 8장면의 교훈("용기는 마음속에서 스스로 빛나는 작은 불빛")을 재사용 — 의도된 마무리.

## 섹션 2 — Image-to-Page Matching: PASS (매핑 한정)
- `images/` 에 cover.png, scene_01.png ~ scene_08.png **9개 파일 모두 존재**, 누락 0.
- 파일명 패턴 `scene_%02d.png` 규칙 정확히 준수.
- book.js 렌더링: cover→cover.png, scene N→scene_0N.png, ending→scene_08.png 재사용. 매핑 정확.
- 파일 크기 6.5~7.1KB, 전부 0바이트 아님(정상 PNG). **단, 아래 섹션 4 참조.**

## 섹션 3 — Navigation Integrity: PASS
- 페이지 카운터: `indicator.textContent = (index+1) + " / " + total` → "1 / 10" 형식 정확, HTML 초기값도 "1 / 10".
- 진행바: `pct = index/(total-1)*100` → 표지 0%, 엔딩 100% 비례 정확. `aria-valuenow` 갱신.
- 목차(TOC): 10개 페이지 전부 나열(표지★/장면1~8/끝), 현재 페이지 `.current` 하이라이트 로직 정상.
- 조작계: 버튼/엣지클릭/키보드(←→ Space Home End Esc)/터치 스와이프 모두 바인딩.
- **file:// 로컬 오픈 대응**: book.json fetch 실패 시 `book.data.js` 인라인 폴백으로 그대로 동작 → 더블클릭 오픈 OK.

## 섹션 4 — Visual Consistency: FAIL
- **핵심 결함**: 9장 전부 실제 수채화 일러스트가 아니라 `generate_placeholders.py` 가 만든 **세로 그라디언트 + "Placeholder" 텍스트** 이미지.
- 근거:
  - `03_illustrator_log.md` — "생성 실패 (0 / 9)". codex CLI 벤더 바이너리 유실 + codex-image 스킬 미설치로 단 한 장도 실제 생성 안 됨.
  - `books/03-default-story/generate_placeholders.py` 존재 — 5색 파스텔 그라디언트에 "Scene N (Placeholder)" 텍스트를 찍는 스크립트. 현재 images/ 내용물이 정확히 이 산출물.
  - 파일 크기 6.5~7KB (실제 gpt-image 수채화라면 수백 KB~MB 수준이어야 함).
- 결과적으로:
  - 규격 일관성은 역설적으로 PASS (전부 800x1000 세로, 통일된 파스텔 톤).
  - 그러나 **스토리 톤(어두운 밤·반딧불이 노란빛·두리 캐릭터)을 전혀 담지 못함.** 장면 내용과 무관한 색면일 뿐.
  - art-director가 작성한 `02_art_director_prompts.json`(9개 프롬프트, 캐릭터 시그니처 포함)은 정상 — 소재는 준비됐으나 렌더링만 미완.

## 섹션 5 — Critical Issues: PARTIAL
- 깨진 링크/누락 자원: **없음**. 모든 image 경로, style.css, book.js, book.data.js 참조 정상.
- 콘솔 에러: 코드 정적 분석상 예상 에러 없음. fetch 실패는 try/catch로 폴백 처리, history.replaceState도 try/catch.
- 접근성: 이미지 alt 텍스트 존재, progressbar role/aria-valuenow, 버튼 aria-label, 장식용 `.stars`는 aria-hidden — 양호.
  - 경미: 다크 테마 대비, placeholder의 회색(100,100,100) 텍스트 위 alt는 문제 없음.
- 유일하고 결정적인 이슈는 섹션 4의 placeholder 이미지.

---

## 발견된 문제 (우선순위순)

1. **[치명적] 실제 일러스트 부재** — images/ 9장이 전부 placeholder. 스토리·뷰어는 완성됐으나 "그림책"으로서의 그림이 없음.
   - 영향 범위: 최종 산출물의 시청 경험 전체. 출판/공유 불가 수준.
   - 근본 원인: codex CLI 바이너리 유실 + codex-image 스킬 미설치 (illustrator 단계 블로커).

2. **[경미] book.json / book.data.js 이중 관리** — 두 파일이 현재 완전 동일하나, 향후 수정 시 한쪽만 고치면 file:// 와 http:// 결과가 갈릴 위험. 빌드 시 book.data.js를 book.json에서 자동 생성하도록 유지 권장.

---

## 권장 후속 조치

### 사용자 조치 (선행 필수)
1. codex CLI 재설치: `npm install -g @openai/codex` 로 유실된 벤더 바이너리 복구.
2. `codex login` → `codex login status` 가 "Logged in using ChatGPT" 확인.
3. codex-image 스킬(배치 헬퍼 `codex_imagegen_batch.sh`) 설치.

### illustrator 재실행
- 위 복구 후 `02_art_director_prompts.json` 9개 프롬프트로 재생성 → `books/03-default-story/images/` 에 동일 파일명으로 덮어쓰기.
- 파일명만 일치시키면 book-builder/book.json 수정 불필요 (뷰어는 그대로 새 이미지를 렌더).

### book-builder 조치 (선택)
- 재생성 완료 시 book.json / book.data.js 는 변경 불필요 (경로 동일).
- 이미지 교체 후 QA에 재검증 요청하면 섹션 4가 PASS로 전환되어 전체 **PASS** 승격 가능.

---

## 최종 판정
- **PARTIAL** — 텍스트·구조·뷰어·네비게이션은 프로덕션 품질로 완성. 오직 이미지 콘텐츠(placeholder)만 미완이며, 이는 도구 의존성 복구 후 illustrator 재실행 한 번으로 해소 가능.

## 최종 산출물 경로
- HTML 뷰어: `/Users/user/Desktop/picturebook/books/03-default-story/index.html`
  - 더블클릭(file://) 오픈 OK — book.data.js 인라인 폴백으로 동작.
  - 권장: `cd books/03-default-story && python3 -m http.server` 후 http://localhost:8000 접속 (fetch 경로).
- 현재 열면 스토리·페이지 넘김·목차·진행바는 정상 동작하나, 그림 자리에 placeholder가 표시됨.
