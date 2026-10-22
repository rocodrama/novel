#!/usr/bin/env python3
"""노션 MCP의 notion-create-file-upload가 준 upload_url로 파일 하나를 올린다.

curl은 한글 경로(예: G:\\내 드라이브\\...)에서 업로드에 실패하므로 ASCII 임시 경로로 복사해서 보낸다.

사용:
  python -X utf8 notion_upload.py <upload_url> "<authorization 헤더 값>" <파일 경로>
성공하면 markdown_source(file-upload://...)를 출력한다.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    url, auth, src = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    with tempfile.TemporaryDirectory(prefix="notion_up_") as tmp:
        safe = Path(tmp) / ("upload" + src.suffix.lower())
        shutil.copyfile(src, safe)
        proc = subprocess.run(
            ["curl", "-sS", "-X", "POST", url, "-H", f"authorization: {auth}", "-F", f"file=@{safe.name}"],
            capture_output=True, text=True, cwd=tmp,
        )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("업로드 실패:", proc.stdout[:300], proc.stderr[:300])
        return 1
    if data.get("status") != "uploaded":
        print("업로드 실패:", json.dumps(data, ensure_ascii=False)[:300])
        return 1
    print(data["markdown_source"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
