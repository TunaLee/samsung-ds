"""과정 소개 도식. 흰 바탕 · 검정 글자 · 빨강 강조 · 선 아이콘."""
from fig import ic


def _box(x, y, w, h, fill="#fff", stroke="#111", sw=1.5, rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def _t(x, y, s, size=18, fill="#111", w=700, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def _ar(x1, y1, x2, y2, c="#111", m="s0k", sw=2.2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" marker-end="url(#{m})"/>'


def roles():
    """두 AI의 역할: 개발 환경의 Claude Code가 앱을 만들고, 실행 환경의 앱이 OpenAI GPT를 호출."""
    R, K, M = "#E8002D", "#111", "#8C8C94"
    mk = "".join(f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                 f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for i, c in [("s0k", K), ("s0r", R)])
    s = [f'<svg class="s0-roles" viewBox="0 0 1160 440"><defs>{mk}</defs>',
         # 앱 실행 환경
         _box(1, 1, 1158, 248, "#FAFAFB", "#E6E6EA", 1, 14), _t(26, 36, "앱 실행 환경", 16, M, 800, "start"),
         _box(24, 95, 130, 80, "#fff", K), _t(89, 142, "사용자", 19),
         _ar(160, 135, 208, 135),
         _box(216, 50, 470, 180, "#fff", K, 2, 14), _t(240, 84, "웹 앱 · RAG 앱 · Agent 앱", 17, K, 800, "start"),
         _box(240, 106, 180, 100, "#F5F5F7", "#E6E6EA", 1, 10), _t(330, 163, "화면", 19),
         _ar(426, 156, 474, 156),
         _box(482, 106, 180, 100, "#F5F5F7", "#E6E6EA", 1, 10), _t(572, 163, "앱 로직", 19),
         _ar(694, 112, 886, 112), _t(790, 100, "LLM 호출", 16, K, 800),
         _ar(886, 190, 694, 190), _t(790, 218, "응답", 16, M, 800),
         _box(894, 70, 242, 150, K, K, 2, 14), _t(1015, 142, "OpenAI GPT", 27, "#fff", 900),
         _t(1015, 176, "API Key", 16, "#C9C9CF", 700),
         # 사이 화살표
         _ar(486, 346, 486, 238, R, "s0r", 2.6), _t(504, 296, "코드 생성 · 수정", 17, R, 800, "start"),
         # 개발 환경
         _box(1, 310, 1158, 129, "#FFF5F7", "#F7A8B8", 1, 14), _t(26, 345, "개발 환경", 16, R, 800, "start"),
         _box(24, 360, 130, 62, "#fff", K), _t(89, 398, "수강생", 19),
         _ar(160, 391, 328, 391, R, "s0r"), _t(244, 380, "자연어 지시", 16, R, 800),
         _box(336, 350, 300, 82, "#fff", R, 2.5, 12), _t(486, 388, "Claude Code", 25, R, 900),
         _t(486, 416, "구독 계정", 15, M, 700),
         '</svg>']
    return "".join(s)


def modules():
    """과정 구성: 5개 모듈 · 8개 교시."""
    rows = [("1", "1교시", "AI Agent", "목표 · 도구 선택 · Context Window"),
            ("2", "2 ~ 3교시", "RAG", "필요한 근거를 찾고 입력에 담는 방법"),
            ("3", "4 ~ 5교시", "AI Agent", "도구 결과를 읽고 다음 행동 선택"),
            ("4", "6교시", "Multi-Agent", "반복 판정과 도구 조사의 역할 · 비용 분담"),
            ("5", "7 ~ 8교시", "캡스톤 프로젝트", "업무 결과물 구현 · 실제 실행 결과 발표")]
    out = [f'<div class="s0-mod{" on" if n in ("1", "5") else ""}"><em>Module {n}</em><small>{s}</small><b>{t}</b><span>{d}</span></div>'
           for n, s, t, d in rows]
    return '<div class="s0-mods">' + '<i class="s0-pa">→</i>'.join(out) + "</div>"


def tree(root, items):
    """폴더 구조 카드."""
    li = "".join(f'<li>{ic("folder")}<span>{x}</span></li>' for x in items)
    return (f'<div class="s0-tree"><div class="s0-troot">{ic("folder")}<code>{root}</code></div>'
            f'<ul>{li}</ul></div>')


def link(label, url, desc=""):
    d = f'<span class="s0-ld">{desc}</span>' if desc else ""
    return (f'<a class="s0-link" href="{url}" target="_blank" rel="noopener"><div class="s0-li">{ic("link")}</div><div class="s0-lt"><b>{label}</b>'
            f'<code>{url}</code>{d}</div></a>')
