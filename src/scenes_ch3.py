"""Ch3 장면."""
from art import *  # noqa
import math


def _quad(p00, p10, p01, p11):
    """사각형 안의 (u, v) → 좌표. p00 왼위, p10 오른위, p01 왼아래, p11 오른아래."""
    def f(u, v):
        x = (p00[0] * (1 - u) + p10[0] * u) * (1 - v) + (p01[0] * (1 - u) + p11[0] * u) * v
        y = (p00[1] * (1 - u) + p10[1] * u) * (1 - v) + (p01[1] * (1 - u) + p11[1] * u) * v
        return x, y
    return f


def _poly(f, u1, v1, u2, v2, fill, stroke="none", sw=0):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (f(u1, v1), f(u2, v1), f(u2, v2), f(u1, v2)))
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke != "none" else ""
    return f'<polygon points="{pts}" fill="{fill}"{st}/>'


def _pline(f, u1, u2, v, color=G, w=5):
    (x1, y1), (x2, y2) = f(u1, v), f(u2, v)
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'


def _bubble(cx, cy, rx, ry, tx, ty):
    """빈 말풍선. (tx, ty) 쪽으로 꼬리."""
    bx = cx + (tx - cx) * .45
    return (f'<path d="M{bx-12} {cy+ry*.6} L{tx} {ty} L{bx+14} {cy+ry*.55} Z" fill="{W}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{W}" stroke="{N}" stroke-width="4"/>'
            f'<path d="M{bx-10} {cy+ry*.55} L{bx+12} {cy+ry*.5}" stroke="{W}" stroke-width="8"/>')


