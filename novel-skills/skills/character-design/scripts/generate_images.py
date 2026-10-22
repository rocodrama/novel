#!/usr/bin/env python3
"""Codex CLI로 캐릭터 디자인 이미지를 병렬 생성하고 출력 폴더로 복사한다.

Codex는 샌드박스 때문에 드라이브 같은 폴더에 직접 저장하지 못한다. 그래서 이미지는
~/.codex/generated_images/<session id>/ 에 남고, 이 스크립트가 세션 id로 찾아 복사한다.

사용:
  python -X utf8 generate_images.py <spec.json> <출력 폴더> [--dry-run]

spec.json:
  {"style": "공통 스타일 문장", "items": [{"file": "01_서하린_교복.png", "prompt": "Character: ..."}]}
"""
import argparse
import concurrent.futures as cf
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

GEN_DIR = Path.home() / ".codex" / "generated_images"
SESSION_RE = re.compile(r"session id:\s*([0-9a-f-]{36})", re.IGNORECASE)


def build_prompt(style: str, prompt: str) -> str:
    return f"Use your image generation tool to create ONE image. Do not try to save or move files. {style} {prompt}"


def run_one(style: str, item: dict, out_dir: Path) -> str:
    proc = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", build_prompt(style, item["prompt"])],
        # stdin을 비우지 않으면 codex exec가 입력을 기다리며 멈춘다
        stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=Path.home(),
        timeout=600,
        shell=sys.platform == "win32",
    )
    log = (proc.stdout or "") + (proc.stderr or "")
    m = SESSION_RE.search(log)
    if not m:
        return f"실패 {item['file']}: 세션 id를 찾지 못함\n{log[-500:]}"
    pngs = sorted((GEN_DIR / m.group(1)).glob("*.png"))
    if not pngs:
        return f"실패 {item['file']}: 세션 {m.group(1)}에 이미지가 없음 (Codex 응답: {log.strip()[-200:]})"
    shutil.copyfile(pngs[-1], out_dir / item["file"])
    return f"완료 {item['file']} ← {pngs[-1]}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("out_dir")
    ap.add_argument("--dry-run", action="store_true", help="Codex를 부르지 않고 프롬프트만 출력")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    style, items = spec.get("style", ""), spec["items"]
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        for it in items:
            print(f"[{it['file']}]\n{build_prompt(style, it['prompt'])}\n")
        return 0

    with cf.ThreadPoolExecutor(max_workers=min(4, len(items))) as ex:
        results = list(ex.map(lambda it: run_one(style, it, out_dir), items))
    print("\n".join(results))
    return 0 if all(r.startswith("완료") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
