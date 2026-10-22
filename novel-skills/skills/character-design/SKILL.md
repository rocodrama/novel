---
name: character-design
description: 웹소설 작품의 캐릭터 디자인 이미지를 만든다. 설정집 인물 카드로 이미지 프롬프트를 쓰고, Codex CLI로 병렬 생성해 구글 드라이브 이미지 폴더에 저장하고, 노션 작품의 '3. 비주얼' 페이지에 이미지와 인물 관계도를 올린다. "캐릭터 디자인 만들어 줘", "인물 이미지 뽑아 줘", "비주얼 단계 진행" 같은 요청에 쓴다.
---

# 캐릭터 디자인

## 0. 준비

- 작업 폴더는 작품 폴더다. `CLAUDE.md`에서 드라이브 경로와 노션 작품 페이지 위치를 읽는다.
- `codex login status`로 Codex 로그인을 확인한다. 이미지 생성은 ChatGPT 로그인 Codex에서 된다.
- 설정집을 읽는다: `设定集/主角卡.md`, `设定集/女主卡.md`, `设定集/조연.md`(있으면), `设定集/世界观.md`.
- **설정이 확정된 뒤에** 만든다. 외모나 관계가 바뀌면 다시 만들어야 한다.

## 1. 인물과 프롬프트 정하기

- 기본은 주인공, 여주, 서브 히로인. 한 인물이 두 모습이면(예: 학교 모습과 버튜버 아바타) 따로 만든다.
- 인물마다 설정집에서 **외모 고정값**(머리 색·길이, 눈, 체형, 옷, 소품, 표정)을 뽑는다. 설정집에 외모가 없으면 작품 분위기에 맞춰 정하고, 정한 내용을 설정집에도 적는다.
- 인물을 잇는 **시각 단서**(같은 머리핀, 같은 색, 같은 소품)를 의도적으로 넣는다.
- 프롬프트는 영어로, 인물 이름은 로마자로 쓴다. 이미지 안에 글자를 넣지 않는다.

`spec.json` (작품 폴더의 `.webnovel/tmp/`에 둔다):

```json
{
  "style": "Character design sheet, Korean web novel illustration style (clean anime-inspired line art, soft cel shading), full body front view plus a small bust close-up, plain light background, no text, no logos.",
  "items": [
    {"file": "01_서하린_교복.png", "prompt": "Character: Seo Ha-rin, Korean high school girl ... (외모 고정값)"},
    {"file": "02_하루미루_아바타.png", "prompt": "Character: 'Harumiru', a VTuber avatar ..."}
  ]
}
```

파일 이름은 `NN_이름_구분.png`.

## 2. 생성

```bash
python -X utf8 "<이 스킬 폴더>/scripts/generate_images.py" .webnovel/tmp/spec.json "G:/내 드라이브/novel/<플랫폼>/<폴더 이름>/이미지"
```

- 최대 4장을 동시에 만든다. 한 장에 1~2분 걸린다. 오래 걸리면 백그라운드로 돌린다.
- 먼저 `--dry-run`으로 프롬프트를 확인할 수 있다.
- **Codex에게 저장을 시키지 않는다.** Codex는 드라이브 폴더에 쓰지 못한다. 스크립트가 `~/.codex/generated_images/<세션 id>/`에서 찾아 복사한다.
- 실패한 장만 spec에서 남기고 다시 실행한다.

## 3. 확인

만든 이미지를 하나씩 열어(Read) 본다.

- 설정과 어긋나는 점(머리 색, 옷, 소품, 표정, 나이대)이 있으면 프롬프트를 고쳐 그 장만 다시 만든다.
- 실존 로고·브랜드나 읽을 수 있는 글자가 들어갔으면 다시 만든다.
- 플랫폼 수위에 맞지 않는 노출이 있으면 다시 만든다.

## 4. 노션 '3. 비주얼' 페이지

1. 이미지마다 `notion-create-file-upload`(파일 이름은 ASCII, 예: `harin_school.png`)를 부른다. 응답의 `upload_url`과 `upload_headers.authorization`을 받는다.
2. 업로드한다. 한글 경로 문제를 스크립트가 처리한다.
   ```bash
   python -X utf8 "<이 스킬 폴더>/scripts/notion_upload.py" "<upload_url>" "<authorization 값>" "<이미지 경로>"
   ```
   출력된 `file-upload://...`을 쓴다. 업로드 URL은 한 시간 안에 써야 한다.
3. 작품의 '3. 비주얼' 하위 페이지를 다시 쓴다.
   - 맨 위 콜아웃: 1차안이며 원본은 드라이브 `이미지` 폴더에 있다는 안내
   - `## 캐릭터 디자인`: 두 장씩 `<columns><column>…</column></columns>`. 각 칸에 **이름(구분)**, 외모 요약 한 줄, `<image source="file-upload://...">캡션</image>`
   - `## 디자인 포인트`: 시각 단서, 인물 간 대비
   - `## 인물 관계도`: mermaid `graph LR` 코드 블록. 관계 화살표에 관계와 시기(1부·2부)를 적는다. 피그마가 연결돼 있으면 피그마 관계도 링크도 단다.
   - `## 수정 메모`: 빈 줄 하나(작가가 적는 칸)
4. 페이지를 다시 읽어 이미지 4장이 `notion-file-block://`로 붙었는지 확인한다.

## 5. 마무리

- 작품 '진행 단계' 페이지에서 "3. 비주얼: 캐릭터 디자인" 항목을 체크한다.
- 사용자에게 인물별로 디자인 요약과 확인 포인트를 알리고, 수정할 점은 '3. 비주얼'의 "수정 메모"에 적어 달라고 안내한다.
