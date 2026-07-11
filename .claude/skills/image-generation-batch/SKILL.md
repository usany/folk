---
name: image-generation-batch
description: Cloudflare Workers AI (Flux 1 Schnell)를 사용한 배치 이미지 생성 스킬. illustrator 에이전트 전용. 프롬프트 JSON 을 받아 9장 이상의 이미지를 병렬 생성한다. 트리거 'create images' '이미지 N장 생성', '동화 이미지 배치', '병렬 이미지 생성', 'Cloudflare 이미지'.
---

# Image Generation Batch — Cloudflare Flux 1 Schnell

illustrator 에이전트 전용. Cloudflare Workers AI의 Flux 1 Schnell 모델을 활용해 이미지를 효율적으로 병렬 생성한다.

## 사전 확인

- Cloudflare 계정 및 Workers AI 접근 가능
- `.env` 파일에 다음 변수 설정:
  - `CLOUDFLARE_API_TOKEN` (계정 토큰, `cfat_` 시작)
  - `CLOUDFLARE_ACCOUNT_ID` (계정 ID)
- `books/NN-slug/images/` 디렉토리 쓰기 권한

## 핵심 접근

Cloudflare Workers AI의 Flux 1 Schnell 엔드포인트를 활용하여 프롬프트를 이미지로 변환:

```python
# 의사 코드
for each prompt in prompts (병렬):
    response = POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell
    image_data = base64_decode(response.result.image)
    save_image(image_data, filename)
```

- N장을 병렬로 요청
- 병렬 처리로 ~2~3분 예상

## 실행 절차 (illustrator 가 따르는 순서)

1. `.env` 에서 `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` 로드
2. `_workspace/NN/02_art_director_prompts.json` 을 JSON 파싱
3. 모든 프롬프트 추출 (cover + N scenes)
4. 각 프롬프트를 Cloudflare Workers AI API 로 병렬 요청:
   ```
   POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell
   Authorization: Bearer {API_TOKEN}
   {"prompt": "...", "steps": 4}
   ```
   - 이미지를 base64 인코딩된 PNG로 받음
   - 지정된 파일명으로 `books/NN-slug/images/` 에 저장
5. 완료 알림 대기 (병렬 처리)
6. 완료 후 `books/NN-slug/images/*.png` 모두 존재 확인

## 재시도

배치 후 일부 PNG 가 없으면 해당 프롬프트만 재시도:

```python
if missing_files:
    for filename, prompt in missing_files:
        response = POST {cloudflare_endpoint}
        image_data = base64_decode(response.result.image)
        save_image(image_data, filename)
```

## 결과 검증

```bash
ls -la books/NN-slug/images/*.png  # 파일 크기 > 100K 인지 확인
file books/NN-slug/images/*.png    # PNG 파일 형식 검증
wc -l books/NN-slug/images/*.png   # 예상 N장 모두 생성 확인
```

## 로그 저장

`_workspace/NN/03_illustrator_log.md` 에 사람이 읽기 좋은 요약 저장:

```markdown
# Illustrator 실행 로그

- 실행 시각: YYYY-MM-DD HH:MM
- 모델: @cf/black-forest-labs/flux-1-schnell
- 총 요청: N장
- 병렬 생성: cover, scene_01~NN — 완료 (약 2~3분)
- 재시도: 없음 또는 (장면 N - 사유)
- 누락: 없음 또는 (장면 N)
- 총 소요: 약 X분
```

## 에러 대응

| 증상                | 대응                                                           |
| ------------------- | -------------------------------------------------------------- |
| 401 Unauthorized    | `.env` 의 `CLOUDFLARE_API_TOKEN` 재확인 + 권한 검증            |
| 403 Forbidden       | `.env` 의 `CLOUDFLARE_ACCOUNT_ID` 재확인                       |
| 429 Rate Limited    | 요청 속도 제한, 재시도 대기                                    |
| 이미지 생성 거부    | 프롬프트를 art-director 에게 SendMessage 로 재작성 요청        |
| 디스크 쓰기 실패    | `books/NN-slug/images/` 권한 확인                              |
| `.env` 파일 누락    | 사용자에게 `.env` 설정 가이드 제공                             |
