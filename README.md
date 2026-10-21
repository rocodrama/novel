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

비공개 저장소라서 GitHub에 로그인된 git이 필요합니다.

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
