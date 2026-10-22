# novel

웹소설 작업에 공통으로 쓰는 Claude Code 스킬 모음입니다. 작품 설정과 원고를 관리하는 도구는 별도 저장소인 [webnovel-writer-ko](https://github.com/rocodrama/webnovel-writer-ko)에 있고, 이 저장소에는 그 위에서 쓸 **우리만의 공통 스킬**을 모읍니다.

## 구조

```text
common/                      # 이 저장소
├── .claude-plugin/
│   └── marketplace.json     # 플러그인 마켓플레이스 정의
├── novel-skills/            # 플러그인
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       └── <스킬이름>/SKILL.md
└── webnovel-writer/         # 별도 저장소(webnovel-writer-ko), 여기서는 제외
```

## 스킬 목록

| 스킬 | 언제 쓰나 | 하는 일 |
|---|---|---|
| `episode-finish` | 회차를 다 쓴 뒤 | 분량(5,000자 이상)·AI 티 점검(스크립트 + humanize-scan), Codex 교차 검수, 웹소설식 회차 제목, webnovel-writer-ko 커밋, 드라이브 백업, 노션 회차 표·집필 메모 갱신 |
| `new-work-setup` | 새 작품을 시작할 때 | 제목 중복 확인, 노션 작품 페이지(하위 페이지 8개 + 회차 관리 표), 작품 폴더 초기화, 드라이브 폴더, 작품 CLAUDE.md |
| `character-design` | 설정이 확정된 뒤 | 설정집 기반 이미지 프롬프트, Codex 병렬 생성, 드라이브 저장, 노션 '3. 비주얼' 업로드와 인물 관계도 |

필요한 것: webnovel-writer-ko 플러그인, Codex CLI(ChatGPT 로그인), 노션 연결, humanize-korean 플러그인(선택).

## 스킬 추가하기

`novel-skills/skills/<스킬이름>/SKILL.md` 파일을 만듭니다.

```markdown
---
name: 스킬이름
description: 언제 이 스킬을 쓰는지 한두 문장으로
---

# 스킬 제목

지침 내용
```

## 설치

```bash
claude plugin marketplace add rocodrama/novel --scope user
```

```bash
claude plugin install novel-skills@rocodrama-novel --scope user
```

스킬을 추가하거나 고친 뒤에는 마켓플레이스를 업데이트하고 Claude Code를 다시 시작하세요.

```bash
claude plugin marketplace update rocodrama-novel
```
