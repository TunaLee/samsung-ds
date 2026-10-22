"""움직이는 도해 (posco-dx viz_hx.py에서 가져와 이 과정 용어 · 색으로 바꿈).

함수마다 인라인 <svg> 하나를 돌려준다. 밝은 내용 장의 본문(약 1160×470)에 그대로 넣는다.
- 색: 남색 · 회색 · 주황 · 흰색만. 주황 = 움직이는 것 · 강조.
- 움직임: CSS keyframes (6–12초 반복). 인쇄 · 동작 줄이기 설정에서는 멈추고,
  속성값(기본값)이 그대로 보인다 → 기본값을 「대표 장면」으로 둔다.
- id · 클래스 · keyframes 이름은 함수마다 접두어를 따로 쓴다 (숨은 장의 url(#id) 참조 방지).
"""

N, G, O, W = "#26262B", "#DCDCE1", "#E8002D", "#FFFFFF"
S = "#55555C"  # 보조 글자 (덱 .bs 와 같은 색)


class _D:
    """도해 하나: 접두어 · 반복 길이 · keyframes 모음."""

    def __init__(self, p, dur):
        self.p, self.dur, self.kfs, self.n = p, dur, [], 0

    def a(self, stops, ease="linear", extra=""):
        """stops: [(퍼센트, 'css 선언'), ...] → style 속성 문자열."""
        self.n += 1
        name = f"hx{self.p}{self.n}"
        body = "".join(f"{p:g}%{{{d}}}" for p, d in stops)
        self.kfs.append(f"@keyframes {name}{{{body}}}")
        return f'style="animation:{name} {self.dur}s {ease} infinite both;{extra}"'

    def id(self, s):
        return f"hx{self.p}{s}"

    def markers(self):
        def m(i, c):
            return (f'<marker id="{self.id(i)}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
                    f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{c}"/></marker>')
        return m("ah", N) + m("aho", O) + m("ahg", "#9AA3B0")

    def svg(self, w, h, body, css=""):
        r = f".hx-{self.p}"
        base = (f"{r}{{width:100%;height:auto;max-height:470px;display:block;margin:0 auto;overflow:visible}}"
                f"{r} text{{font-family:var(--serif);dominant-baseline:middle}}"
                f"{r} .tt{{font-size:19px;font-weight:800;fill:{N}}}"
                f"{r} .ts{{font-size:15px;fill:{S}}}"
                f"{r} .to{{font-size:15px;font-weight:700;fill:{O}}}"
                f"{r} .tw{{font-size:15px;font-weight:700;fill:{W}}}"
                f"{r} .tn{{font-size:15px;font-weight:700;fill:{N}}}"
                f"@media print{{{r} *{{animation:none!important}}{r} .mv{{display:none}}}}"
                f"@media (prefers-reduced-motion:reduce){{{r} *{{animation:none!important}}{r} .mv{{display:none}}}}")
        css = css.replace("&", r)
        return (f'<svg class="hxv hx-{self.p}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
                f'<style>{base}{css}{"".join(self.kfs)}</style><defs>{self.markers()}</defs>{body}</svg>')


def _t(x, y, s, cls="ts", anchor="middle", extra=""):
    return f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" class="{cls}" {extra}>{s}</text>'


def _box(x, y, w, h, title, cls="tt", sub="", fill=W, stroke=N, sw=3, rx=14, extra=""):
    s = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if sub:
        s += _t(x + w / 2, y + h / 2 - 11, title, cls) + _t(x + w / 2, y + h / 2 + 14, sub, "ts")
    else:
        s += _t(x + w / 2, y + h / 2 + 1, title, cls)
    return s


def _tr(x, y):
    return f"transform:translate({x:g}px,{y:g}px)"


def _move(d, pts, color=O, r=9, shape=None):
    """pts: [(퍼센트, x, y, 보임 0/1), ...] 를 따라 움직이는 점(또는 shape)."""
    stops = [(p, f"{_tr(x, y)};opacity:{v}") for p, x, y, v in pts]
    inner = shape or f'<circle r="{r}" fill="{color}"/>'
    return f'<g class="mv" {d.a(stops)}>{inner}</g>'



def context_window(fixed=(("지침", 1, .07), ("도구 정의", .6, .12)),
                   grow=("대화 이력", "도구 결과 · 검색 문서"), summary="이력 요약", call="입력 정리",
                   title="Context Window", sub="= 모델이 한 번에 볼 수 있는 크기", turn="요청"):
    """요청이 반복될수록 입력이 차오르고, 한도 근처에서 정리(요약)한 뒤 다시 쌓인다."""
    d = _D("cw", 12)
    X0, Y, H, BW = 60, 110, 84, 1040
    clip = d.id("clip")
    s = f'<clipPath id="{clip}"><rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12"/></clipPath>'
    s += f'<rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12" fill="{G}" fill-opacity=".3"/>'
    s += f'<g clip-path="url(#{clip})">'
    x = X0
    for _, op, f in fixed:
        s += f'<rect x="{x:g}" y="{Y}" width="{f*BW:g}" height="{H}" fill="{N}" fill-opacity="{op}" stroke="{W}" stroke-width="1.5"/>'
        x += f * BW
    XF = x
    st, conv, res = [(0, 0, 0, 0)], 0, 0
    pre = [4, 11, 18, 25, 32, 39, 46, 53]
    post = [75, 82]
    for t in pre:
        st.append((t, 0, conv, res))
        conv, res = conv + .025, res + .044
        st.append((t + 3, 0, conv, res))
    st += [(60, 0, conv, res), (68, .05, 0, 0)]
    conv = res = 0
    for t in post:
        st.append((t, .05, conv, res))
        conv, res = conv + .025, res + .044
        st.append((t + 3, .05, conv, res))
    st += [(95, .05, conv, res), (100, 0, 0, 0)]
    pc, pr = .025 * 8, .044 * 8

    def seg(kind, fill, op, bx, bw):
        stops = []
        for t, sm, cv, rs in st:
            xx, ww = {"sum": (XF, sm), "conv": (XF + sm * BW, cv), "res": (XF + (sm + cv) * BW, rs)}[kind]
            stops.append((t, f"x:{xx:g}px;width:{ww * BW:g}px"))
        return (f'<rect x="{bx:g}" y="{Y}" width="{bw:g}" height="{H}" fill="{fill}" fill-opacity="{op}" '
                f'stroke="{W}" stroke-width="1.5" {d.a(stops)}/>')

    s += seg("sum", O, .35, XF, 0)
    s += seg("conv", G, 1, XF, pc * BW)
    s += seg("res", O, 1, XF + pc * BW, pr * BW)
    s += "</g>"
    s += f'<rect x="{X0}" y="{Y}" width="{BW}" height="{H}" rx="12" fill="none" stroke="{N}" stroke-width="3"/>'
    s += _t(X0, 88, title, "tt", "start") + _t(X0 + 18 + len(title) * 11, 89, sub, "ts", "start")
    s += _t(X0 + BW, 88, "한도", "tt", "end")
    x80 = X0 + .8 * BW
    s += f'<line x1="{x80:g}" y1="{Y-8}" x2="{x80:g}" y2="{Y+H+8}" stroke="{N}" stroke-width="2" stroke-dasharray="5 5"/>'
    s += _t(x80, Y + H + 24, "80%", "tn")
    c = (f'<rect x="{x80-72:g}" y="18" width="144" height="40" rx="20" fill="{O}"/>'
         + _t(x80, 39, call, "tw", extra='style="font-size:17px"')
         + f'<line x1="{x80:g}" y1="58" x2="{x80:g}" y2="{Y-12}" stroke="{O}" stroke-width="3"/>'
         + _t(x80 + 84, 39, f"{grow[0]} → 요약", "to", "start"))
    s += f'<g {d.a([(0, "opacity:0"), (54, "opacity:0"), (57, "opacity:1"), (70, "opacity:1"), (74, "opacity:0"), (100, "opacity:0")])}>{c}</g>'
    TY = 270
    s += _t(X0, TY, turn, "tt", "start")
    for i, t in enumerate(pre + post):
        cx = 140 + i * 92 + (60 if i >= 8 else 0)
        s += (f'<circle cx="{cx}" cy="{TY}" r="12" fill="{O if i < 8 else G}" '
              + d.a([(0, f"fill:{G}"), (t, f"fill:{G}"), (t + 1, f"fill:{O}"), (95, f"fill:{O}"), (100, f"fill:{G}")]) + "/>")
        s += _t(cx, TY + 30, str(i + 1), "ts", extra='style="font-size:14px"')
    mx = 140 + 7 * 92 + 76
    s += f'<line x1="{mx}" y1="{TY-20}" x2="{mx}" y2="{TY+20}" stroke="{O}" stroke-width="3"/>'
    s += _t(mx, TY + 30, "정리", "to", extra='style="font-size:14px"')
    leg = [(n, N, op) for n, op, _ in fixed] + [(grow[0], G, 1), (grow[1], O, 1), (summary, O, .35)]
    LY = 360
    for i, (name, col, op) in enumerate(leg):
        lx = X0 + i * 190
        s += f'<rect x="{lx}" y="{LY-11}" width="22" height="22" rx="4" fill="{col}" fill-opacity="{op}"/>'
        s += _t(lx + 30, LY + 1, name, "ts", "start")
    return d.svg(1160, 390, s)


def index_query():
    """Indexing Time(문서마다 1회 · 미리) → 저장소 ← Query Time(질문마다). 두 줄이 번갈아 움직인다."""
    d = _D("iq", 12)
    P = "#FFF0F3"

    def hl(a, b):
        return d.a([(0, f"stroke:{N};fill:{W}"), (a, f"stroke:{N};fill:{W}"), (a + 1, f"stroke:{O};fill:{P}"),
                    (b, f"stroke:{O};fill:{P}"), (b + 1, f"stroke:{N};fill:{W}"), (100, f"stroke:{N};fill:{W}")])

    def arrow(path):
        return f'<path d="{path}" fill="none" stroke="{N}" stroke-width="2.5" marker-end="url(#{d.id("ah")})"/>'

    def lane_op(on):
        a, b = (1, .28) if on == "top" else (.28, 1)
        return d.a([(0, f"opacity:{a}"), (46, f"opacity:{a}"), (50, f"opacity:{b}"), (95, f"opacity:{b}"), (99, f"opacity:{a}"), (100, f"opacity:{a}")])

    TY, BY, BH = 58, 322, 68
    top = _t(40, 26, "Indexing Time", "tt", "start") + _t(200, 27, "저장할 때 · 문서마다 1회 · 미리 준비", "ts", "start")
    for (x, w, t, sub, a, b) in [(40, 120, "PDF", "원본", 2, 8), (190, 120, "파싱", "글자 꺼내기", 8, 16),
                                 (340, 120, "청킹", "조각 나누기", 16, 24), (490, 120, "임베딩", "숫자 배열", 24, 32)]:
        top += _box(x, TY, w, BH, t, sub=sub, extra=hl(a, b))
    for x in (160, 310, 460):
        top += arrow(f"M{x + 4} {TY + BH / 2} H{x + 24}")
    top += arrow(f"M614 {TY + BH / 2} H760 V150")
    top += _t(690, TY + BH / 2 - 16, "적재", "tn")

    bot = _t(40, 294, "Query Time", "tt", "start") + _t(170, 295, "물어볼 때 · 질문마다 · 바로 응답", "ts", "start")
    for (x, w, t, sub, a, b) in [(40, 120, "질문", "사용자 입력", 52, 58), (190, 140, "질문 임베딩", "같은 모델", 58, 64),
                                 (360, 120, "검색", "가까운 순", 64, 74), (900, 120, "생성", "LLM · 근거로", 84, 90),
                                 (1050, 90, "답", "출처 포함", 90, 96)]:
        bot += _box(x, BY, w, BH, t, sub=sub, extra=hl(a, b))
    for x0, x1 in ((160, 190), (330, 360), (1020, 1050)):
        bot += arrow(f"M{x0 + 4} {BY + BH / 2} H{x1 - 6}")
    bot += arrow(f"M484 {BY + BH / 2} H760 V288")
    bot += _t(620, BY + BH / 2 - 16, "질문 벡터로 찾기", "tn")
    bot += arrow(f"M862 216 H960 V{BY - 6}")
    bot += _t(974, 262, "근거 청크 몇 개", "to", "start")

    # 저장소 (원통) · 두 시점이 만나는 곳
    cx, y0, y1, rx, ry = 760, 168, 266, 100, 20
    db = (f'<path d="M{cx - rx} {y0} V{y1} A{rx} {ry} 0 0 0 {cx + rx} {y1} V{y0}" fill="{W}" stroke="{N}" stroke-width="3" '
          + d.a([(0, f"stroke:{N}"), (36, f"stroke:{N}"), (37, f"stroke:{O}"), (44, f"stroke:{O}"), (45, f"stroke:{N}"),
                 (70, f"stroke:{N}"), (71, f"stroke:{O}"), (80, f"stroke:{O}"), (81, f"stroke:{N}"), (100, f"stroke:{N}")]) + "/>")
    db += f'<ellipse cx="{cx}" cy="{y0}" rx="{rx}" ry="{ry}" fill="{G}" stroke="{N}" stroke-width="3"/>'
    for i, t in enumerate((37, 39, 41, 43)):
        db += (f'<rect x="{cx - 70 + i * 36}" y="{y1 - 12}" width="28" height="14" rx="3" fill="{O}" '
               + d.a([(0, "opacity:0"), (t, "opacity:0"), (t + 1, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")]) + "/>")
    db += _t(cx, 206, "벡터 저장소", "tt") + _t(cx, 230, "청크 · 벡터 · 출처", "ts")

    # 오른쪽 위 비교 카드
    card = f'<rect x="900" y="{TY}" width="240" height="130" rx="14" fill="{G}" fill-opacity=".35"/>'
    for i, (k, v) in enumerate([("준비", "문서 올릴 때 1회"), ("", "오래 걸려도 됨"), ("질문", "질문마다 매번"), ("", "빨라야 함")]):
        y = TY + 26 + i * 27
        if k:
            card += _t(920, y, k, "to" if k == "질문" else "tn", "start")
        card += _t(970, y, v, "ts", "start")

    mv = _move(d, [(0, 100, 92, 0), (2, 100, 92, 1), (8, 250, 92, 1), (16, 400, 92, 1), (24, 550, 92, 1),
                   (30, 760, 92, 1), (36, 760, 172, 1), (37, 760, 172, 0), (100, 760, 172, 0)])
    mv += _move(d, [(0, 100, 356, 0), (51, 100, 356, 0), (52, 100, 356, 1), (58, 260, 356, 1), (64, 420, 356, 1),
                    (70, 760, 356, 1), (74, 760, 290, 1), (75, 760, 290, 0), (100, 760, 290, 0)])
    mv += _move(d, [(0, 862, 216, 0), (77, 862, 216, 0), (78, 862, 216, 1), (82, 960, 216, 1), (86, 960, 356, 1),
                    (92, 1095, 356, 1), (95, 1095, 356, 0), (100, 1095, 356, 0)])

    s = f'<g {lane_op("top")}>{top}</g><g {lane_op("bot")}>{bot}</g>{db}{card}{mv}'
    return d.svg(1160, 400, s)


# ── 지식 그래프 (3교시 GraphRAG) ─────────────────────────────────────
# 설명용 예시: 소프트 에러 문서의 세 청크. 페이지 · 문장은 설명용.
KG_NODES = {
    "알파 입자": (90, 70), "중성자": (90, 190), "소프트 에러": (300, 130), "RAM": (520, 60),
    "패리티": (150, 300), "ECC": (330, 300), "스크러빙": (510, 250),
    "추가 메모리 비트": (330, 395), "주기적 읽기 부하": (520, 360),
}
KG_EDGES = [  # (출발, 도착, 관계, 청크 번호)
    ("알파 입자", "소프트 에러", "일으킨다", 0), ("중성자", "소프트 에러", "일으킨다", 0), ("소프트 에러", "RAM", "발생 위치", 0),
    ("패리티", "소프트 에러", "검출만", 1), ("ECC", "소프트 에러", "검출 · 정정", 1), ("ECC", "추가 메모리 비트", "필요", 1),
    ("스크러빙", "소프트 에러", "완화", 2), ("스크러빙", "주기적 읽기 부하", "발생", 2),
]
KG_CHUNKS = [("p.3", "소프트 에러는 알파 입자나 중성자가", "RAM 셀의 값을 뒤집는 현상이다."),
             ("p.7", "패리티는 오류를 검출만 한다. ECC는 검출 · 정정", "하지만 추가 메모리 비트가 필요하다."),
             ("p.9", "스크러빙은 메모리를 주기적으로 읽어", "오류를 정정 · 완화하며 읽기 부하가 생긴다.")]


def _kg_w(name):
    return sum(9 if c.isascii() else 16 for c in name) + 30


def _kg_clip(a, b, dx=0):
    """a 중심에서 b 중심으로 가는 선을 두 상자 테두리에서 자른다."""
    (x1, y1), (x2, y2) = KG_NODES[a], KG_NODES[b]
    x1, x2 = x1 + dx, x2 + dx

    def edge(cx, cy, w, ux, uy):
        hw, hh = w / 2 + 4, 24
        t = min(hw / abs(ux) if ux else 1e9, hh / abs(uy) if uy else 1e9)
        return cx + ux * t, cy + uy * t
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    sx, sy = edge(x1, y1, _kg_w(a), ux, uy)
    ex, ey = edge(x2, y2, _kg_w(b), -ux, -uy)
    return sx, sy, ex, ey


def _kg_node(d, name, dx, fill_stops=None, text_stops=None, op_stops=None):
    x, y = KG_NODES[name]
    x += dx
    w = _kg_w(name)
    fa = f' {d.a(fill_stops)}' if fill_stops else ""
    ta = f' {d.a(text_stops)}' if text_stops else ""
    g = f'<g {d.a(op_stops)}>' if op_stops else "<g>"
    return (g + f'<rect x="{x - w / 2:g}" y="{y - 20}" width="{w}" height="40" rx="20" fill="{W}" stroke="{N}" stroke-width="2.5"{fa}/>'
            + f'<text x="{x:g}" y="{y + 1}" text-anchor="middle" class="tn"{ta}>{name}</text></g>')


def _kg_edge(d, a, b, rel, dx, line_stops=None, op_stops=None, marker="ah"):
    sx, sy, ex, ey = _kg_clip(a, b, dx)
    la = f' {d.a(line_stops)}' if line_stops else ""
    g = f'<g {d.a(op_stops)}>' if op_stops else "<g>"
    mx, my = (sx + ex) / 2, (sy + ey) / 2
    return (g + f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{S}" stroke-width="2.5" '
            f'marker-end="url(#{d.id(marker)})"{la}/>'
            + f'<rect x="{mx - len(rel) * 7 - 8:.1f}" y="{my - 11:.1f}" width="{len(rel) * 14 + 16}" height="22" rx="6" fill="{W}"/>'
            + f'<text x="{mx:.1f}" y="{my + 1:.1f}" text-anchor="middle" class="tk">{rel}</text></g>')


_KG_CSS = "& .tk{font-size:13px;font-weight:700;fill:#55555C}& .tx{font-size:14px;fill:#26262B}& .th{font-size:13px;font-weight:800;fill:#E8002D}"


def kg_build():
    """청크 → LLM 추출 → 세 묶음 → 그래프에 노드 · 연결이 하나씩 생긴다 (같은 대상은 하나로)."""
    d = _D("kb", 15)
    DX = 560
    starts = [4, 32, 60]
    s = ""
    # 왼쪽: 청크 세 개
    for i, (pg, l1, l2) in enumerate(KG_CHUNKS):
        y = 20 + i * 132
        t0 = starts[i]
        s += (f'<rect x="10" y="{y}" width="330" height="104" rx="12" fill="{W}" stroke="{G}" stroke-width="2.5" '
              + d.a([(0, f"stroke:{G}"), (t0, f"stroke:{G}"), (t0 + 1, f"stroke:{O}"), (t0 + 20, f"stroke:{O}"), (t0 + 21, f"stroke:{G}"), (100, f"stroke:{G}")]) + "/>")
        s += _t(28, y + 24, f"청크 {i + 1} · {pg}", "th", "start")
        s += _t(28, y + 54, l1, "tx", "start") + _t(28, y + 78, l2, "tx", "start")
    # 가운데: LLM 추출
    s += f'<rect x="372" y="150" width="150" height="64" rx="14" fill="{N}" ' + d.a(
        [(0, f"fill:{N}")] + sum([[(t + 9, f"fill:{N}"), (t + 10, f"fill:{O}"), (t + 13, f"fill:{O}"), (t + 14, f"fill:{N}")] for t in starts], []) + [(100, f"fill:{N}")]) + "/>"
    s += _t(447, 172, "LLM 추출", "tw") + _t(447, 196, "대상 · 관계", "tw", extra='style="font-size:13px;font-weight:600"')
    s += _t(447, 250, "(대상, 관계, 대상)", "tk") + _t(447, 272, "세 묶음으로 저장", "tk")
    s += _t(447, 300, "+ 근거 청크 · 페이지", "th")
    for i, t0 in enumerate(starts):
        cy = 72 + i * 132
        s += _move(d, [(0, 340, cy, 0), (t0 + 2, 340, cy, 0), (t0 + 3, 340, cy, 1), (t0 + 9, 372, 182, 1), (t0 + 10, 372, 182, 0), (100, 372, 182, 0)])
        s += _move(d, [(0, 522, 182, 0), (t0 + 13, 522, 182, 0), (t0 + 14, 522, 182, 1), (t0 + 19, 600, 182, 1), (t0 + 20, 600, 182, 0), (100, 600, 182, 0)])
    # 오른쪽: 그래프가 자란다
    first = {}
    for a, b, _, c in KG_EDGES:
        for n in (a, b):
            first.setdefault(n, c)
    for a, b, rel, c in KG_EDGES:
        t = starts[c] + 15
        s += _kg_edge(d, a, b, rel, DX, op_stops=[(0, "opacity:0"), (t, "opacity:0"), (t + 3, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")])
    for n, c in first.items():
        t = starts[c] + 14
        s += _kg_node(d, n, DX, op_stops=[(0, "opacity:0"), (t, "opacity:0"), (t + 2, "opacity:1"), (96, "opacity:1"), (100, "opacity:0")])
    # 같은 대상은 하나로: 청크 2 · 3에서 「소프트 에러」가 다시 나오면 기존 노드에 연결
    x, y = KG_NODES["소프트 에러"]
    for t0 in starts[1:]:
        t = t0 + 15
        s += (f'<rect x="{x + DX - 70}" y="{y - 26}" width="140" height="52" rx="26" fill="none" stroke="{O}" stroke-width="3" '
              + d.a([(0, "opacity:0"), (t, "opacity:0"), (t + 1, "opacity:1"), (t + 8, "opacity:1"), (t + 9, "opacity:0"), (100, "opacity:0")]) + "/>")
    s += (f'<g {d.a([(0, "opacity:0"), (46, "opacity:0"), (47, "opacity:1"), (82, "opacity:1"), (83, "opacity:0"), (100, "opacity:0")])}>'
          + _t(x + DX, y - 44, "같은 대상 → 기존 노드에 연결", "th") + "</g>")
    return d.svg(1160, 430, s, _KG_CSS)


def kg_answer():
    """질문 → 시작 노드 → 1 hop → 2 hop → 관계 + 원문을 LLM 입력에 → 출처가 붙은 답."""
    d = _D("ka", 15)
    DX = 0
    on_nodes = {"RAM": 10, "소프트 에러": 10, "패리티": 24, "ECC": 24, "스크러빙": 24, "추가 메모리 비트": 40, "주기적 읽기 부하": 40}
    on_edges = {("소프트 에러", "RAM"): 18, ("패리티", "소프트 에러"): 24, ("ECC", "소프트 에러"): 24, ("스크러빙", "소프트 에러"): 24,
                ("ECC", "추가 메모리 비트"): 40, ("스크러빙", "주기적 읽기 부하"): 40}
    s = ""
    for a, b, rel, _ in KG_EDGES:
        t = on_edges.get((a, b))
        if t:
            s += _kg_edge(d, a, b, rel, DX, line_stops=[(0, f"stroke:{S}"), (t, f"stroke:{S}"), (t + 2, f"stroke:{O}"), (95, f"stroke:{O}"), (99, f"stroke:{S}")])
        else:
            s += _kg_edge(d, a, b, rel, DX, op_stops=[(0, "opacity:1"), (8, "opacity:1"), (10, "opacity:.25"), (95, "opacity:.25"), (99, "opacity:1")])
    for n in KG_NODES:
        t = on_nodes.get(n)
        if t is None:
            s += _kg_node(d, n, DX, op_stops=[(0, "opacity:1"), (8, "opacity:1"), (10, "opacity:.3"), (95, "opacity:.3"), (99, "opacity:1")])
        elif t == 10:
            s += _kg_node(d, n, DX, fill_stops=[(0, f"fill:{W};stroke:{N}"), (t, f"fill:{W};stroke:{N}"), (t + 2, f"fill:{O};stroke:{O}"), (95, f"fill:{O};stroke:{O}"), (99, f"fill:{W};stroke:{N}")],
                          text_stops=[(0, f"fill:{N}"), (t, f"fill:{N}"), (t + 2, f"fill:{W}"), (95, f"fill:{W}"), (99, f"fill:{N}")])
        else:
            s += _kg_node(d, n, DX, fill_stops=[(0, f"fill:{W};stroke:{N}"), (t, f"fill:{W};stroke:{N}"), (t + 2, f"fill:#FFF0F3;stroke:{O}"), (95, f"fill:#FFF0F3;stroke:{O}"), (99, f"fill:{W};stroke:{N}")])
    # 단계 표시 (그래프 아래)
    for i, (txt, t) in enumerate([("① 질문에서 시작 노드 찾기", 10), ("② 1 hop · 방법 찾기", 24), ("③ 2 hop · 제약 찾기", 40)]):
        s += (f'<g {d.a([(0, "opacity:.25"), (t, "opacity:.25"), (t + 2, "opacity:1"), (95, "opacity:1"), (99, "opacity:.25")])}>'
              + _t(40 + i * 200, 440, txt, "th", "start") + "</g>")
    # 오른쪽: 질문 → LLM 입력 → LLM → 답
    X = 690
    s += f'<rect x="{X}" y="8" width="460" height="62" rx="14" fill="{G}" fill-opacity=".45"/>'
    s += _t(X + 18, 28, "질문", "th", "start") + _t(X + 18, 52, "RAM 소프트 에러를 검출 · 완화하는 방법과 제약은?", "tx", "start")
    s += f'<rect x="{X}" y="92" width="460" height="150" rx="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
    s += _t(X + 18, 114, "LLM 입력 = 질문 + 그래프에서 모은 근거", "tn", "start")
    rows = [("관계 경로", "패리티 · ECC · 스크러빙 → 소프트 에러", 56), ("관계 경로", "ECC → 추가 비트 · 스크러빙 → 읽기 부하", 60),
            ("원문 근거", "청크 2 (p.7) · 청크 3 (p.9) 원문", 64), ("지침", "근거에 있는 내용만 · 출처 표시", 66)]
    for i, (k, v, t) in enumerate(rows):
        y = 144 + i * 26
        s += (f'<g {d.a([(0, "opacity:0"), (t, "opacity:0"), (t + 2, "opacity:1"), (96, "opacity:1"), (99, "opacity:0")])}>'
              + _t(X + 18, y, k, "th", "start") + _t(X + 100, y, v, "tx", "start") + "</g>")
    s += _move(d, [(0, 520, 250, 0), (54, 520, 250, 0), (55, 520, 250, 1), (62, X, 170, 1), (63, X, 170, 0), (100, X, 170, 0)])
    s += _move(d, [(0, 330, 300, 0), (56, 330, 300, 0), (57, 330, 300, 1), (64, X, 200, 1), (65, X, 200, 0), (100, X, 200, 0)])
    s += f'<line x1="{X + 230}" y1="244" x2="{X + 230}" y2="262" stroke="{N}" stroke-width="2.5" marker-end="url(#{d.id("ah")})"/>'
    s += (f'<rect x="{X + 170}" y="266" width="120" height="38" rx="19" fill="{N}" '
          + d.a([(0, f"fill:{N}"), (70, f"fill:{N}"), (71, f"fill:{O}"), (78, f"fill:{O}"), (79, f"fill:{N}"), (100, f"fill:{N}")]) + "/>")
    s += _t(X + 230, 286, "LLM", "tw")
    s += f'<line x1="{X + 230}" y1="306" x2="{X + 230}" y2="322" stroke="{N}" stroke-width="2.5" marker-end="url(#{d.id("ah")})"/>'
    s += f'<rect x="{X}" y="326" width="460" height="124" rx="14" fill="#FFF0F3" stroke="{O}" stroke-width="2.5" ' + d.a(
        [(0, "opacity:0"), (79, "opacity:0"), (81, "opacity:1"), (96, "opacity:1"), (99, "opacity:0")]) + "/>"
    ans = [("검출", "패리티 · 정정은 불가 (p.7)", 81), ("검출 + 정정", "ECC · 추가 메모리 비트 필요 (p.7)", 84),
           ("완화", "스크러빙 · 주기적 읽기 부하 (p.9)", 87)]
    s += (f'<g {d.a([(0, "opacity:0"), (79, "opacity:0"), (81, "opacity:1"), (96, "opacity:1"), (99, "opacity:0")])}>'
          + _t(X + 18, 348, "답 · 관계를 따라 모은 근거로", "th", "start") + "</g>")
    for i, (k, v, t) in enumerate(ans):
        y = 376 + i * 26
        s += (f'<g {d.a([(0, "opacity:0"), (t, "opacity:0"), (t + 2, "opacity:1"), (96, "opacity:1"), (99, "opacity:0")])}>'
              + _t(X + 18, y, k, "tn", "start") + _t(X + 128, y, v, "tx", "start") + "</g>")
    return d.svg(1160, 456, s, _KG_CSS)


# ── 다음 토큰 예측 (posco-dx explain.e2에서 가져와 이 덱 색으로) ─────────────
def next_token(prefix, steps, end_label, uid="nt"):
    """단계마다 (후보, 확률) 목록 · 첫 후보를 골라 문장에 붙인다. 값은 설명용."""
    import json
    data = json.dumps({"prefix": prefix, "steps": steps}, ensure_ascii=False)
    full = "".join([prefix] + [st[0][0] for st in steps])
    last = steps[-1]
    rows = "".join(
        f'<div class="gar{" pick" if i == 0 else ""}"><span class="gaw">{w}</span><span class="gab"><i style="width:{p*100:.0f}%"></i></span><span class="gap">{p:.2f}</span></div>'
        for i, (w, p) in enumerate(last + [("", 0)] * (max(len(st) for st in steps) - len(last))))
    css = ("<style>.ga{background:#F6F6F8;border:1px solid #E4E4E9;border-radius:14px;padding:22px 24px;display:flex;flex-direction:column;gap:14px}"
           ".ga .gas{font-size:26px;font-weight:800;color:#26262B;min-height:40px;line-height:1.4;word-break:keep-all}"
           ".ga .gacur{display:inline-block;width:3px;height:26px;background:#E8002D;margin-left:4px;vertical-align:-4px;animation:gablink 1s steps(1) infinite}"
           "@keyframes gablink{50%{opacity:0}}"
           ".ga .galab{font-size:13px;font-weight:800;color:#6B6B73}.ga .galab span{font-weight:400}"
           ".ga .garows{display:flex;flex-direction:column;gap:8px}"
           ".ga .gar{display:grid;grid-template-columns:120px 1fr 48px;align-items:center;gap:10px;font-size:18px;color:#26262B}"
           ".ga .gaw{text-align:right;font-weight:800;font-family:var(--mono,monospace)}"
           ".ga .gab{height:22px;background:#fff;border-radius:5px;overflow:hidden}"
           ".ga .gab i{display:block;height:100%;background:#DCDCE1;border-radius:5px;transition:width .5s ease,background .3s}"
           ".ga .gar.pick .gab i{background:#E8002D}.ga .gar.pick .gaw{color:#E8002D}"
           ".ga .gap{font-family:var(--mono,monospace);font-size:14px;color:#55555C}"
           ".ga .gaend{display:inline-block;vertical-align:5px;margin-left:12px;font-size:13px;font-weight:800;color:#fff;background:#26262B;border-radius:999px;padding:5px 12px;opacity:0;transition:opacity .3s}"
           ".ga .gaend.on{opacity:1}@media print{.ga .gaend{opacity:1}.ga .gacur{display:none}}</style>")
    js = '''<script>
(function () {
  const box = document.getElementById('%s');
  if (!box) return;
  const D = JSON.parse(box.dataset.gen);
  const txt = box.querySelector('.gatxt'), rows = box.querySelectorAll('.gar'), end = box.querySelector('.gaend');
  let step = 0, words = [D.prefix], phase = 0, timer = null;
  function show(i) {
    const st = D.steps[i];
    rows.forEach((r, k) => {
      const c = st[k];
      r.classList.remove('pick');
      r.style.visibility = c ? 'visible' : 'hidden';
      if (!c) return;
      r.querySelector('.gaw').textContent = c[0];
      r.querySelector('.gap').textContent = c[1].toFixed(2);
      r.querySelector('i').style.width = (c[1] * 100) + '%%';
    });
  }
  function tick() {
    if (box.offsetParent === null) return;
    if (step >= D.steps.length) {
      end.classList.add('on');
      if (++phase > 4) { step = 0; phase = 0; words = [D.prefix]; txt.textContent = D.prefix; end.classList.remove('on'); show(0); }
      return;
    }
    if (phase === 0) { show(step); phase = 1; return; }
    if (phase === 1) { rows[0].classList.add('pick'); phase = 2; return; }
    words.push(D.steps[step][0][0]); txt.textContent = words.join('');
    step += 1; phase = 0;
  }
  window.addEventListener('beforeprint', () => {
    clearInterval(timer); const n = D.steps.length - 1;
    txt.textContent = [D.prefix].concat(D.steps.map(st => st[0][0])).join('');
    show(n); rows[0].classList.add('pick'); end.classList.add('on');
  });
  txt.textContent = D.prefix; show(0);
  rows.forEach(r => r.querySelector('i').style.width = '0%%');
  timer = setInterval(tick, 900);
})();
</script>''' % uid
    return (css + f'''<div class="ga" id="{uid}" data-gen='{data}'>
  <div class="gas"><span class="gatxt">{full}</span><span class="gacur"></span><span class="gaend">{end_label}</span></div>
  <div class="galab">다음 토큰 후보 <span>(설명용 확률)</span></div>
  <div class="garows">{rows}</div>
</div>''' + js)
