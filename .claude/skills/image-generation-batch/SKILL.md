---
name: image-generation-batch
description: Claude 이미지 생성을 사용한 배치 이미지 생성 스킬. illustrator 에이전트 전용. 프롬프트 JSON 을 받아 9장 이상의 이미지를 병렬 생성한다. 트리거 'create images' '이미지 N장 생성', '동화 이미지 배치', '병렬 이미지 생성'.
---

# Image Generation Batch — Claude 이미지 생성

illustrator 에이전트 전용. Claude의 이미지 생성 기능을 활용해 이미지를 효율적으로 병렬 생성한다.

## 사전 확인

- Claude API 접근 가능 (스킬/에이전트는 기본적으로 Claude 모델 사용 가능)
- `book/images/` 디렉토리 쓰기 권한

## 핵심 접근

Claude의 이미지 생성을 활용하여 프롬프트를 이미지로 변환:

```python
# 의사 코드
for each prompt in prompts:
    image_data = claude.generate_image(prompt)
    save_image(image_data, filename)
```

- 9장을 병렬로 요청
- 병렬 처리로 ~2~3분 예상 (codex 보다 빠름)

## 실행 절차 (illustrator 가 따르는 순서)

1. `_workspace/02_art_director_prompts.json` 을 JSON 파싱
2. 모든 프롬프트 + 파일명 쌍 추출 (cover + 8 scenes)
3. 각 프롬프트를 Claude 이미지 생성 API에 병렬 요청
   - 이미지를 base64 인코딩된 PNG로 받음
   - 지정된 파일명으로 `book/images/` 에 저장
4. 완료 알림 대기 (병렬 처리)
5. 완료 후 `book/images//*.png` 9개 존재 확인

## 재시도

배치 후 일부 PNG 가 없으면 해당 프롬프트만 재시도:

```python
if missing_files:
    for filename, prompt in missing_files:
        image_data = claude.generate_image(prompt)
        save_image(image_data, filename)
```

## 결과 검증

```bash
ls -la book/images/*.png  # 파일 크기 0 아닌지 확인
file book/images/*.png    # PNG 파일 형식 검증
wc -l book/images/*.png   # 예상 9장 모두 생성 확인
```

## 로그 저장

`_workspace/03_illustrator_log.md` 에 사람이 읽기 좋은 요약 저장:

```markdown
# Illustrator 실행 로그

- 실행 시각: YYYY-MM-DD HH:MM
- 총 요청: 9장
- 병렬 생성: cover, scene_01~08 — 완료 (약 2~3분)
- 재시도: 없음 또는 (장면 N - 사유)
- 누락: 없음 또는 (장면 N)
- 총 소요: 약 X분
```

## 에러 대응

| 증상             | 대응                                                    |
| ---------------- | ------------------------------------------------------- |
| API 오류         | 중단 + 사용자에게 보고                                  |
| 이미지 생성 거부 | 프롬프트를 art-director 에게 SendMessage 로 재작성 요청 |
| 디스크 쓰기 실패 | book/images/ 권한 확인                                  |
