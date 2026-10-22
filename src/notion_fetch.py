#!/usr/bin/env python3
"""공개 노션 사이트(teamsparta.notion.site) 페이지를 블록 단위로 받아 마크다운으로 저장한다.

사용: python3 src/notion_fetch.py <페이지 id> <저장 이름>
그림은 source/<저장 이름>_img/ 에 함께 받는다. 읽기 권한으로 보이는 공개 페이지만 대상.
"""
import json
import subprocess
import sys
import urllib.parse
from pathlib import Path

BASE = "https://teamsparta.notion.site"
SPACE = "83c75a39-3aba-4ba4-a792-7aefe4b07895"
ROOT = Path(__file__).resolve().parent.parent
_cache = {}


def post(ep, body):
    out = subprocess.run(["curl", "-s", "-X", "POST", f"{BASE}/api/v3/{ep}", "-H", "content-type: application/json",
                          "-d", json.dumps(body)], capture_output=True, text=True).stdout
    return json.loads(out)


def fetch(ids):
    need = [i for i in ids if i not in _cache]
    for k in range(0, len(need), 80):
        d = post("syncRecordValuesMain", {"requests": [{"pointer": {"table": "block", "id": i, "spaceId": SPACE}, "version": -1}
                                                       for i in need[k:k + 80]]})
        for i, v in d.get("recordMap", {}).get("block", {}).items():
            v = v.get("value", v)
            _cache[i] = v.get("value", v)
    return [_cache.get(i) for i in ids]


def text(prop):
    if not prop:
        return ""
    out = []
    for seg in prop:
        t = seg[0]
        marks = seg[1] if len(seg) > 1 else []
        if any(m[0] == "c" for m in marks):
            t = f"`{t}`"
        if any(m[0] == "b" for m in marks):
            t = f"**{t}**"
        out.append(t)
    return "".join(out)


def walk(bid, depth, lines, imgs):
    b = fetch([bid])[0]
    if not b or not b.get("alive", True):
        return
    t, p = b.get("type"), b.get("properties", {})
    title = text(p.get("title"))
    ind = "  " * depth
    if t == "header":
        lines.append(f"\n# {title}")
    elif t == "sub_header":
        lines.append(f"\n## {title}")
    elif t == "sub_sub_header":
        lines.append(f"\n### {title}")
    elif t == "bulleted_list":
        lines.append(f"{ind}- {title}")
    elif t == "numbered_list":
        lines.append(f"{ind}1. {title}")
    elif t == "to_do":
        lines.append(f"{ind}- [ ] {title}")
    elif t == "quote":
        lines.append(f"> {title}")
    elif t == "callout":
        lines.append(f"\n> 💡 {title}")
    elif t == "toggle":
        lines.append(f"\n▸ {title}")
    elif t == "code":
        lang = text(p.get("language")) or ""
        lines.append(f"\n```{lang}\n{title}\n```")
    elif t in ("image", "file", "pdf", "video"):
        src = text(p.get("source"))
        cap = text(p.get("caption"))
        if src:
            u = f"{BASE}/image/{urllib.parse.quote(src, safe='')}?table=block&id={bid}&spaceId={SPACE}&width=2000&cache=v2"
            imgs.append((bid, cap, u))
            lines.append(f"\n![{cap}](IMG:{bid})")
    elif t == "table":
        rows = fetch(b.get("content", []))
        order = b.get("format", {}).get("table_block_column_order", [])
        for k, r in enumerate(rows):
            cells = [text(r.get("properties", {}).get(c)) if r else "" for c in order]
            lines.append("| " + " | ".join(x.replace("\n", " ") for x in cells) + " |")
            if k == 0:
                lines.append("|" + "---|" * len(order))
        return
    elif t == "divider":
        lines.append("\n---")
    elif t in ("table_of_contents", "breadcrumb"):
        pass
    elif t == "page":
        lines.append(f"\n[하위 페이지] {title}")
        return
    elif title:
        lines.append(f"\n{title}" if depth == 0 else f"{ind}{title}")
    kids = b.get("content", [])
    fetch(kids)
    for c in kids:
        walk(c, depth + (1 if t in ("bulleted_list", "numbered_list", "toggle", "callout", "to_do") else 0), lines, imgs)


def main():
    pid, name = sys.argv[1], sys.argv[2]
    page = fetch([pid])[0]
    lines, imgs = [f"# {text(page['properties'].get('title'))}"], []
    for c in page.get("content", []):
        walk(c, 0, lines, imgs)
    d = ROOT / "source" / f"{name}_img"
    d.mkdir(parents=True, exist_ok=True)
    md = "\n".join(lines)
    for k, (bid, cap, u) in enumerate(imgs, 1):
        fn = d / f"{k:02d}"
        subprocess.run(["curl", "-sL", "-o", str(fn), u])
        kind = subprocess.run(["file", "-b", str(fn)], capture_output=True, text=True).stdout
        ext = ".svg" if "SVG" in kind else ".jpg" if "JPEG" in kind else ".png"
        fn.rename(fn.with_suffix(ext))
        md = md.replace(f"IMG:{bid}", f"{name}_img/{k:02d}{ext}")
    (ROOT / "source" / f"{name}.md").write_text(md, encoding="utf-8")
    print(name, len(lines), "줄 ·", len(imgs), "그림")


if __name__ == "__main__":
    main()