# ── ① 채팅 vs 작업대 ─────────────────────────────────────
def chat_vs_workbench():
    # 왼쪽: 카페 테이블에 마주 앉아 말풍선을 주고받는다
    left = f'''
{floor(330, 662, 270)}
<rect x="96" y="590" width="128" height="14" rx="5" fill="{N}"/>
<rect x="104" y="604" width="10" height="52" fill="{N}"/><rect x="206" y="604" width="10" height="52" fill="{N}"/>
{person(165, 590, .82, extra_back=parm(-54, -140, -66, -20, -74, -80), extra_front=parm(54, -140, 128, -86, 110, -136))}
<rect x="226" y="574" width="34" height="76" rx="10" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="134" y="560" width="126" height="36" rx="12" fill="{G}" stroke="{N}" stroke-width="3"/>
<ellipse cx="256" cy="654" rx="26" ry="8" fill="{N}"/>
{robot(492, 655, 1.0, rarm(44, -86, 62, -30) + rarm(-44, -86, -82, -128, -70, -96))}
<ellipse cx="330" cy="526" rx="118" ry="22" fill="{G}" stroke="{N}" stroke-width="4"/>
<rect x="323" y="548" width="14" height="100" fill="{N}"/>
<ellipse cx="330" cy="652" rx="46" ry="8" fill="{N}"/>
<path d="M276 498 L304 498 L301 524 L279 524 Z" fill="{W}" stroke="{N}" stroke-width="3"/>
<path d="M304 504 Q314 510 302 518" stroke="{N}" stroke-width="3" fill="none"/>
<path d="M356 498 L384 498 L381 524 L359 524 Z" fill="{W}" stroke="{N}" stroke-width="3"/>
<path d="M356 504 Q346 510 358 518" stroke="{N}" stroke-width="3" fill="none"/>
<circle cx="270" cy="520" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>
<circle cx="410" cy="527" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>
{_bubble(258, 270, 74, 46, 210, 352)}
{_bubble(476, 352, 62, 38, 488, 410)}'''

    # 오른쪽: 작업대 위에 펼친 큰 문서 한 장을 함께 손본다
    bench = [(752, 474), (1188, 474), (712, 602), (1228, 602)]
    doc = _quad((812, 484), (1128, 484), (790, 590), (1150, 590))
    pmark = doc(.36, .58)
    pen_tip = (pmark[0] - 40, pmark[1] + 4)
    right = f'''
{floor(970, 676, 290)}
{person(830, 572, .86)}
{robot(1110, 580, 1.15, rarm(44, -86, 66, -60, hand=False))}
<polygon points="{bench[0][0]},{bench[0][1]} {bench[1][0]},{bench[1][1]} {bench[3][0]},{bench[3][1]} {bench[2][0]},{bench[2][1]}" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<rect x="712" y="602" width="516" height="16" rx="4" fill="{N}"/>
<rect x="732" y="618" width="14" height="58" fill="{N}"/><rect x="1194" y="618" width="14" height="58" fill="{N}"/>
{_poly(doc, 0, 0, 1, 1, W, N, 3.5)}
{"".join(_pline(doc, .07, .93 if i % 3 else .6, v, G, 6) for i, v in enumerate((.14, .27, .40)))}
{_poly(doc, .07, .52, .62, .66, "none")}
{_pline(doc, .07, .93, .78, G, 6)}{_pline(doc, .07, .55, .9, G, 6)}
{_pline(doc, .66, .93, .58, G, 6)}
<ellipse cx="{pmark[0]:.0f}" cy="{pmark[1]:.0f}" rx="96" ry="13" fill="none" stroke="{O}" stroke-width="5"/>
{_pline(doc, .1, .62, .58, G, 6)}
<g transform="translate(830,572) scale(.86)">{parm(54, -140, 92, -40, 104, -112, hand=False)}{parm(-54, -140, -40, -30, -96, -60)}</g>
<line x1="{pen_tip[0]-10:.0f}" y1="{pen_tip[1]-48:.0f}" x2="{pen_tip[0]:.0f}" y2="{pen_tip[1]:.0f}" stroke="{O}" stroke-width="7" stroke-linecap="round"/>
<circle cx="{pen_tip[0]-8:.0f}" cy="{pen_tip[1]-30:.0f}" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>
<g transform="translate(1110,580) scale(1.15)">{rarm(-44, -86, -78, -42, -80, -80)}</g>'''
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── ② 벽화 ────────────────────────────────────────────
def _mural(x, y):
    """460x300 벽화. 산 두 개, 해, 나무."""
    return f'''
<rect x="{x}" y="{y}" width="460" height="300" fill="{W}" stroke="{N}" stroke-width="5"/>
<circle cx="{x+380}" cy="{y+70}" r="32" fill="{G}" stroke="{N}" stroke-width="4"/>
{"".join(f'<line x1="{x+380+44*c}" y1="{y+70+44*s}" x2="{x+380+58*c}" y2="{y+70+58*s}" stroke="{N}" stroke-width="4" stroke-linecap="round"/>' for c, s in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)))}
<path d="M{x+170} {y+262} L{x+305} {y+128} L{x+440} {y+262} Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M{x+20} {y+262} L{x+135} {y+96} L{x+270} {y+262} Z" fill="{N}"/>
<path d="M{x+110} {y+132} L{x+135} {y+96} L{x+160} {y+132} L{x+146} {y+124} L{x+135} {y+134} L{x+122} {y+124} Z" fill="{W}"/>
<rect x="{x+56}" y="{y+214}" width="12" height="48" fill="{N}"/>
<circle cx="{x+62}" cy="{y+196}" r="28" fill="{G}" stroke="{N}" stroke-width="4"/>
<line x1="{x+6}" y1="{y+262}" x2="{x+454}" y2="{y+262}" stroke="{N}" stroke-width="4"/>'''


def _stain(cx, cy):
    return (f'<path d="M{cx-14} {cy-8} Q{cx-6} {cy-20} {cx+8} {cy-14} Q{cx+22} {cy-10} {cx+16} {cy+4} '
            f'Q{cx+20} {cy+16} {cx+2} {cy+14} Q{cx-16} {cy+18} {cx-18} {cy+4} Q{cx-24} {cy-2} {cx-14} {cy-8} Z" fill="{N}" fill-opacity=".55"/>')


