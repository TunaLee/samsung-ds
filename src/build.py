#!/usr/bin/env python3
"""교시별 덱을 docs/ 에 만든다. 사용: python3 src/build.py"""
import importlib
from pathlib import Path

import art

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DECKS = [f"s{i}" for i in range(1, 9) if (SRC / f"s{i}.py").exists()]


def render(title, parts):
    tpl = (SRC / "template.html").read_text(encoding="utf-8")
    theme = "\n".join(f.read_text(encoding="utf-8") for f in sorted(SRC.glob("theme*.css")))
    tpl = tpl.replace("</style>\n</head>", theme + "\n</style>\n</head>", 1)
    return tpl.replace("{{DECK_TITLE}}", title).replace("{{SLIDES}}", art.DEFS + "\n\n".join(parts))


def main():
    out = ROOT / "docs"
    out.mkdir(exist_ok=True)
    rows = []
    for name in DECKS:
        mod = importlib.import_module(name)
        parts = mod.slides()
        (out / f"{name}.html").write_text(render(mod.TITLE, parts), encoding="utf-8")
        rows.append(f'<a class="row" href="{name}.html"><b>{name[1:]}교시 · {mod.TITLE}</b><span>{len(parts)}장 →</span></a>')
        print(name, len(parts), "장")
    (out / "index.html").write_text(INDEX.replace("{{ROWS}}", "\n".join(rows)), encoding="utf-8")


INDEX = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Agent 아키텍트 과정</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.min.css">
<style>body{margin:0;font-family:Pretendard,sans-serif;color:#111;background:#fff}main{max-width:860px;margin:0 auto;padding:56px 16px}
.k{color:#E8002D;font-weight:800;font-size:14px}h1{font-size:38px;margin:10px 0 30px}
a.row{display:flex;justify-content:space-between;padding:14px 4px;border-bottom:1px solid #E6E6EA;color:#111;text-decoration:none}
a.row:hover{background:#FFF5F7}a.row span{color:#6B6B73;font-size:14px}</style></head><body><main>
<div class="k">B Track</div><h1>AI Agent 아키텍트 과정</h1>
{{ROWS}}
</main></body></html>"""

if __name__ == "__main__":
    main()
