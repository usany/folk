---
name: fairy-tale-orchestrator
description: "동화책 자동 제작 오케스트레이터. 시나리오 작성부터 이미지 생성, HTML 책 뷰어 빌드, 라이브러리 갱신까지 5명의 에이전트 팀(art-director, illustrator, book-builder, qa-reviewer, librarian)을 조율한다. 단편(6~15페이지)과 장편(30+페이지) 모두 지원. doodle/watercolor/Ghibli/flat 스타일 선택 가능. 트리거: 'need book', '동화책 만들어', '동화 만들어줘', '그림책 제작', '두 번째 동화', '새 동화', '동물 동화', '모험 동화', '장편 동화', '챕터 동화', 'doodle 동화', '색연필 동화', '아이용 책 만들기', 'fairy tale book', 'storybook', '동화책 뷰어'. 후속 작업: '동화 다시 써', '이미지 다시 그려', '장면 N 수정', '스토리 보완', '뷰어 디자인 변경', '이전 책 개선', '책 업데이트', '라이브러리 갱신', '도서관 홈 수정' 등 동화 관련 모든 후속 요청도 반드시 이 스킬을 사용."
---

# Fairy Tale Orchestrator — 동화책 제작 통합 워크플로우

5명의 에이전트 팀이 협업하여 시나리오 → 이미지 → 책 뷰어 → 라이브러리 갱신을 완성하는 통합 스킬.

## 실행 모드: 하이브리드

| Phase                    | 모드          | 이유                                                                |
| ------------------------ | ------------- | ------------------------------------------------------------------- |
| Phase 2 (아트디렉션)     | 서브 에이전트 | art-director 단일이 시나리오 + 스타일 + 프롬프트 생성               |
| Phase 3 (이미지 생성)    | 서브 에이전트 | illustrator 단일이 이미지 배치를 실행, 팀 통신 오버헤드 불필요      |
| Phase 4 (뷰어 빌드 + QA) | 에이전트 팀   | book-builder ↔ qa-reviewer 가 즉시 피드백 교환                      |
| Phase 5 (라이브러리 갱신)| 서브 에이전트 | librarian 단일이 library.json 및 홈 페이지 리빌드                   |

## 에이전트 구성

| 팀원         | agent_type   | 역할                                          | 출력                                                |
| ------------ | ------------ | --------------------------------------------- | --------------------------------------------------- |
| art-director | art-director | 비주얼 스타일 + 영문 프롬프트 | `_workspace/01_storyteller_scenario.json` + `02_art_director_prompts.json` |
| illustrator  | illustrator  | 이미지 PNG 12장 생성                          | `book/images/cover.png + scene_01~11.png`           |
| book-builder | book-builder | HTML 책 뷰어 빌드                            | `book/index.html + style.css + book.js + book.json` |
| qa-reviewer  | qa-reviewer  | 통합 정합성 검증                              | `_workspace/04_qa_report.md`                        |
| librarian    | librarian    | 라이브러리 매니페스트 + 홈 갱신               | `books/library.json`, `index.html`                  |

## 워크플로우

### Phase 0: 컨텍스트 확인

1. `_workspace/` 존재 여부 확인
2. `book/index.html` 존재 여부 확인
3. 실행 모드 결정:
   - 둘 다 없음 → **초기 실행**, Phase 1 진행
   - 둘 다 존재 + 사용자가 부분 수정 요청 → **부분 재실행** (해당 에이전트만 호출)
   - 둘 다 존재 + 새 주제 입력 → **새 실행**, 기존 `_workspace/` 와 `book/` 를 각각 `_workspace_{timestamp}/`, `book_{timestamp}/` 로 보관 후 새로 생성

### Phase 1: 준비

1. 디렉토리 보장: `_workspace/`, `book/images/`

### Phase 2: 아트디렉션 (서브)

**실행 모드:** 서브 에이전트

1. `Agent(name: art-director, subagent_type: art-director, model: opus, prompt: "[주제: {theme}] [연령대: {age}] 동화 시나리오 11장면 작성 후, 일관된 비주얼 스타일 + 12개 영문 프롬프트 생성")`
   - 출력: `_workspace/01_storyteller_scenario.json` (시나리오)
   - 출력: `_workspace/02_art_director_prompts.json` (스타일 + 프롬프트)
   - 백그라운드 실행 가능

### Phase 3: 이미지 생성 (서브)

**실행 모드:** 서브 에이전트