def mural():
    lx, rx, wy = 60, 760, 200
    sx, sy = 230, 140  # 얼룩 위치 (벽화 안)
    left = f'''
{floor(290, 668, 270)}
{_mural(lx, wy)}
<path d="M{lx+160} {wy+3} L{lx+457} {wy+3} L{lx+457} {wy+297} L{lx+168} {wy+297} Q{lx+152} {wy+250} {lx+166} {wy+200} Q{lx+150} {wy+150} {lx+164} {wy+100} Q{lx+150} {wy+50} {lx+160} {wy+3} Z" fill="{G}"/>
{"".join(f'<line x1="{lx+190+i*58}" y1="{wy+20}" x2="{lx+190+i*58}" y2="{wy+280}" stroke="{W}" stroke-width="6" stroke-opacity=".7" stroke-linecap="round"/>' for i in range(5))}
<rect x="{lx}" y="{wy}" width="460" height="300" fill="none" stroke="{N}" stroke-width="5"/>
{robot(470, 662, 1.12, rarm(-44, -86, -78, -150, -86, -100) + rarm(44, -86, 84, -118, 92, -80), mouth="wavy")}
<line x1="382" y1="494" x2="400" y2="360" stroke="{N}" stroke-width="6" stroke-linecap="round"/>
<path d="M400 360 L400 340 L392 340" stroke="{N}" stroke-width="5" fill="none" stroke-linejoin="round"/>
<rect x="352" y="318" width="80" height="26" rx="10" fill="{G}" stroke="{N}" stroke-width="4"/>
<circle cx="383" cy="495" r="11" fill="{G}" stroke="{N}" stroke-width="3"/>
<path d="M548 418 L566 404 M556 436 L578 432 M540 404 L546 384" stroke="{N}" stroke-width="4" stroke-linecap="round"/>'''
    px, pyw = 1185, 668 - 152 * .72
    tip = (rx + 300, wy + 165)
    hx, hy = px - 82, pyw - 112   # 손 위치 = 팔 끝 (-114, -156) * .72
    ang = math.degrees(math.atan2(hy - tip[1], hx - tip[0]))
    ln = math.hypot(hx - tip[0], hy - tip[1])
    brush = (f'<g transform="translate({tip[0]},{tip[1]}) rotate({ang:.1f})">'
             f'<line x1="34" y1="0" x2="{ln+14:.0f}" y2="0" stroke="{N}" stroke-width="8" stroke-linecap="round"/>'
             f'<rect x="22" y="-7" width="16" height="14" rx="2" fill="{G}" stroke="{N}" stroke-width="2.5"/>'
             f'<path d="M22 -7 Q8 -7 -2 0 Q8 7 22 7 Z" fill="{O}" stroke="{N}" stroke-width="2.5" stroke-linejoin="round"/></g>')
    right = f'''
{floor(990, 668, 270)}
{_mural(rx, wy)}
<circle cx="{tip[0]}" cy="{tip[1]}" r="12" fill="{O}" fill-opacity=".85"/>
{person(px, pyw, .72, extra_back=parm(54, -140, 62, -30, 70, -90), extra_front=parm(-54, -140, -114, -156, -110, -90), legs=True)}
{brush}
<circle cx="{hx}" cy="{hy}" r="9" fill="{W}" stroke="{N}" stroke-width="3"/>'''
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── ③ 업무 지시 ────────────────────────────────────────
def _card(x, y, kind):
    c = f'<rect x="{x}" y="{y}" width="124" height="150" rx="8" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
    c += f'<circle cx="{x+62}" cy="{y+4}" r="9" fill="{O}" stroke="{N}" stroke-width="2.5"/>'
    mx, my = x + 62, y + 80
    if kind == 0:  # 역할: 사람
        c += (f'<circle cx="{mx}" cy="{my-20}" r="20" fill="{N}"/>'
              f'<path d="M{mx-36} {my+40} Q{mx-36} {my+6} {mx} {my+6} Q{mx+36} {my+6} {mx+36} {my+40} Z" fill="{N}"/>')
    elif kind == 1:  # 맥락: 지도와 핀
        c += (f'<path d="M{x+16} {my-26} L{x+46} {my-36} L{x+78} {my-26} L{x+108} {my-36} L{x+108} {my+42} L{x+78} {my+52} L{x+46} {my+42} L{x+16} {my+52} Z" fill="{G}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
              f'<path d="M{x+46} {my-36} L{x+46} {my+42} M{x+78} {my-26} L{x+78} {my+52}" stroke="{N}" stroke-width="2.5"/>'
              f'<path d="M{mx} {my+18} Q{mx-20} {my-4} {mx-20} {my-18} A20 20 0 0 1 {mx+20} {my-18} Q{mx+20} {my-4} {mx} {my+18} Z" fill="{N}"/>'
              f'<circle cx="{mx}" cy="{my-18}" r="7" fill="{W}"/>')
    elif kind == 2:  # 작업: 체크 목록
        for i in range(3):
            yy = my - 34 + i * 32
            c += f'<rect x="{x+18}" y="{yy-10}" width="20" height="20" rx="3" fill="none" stroke="{N}" stroke-width="3"/>' + lines(x + 50, x + 104, [yy], G, 7)
            if i < 2:
                c += f'<path d="M{x+22} {yy} L{x+27} {yy+6} L{x+36} {yy-6}" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    else:  # 형식: 문서 배치
        c += (f'<rect x="{x+22}" y="{my-50}" width="80" height="16" rx="3" fill="{N}"/>'
              f'<rect x="{x+22}" y="{my-26}" width="36" height="40" rx="3" fill="{G}" stroke="{N}" stroke-width="2.5"/>'
              + lines(x + 66, x + 102, [my - 20, my - 6, my + 8], G, 5)
              + f'<rect x="{x+22}" y="{my+24}" width="80" height="26" rx="3" fill="none" stroke="{N}" stroke-width="2.5"/>'
              f'<line x1="{x+62}" y1="{my+24}" x2="{x+62}" y2="{my+50}" stroke="{N}" stroke-width="2.5"/>'
              f'<line x1="{x+22}" y1="{my+37}" x2="{x+102}" y2="{my+37}" stroke="{N}" stroke-width="2.5"/>')
    return c


