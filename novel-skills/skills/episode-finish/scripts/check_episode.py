#!/usr/bin/env python3
"""회차 원고 점검: 분량(공백 포함) + AI 티 신호(C-11, C-8, I-4, F-5) + 장면 구분 줄 번호.

사용: python -X utf8 check_episode.py <회차.md> [--min 5000] [--novelpia 3000]
--novelpia N 을 주면 공백 포함 기준 대신 노벨피아식 글자 수(공백·구분선·주요 문장부호 제외) N자 이상으로 판정한다.
분량 미달이거나 C-11이 1개 이상이거나 C-8이 2개 이상이면 종료 코드 1.
"""
import argparse
import re
import sys
from pathlib import Path

NARRATION_SKIP = ("#", '"', "[", "---", "“")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--min", type=int, default=5000)
    ap.add_argument("--novelpia", type=int, default=0)
    args = ap.parse_args()

    text = Path(args.path).read_text(encoding="utf-8")
    lines = text.splitlines()
    body = text.split("\n", 1)[1] if "\n" in text else text
    with_spaces = len(body.replace("\n", ""))
    without_spaces = len("".join(body.split()))
    # 대사·채팅·제목·구분선은 서술 신호 측정에서 뺀다
    narration = [(i, l) for i, l in enumerate(lines, 1) if l and not l.startswith(NARRATION_SKIP)]

    c11 = [(i, m.group()) for i, l in narration for m in re.finditer(r"\S*(고|며|지만|면서|아서|어서),", l)]
    c8 = [(i, l[:40]) for i, l in narration if re.search(r"아니라|아닌가|도 아니다|은 아니다\. 오히려", l)]
    i4 = [i for i, l in narration if re.search(r"해야 한다[.!]?$", l)]
    f5 = [(i, m.group()) for i, l in narration for m in re.finditer(r"\S+적 \S+", l)]
    breaks = [i for i, l in enumerate(lines, 1) if l.strip() == "---"]

    # 노벨피아 표시 글자 수 근사: 공백·구분선·마침표·쉼표·물음표·따옴표·말줄임표 제외
    kept = "".join(l for l in body.splitlines() if l.strip() != "---")
    novelpia = len(re.sub(r"[\s.,?\"…]", "", kept))
    if args.novelpia:
        ok_len = novelpia >= args.novelpia
        rule = f"노벨피아식 {args.novelpia}자 이상"
    else:
        ok_len = with_spaces >= args.min
        rule = f"공백 포함 {args.min}자 이상"
    print(f"분량: 공백 포함 {with_spaces}자 / 공백 제외 {without_spaces}자 / 노벨피아식 약 {novelpia}자 / 기준 {rule} → {'통과' if ok_len else '미달'}")
    print(f"줄 수: {len(lines)} / 장면 구분(---) 줄: {breaks}")
    print(f"C-11 연결어미 뒤 쉼표: {len(c11)}개 {c11}")
    print(f"C-8 'A가 아니라 B' 대구: {len(c8)}개 {c8}")
    print(f"I-4 당위 종결: {i4}")
    print(f"F-5 '~적 N': {f5}")

    failed = (not ok_len) or c11 or len(c8) >= 2
    print("판정:", "수정 필요" if failed else "통과")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
