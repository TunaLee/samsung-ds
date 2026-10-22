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
                   title="Context Window", sub="= 한 요청의 장바구니", turn="요청"):
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