def briefing():
    board = f'''
<rect x="590" y="160" width="640" height="220" rx="10" fill="{W}" stroke="{N}" stroke-width="5"/>
<rect x="600" y="170" width="620" height="200" rx="4" fill="{G}" fill-opacity=".35"/>
<rect x="640" y="380" width="10" height="290" fill="{N}"/><rect x="1170" y="380" width="10" height="290" fill="{N}"/>
<rect x="840" y="374" width="140" height="10" rx="4" fill="{N}"/>
{"".join(_card(624 + i * 150, 196, i) for i in range(4))}'''
    py = 676 - 152 * .82
    folder = f'''
<g transform="rotate(-6 905 520)">
<rect x="850" y="482" width="112" height="80" rx="6" fill="{G}" stroke="{N}" stroke-width="4"/>
<rect x="858" y="474" width="96" height="70" fill="{W}" stroke="{N}" stroke-width="2.5"/>
{lines(870, 940, [490, 504, 518], G, 4)}
<path d="M850 498 L962 498 L962 562 L850 562 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M850 498 L850 488 L884 488 L890 498" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
</g>'''
    badge = (f'<path d="M-24 -98 L0 -64 L24 -98" stroke="{N}" stroke-width="3" fill="none"/>'
             f'<rect x="-12" y="-66" width="24" height="30" rx="3" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<rect x="-7" y="-60" width="14" height="10" rx="2" fill="{N}"/><line x1="-6" y1="-44" x2="6" y2="-44" stroke="{G}" stroke-width="3"/>')
    return f'''
{board}
{floor(910, 680, 330)}
{robot(1080, 676, .92, badge + rarm(44, -86, 70, -30) + rarm(-44, -86, -128, -168, -100, -100), mouth="grin")}
{person(740, py, .82, extra_back=parm(-54, -140, -70, -30, -74, -90), extra_front=parm(54, -140, 180, -36, 150, -130), legs=True)}
{folder}
<circle cx="888" cy="521" r="12" fill="{W}" stroke="{N}" stroke-width="3"/>
<circle cx="962" cy="521" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>'''