1. `Agent(name: illustrator, subagent_type: illustrator, model: opus, prompt: "_workspace/02_art_director_prompts.json 을 읽고 Cloudflare Workers AI 배치로 12장 생성")`
   - **서브 에이전트의 빌트인 타입은 `general-purpose`** (커스텀 타입 illustrator 가 빌트인이 아니라면 `subagent_type: "general-purpose"` 로 호출하고 prompt 에 illustrator.md 의 역할을 요약 전달, 또는 .claude/agents/illustrator.md 파일을 그대로 참조하도록 지시)
   - 백그라운드 실행
2. 완료 후 `book/images/` 의 PNG 12장 존재 확인

### Phase 4: 뷰어 빌드 + QA (팀)

**실행 모드:** 에이전트 팀

1. Lead: "Spawn book-builder and qa-reviewer teammates. Book-builder builds the HTML viewer from scenario + images. QA-reviewer validates after build completes. If QA finds issues, it should communicate them to book-builder for fixes."
   - book-builder → `book/index.html + style.css + book.js + book.json` 출력
   - qa-reviewer → `_workspace/04_qa_report.md` 검증 보고서
2. Teammates automatically coordinate through shared task list and direct messaging until PASS
3. Lead receives completion notification

### Phase 5: 마무리 + 라이브러리 갱신 (서브)

**실행 모드:** 서브 에이전트

1. `Agent(name: librarian, subagent_type: librarian, prompt: "books/library.json 을 업데이트하고 루트 index.html 을 갱신")`
   - 백그라운드 실행, 새 책을 books/library.json 에 추가 및 library home 리빌드
   - 완료 후 `_workspace/` 보존
2. 사용자에게 결과 보고: `book/index.html` 경로, 페이지 수, QA 결과, 라이브러리 업데이트 완료
3. 미리보기 안내: 루트 `index.html` (라이브러리 홈) 또는 개별 책 경로

## 데이터 흐름

```
사용자 입력
    ↓
[art-director]
    ↓
01_scenario.json + 02_prompts.json
    ↓
[illustrator (이미지 병렬)]
    ↓
book/images/*.png (9장)
    ↓
[book-builder] ↔ [qa-reviewer]
    ↓                    ↓
book/index.html    04_qa_report.md
    ↓
[librarian] (라이브러리 갱신)
    ↓
books/library.json + 루트 index.html
    ↓
사용자 (라이브러리 홈 또는 개별 책 열기)
```

## 에러 핸들링

| 상황              | 전략                                                             |
| ----------------- | ---------------------------------------------------------------- |
| storyteller 실패  | 기본 동화 템플릿 (별빛 우정 8장면) 으로 폴백                     |
| 이미지 일부 누락  | 누락 장면 1회 재시도, 그래도 실패 시 placeholder + 보고서에 명시 |
| 이미지 전체 실패  | 사용자에게 보고, 텍스트만 있는 뷰어 빌드 여부 확인               |
| book-builder 실패 | 최소 단일 페이지 fallback HTML 생성                              |
| qa-reviewer FAIL  | 문제 모듈에게 1회 수정 요청, 재실패 시 PARTIAL 로 마무리         |
| librarian 실패    | books/library.json 업데이트 생략, 개별 책은 정상 완성으로 보고   |

## 테스트 시나리오

### 정상 흐름

1. 사용자: "동화책 만들어줘 — 별을 좋아하는 토끼 이야기"
2. Phase 2: art-director 가 8장면 시나리오 + 일관된 watercolor 스타일 + 9개 영문 프롬프트 생성
3. Phase 3: illustrator 가 이미지 배치로 약 5분 만에 9장 생성
4. Phase 4: book-builder 가 HTML 뷰어, qa-reviewer 가 PASS
5. Phase 5: librarian 이 books/library.json 을 업데이트, 루트 index.html (라이브러리 홈) 리빌드
6. 사용자가 루트 `index.html` 을 열면 라이브러리 홈에서 신규 책 카드 확인, 클릭 시 개별 책 뷰어로 진입

### 에러 흐름 (이미지 1장 실패)

1. Phase 3 후 `book/images/scene_05.png` 누락 발견
2. illustrator 가 scene_05 만 단일 재시도
3. 재시도 성공 → 정상 진행, 또는 실패 → placeholder + 보고서 명시
4. book-builder 가 placeholder 처리하여 뷰어 빌드
5. qa-reviewer 가 PARTIAL 로 보고
6. Phase 5: librarian 이 라이브러리 업데이트 (PARTIAL 표시 포함)

## description 의 후속 작업 키워드

이 description 은 다음 후속 요청에서도 반드시 트리거되어야 한다:

- "동화 다시 써", "장면 3 수정", "이미지 다시 그려", "스타일 바꿔", "뷰어 색감 변경"
- "이전 책 개선", "표지만 바꿔", "엔딩 메시지 수정"