# ── ④ 사진 한 장 ───────────────────────────────────────
def _bars(x, y, w, h, hs, fill, stroke=N):
    n = len(hs)
    bw = w / (n * 1.6)
    gap = (w - bw * n) / (n + 1)
    out = f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{N}" stroke-width="3"/>'
    for i, k in enumerate(hs):
        bx = x + gap + i * (bw + gap)
        out += f'<rect x="{bx:.1f}" y="{y+h-h*k:.1f}" width="{bw:.1f}" height="{h*k:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
    return out


def photo():
    old = [.35, .6, .45, .8]
    new = [.9, .3, .75, .25]
    mon = f'''
<rect x="770" y="460" width="420" height="16" rx="6" fill="{N}"/>
<rect x="790" y="476" width="14" height="200" fill="{N}"/><rect x="1156" y="476" width="14" height="200" fill="{N}"/>
<rect x="960" y="420" width="40" height="42" fill="{N}"/><rect x="920" y="452" width="120" height="10" rx="4" fill="{N}"/>
<rect x="830" y="190" width="300" height="236" rx="14" fill="{N}"/>
<rect x="846" y="206" width="268" height="204" rx="4" fill="{W}"/>
{lines(866, 950, [228], G, 7)}
{_bars(870, 244, 220, 150, new, O)}'''
    ph = (900, 440)  # 사진 왼위
    pic = f'''
<g transform="rotate(-4 {ph[0]+70} {ph[1]+80})">
<rect x="{ph[0]}" y="{ph[1]}" width="140" height="164" rx="4" fill="{W}" stroke="{N}" stroke-width="4"/>
<rect x="{ph[0]+12}" y="{ph[1]+12}" width="116" height="110" fill="{N}"/>
<rect x="{ph[0]+18}" y="{ph[1]+18}" width="104" height="98" fill="{W}"/>
{_bars(ph[0]+26, ph[1]+34, 88, 74, old, G)}
</g>'''
    ly = 680 - 152 * .78
    return f'''
{mon}
{floor(900, 682, 340)}
{person(700, ly, .78, extra_back=parm(-54, -140, -70, -30, -74, -90), extra_front=parm(54, -140, 262, -32, 170, -40, hand=False), legs=True)}
{person(1130, ly, .78, extra_back=parm(54, -140, 70, -30, 74, -90), legs=True)}
{pic}
<circle cx="{ph[0]+4}" cy="{ph[1]+96}" r="11" fill="{W}" stroke="{N}" stroke-width="3"/>
<g transform="translate(1130,{ly}) scale(.78)">{parm(-54, -140, -112, -78, -80, -40)}</g>'''


# ── ⑤ 받는 사람 ────────────────────────────────────────
def _prop(kind, x, y):
    if kind == 0:  # 악수
        return (f'<path d="M{x-80} {y+16} L{x-34} {y+2}" stroke="{N}" stroke-width="22" stroke-linecap="round"/>'
                f'<path d="M{x+80} {y+16} L{x+34} {y+2}" stroke="{N}" stroke-width="22" stroke-linecap="round"/>'
                f'<rect x="{x-34}" y="{y-16}" width="68" height="34" rx="16" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
                f'<path d="M{x-30} {y-8} Q{x-6} {y-24} {x+12} {y-8}" stroke="{N}" stroke-width="3.5" fill="{W}" stroke-linecap="round"/>'
                + "".join(f'<line x1="{x+u}" y1="{y-2}" x2="{x+u}" y2="{y+14}" stroke="{N}" stroke-width="3" stroke-linecap="round"/>' for u in (2, 12, 22)))
    if kind == 1:  # 막대그래프 액자
        return (f'<rect x="{x-48}" y="{y-38}" width="96" height="76" rx="4" fill="{W}" stroke="{N}" stroke-width="5"/>'
                + _bars(x - 34, y - 26, 68, 52, [.35, .6, .85], N))
    # 기울어진 저울
    return (f'<rect x="{x-4}" y="{y-30}" width="8" height="64" fill="{N}"/>'
            f'<path d="M{x-26} {y+38} L{x+26} {y+38} L{x} {y+26} Z" fill="{N}"/>'
            f'<g transform="rotate(-16 {x} {y-30})">'
            f'<line x1="{x-56}" y1="{y-30}" x2="{x+56}" y2="{y-30}" stroke="{N}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{x-56} {y-30} L{x-74} {y} M{x-56} {y-30} L{x-38} {y} M{x+56} {y-30} L{x+38} {y} M{x+56} {y-30} L{x+74} {y}" stroke="{N}" stroke-width="2.5"/>'
            f'<path d="M{x-78} {y} L{x-34} {y} Q{x-56} {y+18} {x-78} {y} Z" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M{x+34} {y} L{x+78} {y} Q{x+56} {y+18} {x+34} {y} Z" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{x-68}" y="{y-14}" width="24" height="14" fill="{N}"/></g>'
            f'<circle cx="{x}" cy="{y-30}" r="6" fill="{N}"/>')


def _proposal(cx, hl):
    """책상 위 한 장짜리 제안서. hl = 0 맨 위, 1 가운데 표, 2 아래."""
    f = _quad((cx - 66, 470), (cx + 66, 470), (cx - 80, 600), (cx + 80, 600))
    out = _poly(f, 0, 0, 1, 1, W, N, 3.5)
    blocks = [(.08, .06, .92, .2), (.08, .38, .92, .64), (.08, .78, .92, .93)]
    for i, (u1, v1, u2, v2) in enumerate(blocks):
        out += _poly(f, u1, v1, u2, v2, O if i == hl else G)
    # 표 칸
    for u in (.36, .64):
        (x1, y1), (x2, y2) = f(u, .38), f(u, .64)
        out += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{W}" stroke-width="3"/>'
    out += _pline(f, .08, .92, .51, W, 3)
    out += _pline(f, .08, .92, .28, G, 5) + _pline(f, .08, .7, .7, G, 5)
    return out


def audience():
    cxs = [213, 640, 1067]
    out = [f'<line x1="427" y1="190" x2="427" y2="690" stroke="{G}" stroke-width="3"/>',
           f'<line x1="853" y1="190" x2="853" y2="690" stroke="{G}" stroke-width="3"/>']
    for i, cx in enumerate(cxs):
        out.append(floor(cx, 676, 180))
        out.append(_prop(i, cx, 230))
        out.append(person(cx, 500, .74,
                          ))
        out.append(f'<path d="M{cx-150} 462 L{cx+150} 462 L{cx+180} 612 L{cx-180} 612 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
                   f'<rect x="{cx-180}" y="612" width="360" height="16" rx="4" fill="{N}"/>'
                   f'<rect x="{cx-166}" y="628" width="14" height="46" fill="{N}"/><rect x="{cx+152}" y="628" width="14" height="46" fill="{N}"/>')
        out.append(_proposal(cx, i))
        out.append(f'<g transform="translate({cx},500) scale(.74)">{parm(-54, -140, -128, 24, -110, -60)}{parm(54, -140, 128, 24, 110, -60)}</g>')
    return "".join(out)
