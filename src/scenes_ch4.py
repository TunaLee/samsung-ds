"""Ch4 장면 — 자동화(Apps Script · 트리거 · 두 도구)."""
from art import *  # noqa


def _sw(d, w=4, c=N):
    """선 하나(움직임 선 등)."""
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def _hand_p(x, y):
    return f'<circle cx="{x}" cy="{y}" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>'


def _hand_r(x, y, r=10):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G}" stroke="{N}" stroke-width="3"/>'


def _bubble(x, y, w, h, tx, ty, side="L"):
    """빈 말풍선. (tx,ty) 는 꼬리 끝."""
    bx = x + 26 if side == "L" else x + w - 46
    return (f'<path d="M{bx} {y+h-2} L{tx} {ty} L{bx+22} {y+h-2} Z" fill="{W}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2.4}" fill="{W}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{bx+3}" y="{y+h-8}" width="16" height="10" fill="{W}"/>'
            f'<circle cx="{x+w/2-22}" cy="{y+h/2}" r="6" fill="{G}"/><circle cx="{x+w/2}" cy="{y+h/2}" r="6" fill="{G}"/>'
            f'<circle cx="{x+w/2+22}" cy="{y+h/2}" r="6" fill="{G}"/>')


def _land(x, y, w, h, sun=None):
    """창·액자 안 풍경: 하늘 흰색, 언덕 회색."""
    return (f'<path d="M{x} {y+h*.72} Q{x+w*.25} {y+h*.5} {x+w*.5} {y+h*.7} Q{x+w*.75} {y+h*.56} {x+w} {y+h*.66} L{x+w} {y+h} L{x} {y+h} Z" fill="{G}"/>'
            f'<path d="M{x} {y+h*.86} Q{x+w*.4} {y+h*.74} {x+w} {y+h*.88} L{x+w} {y+h} L{x} {y+h} Z" fill="{N}" fill-opacity=".25"/>')


# ── ① 사진과 창문 ───────────────────────────────────────
def photo_window():
    # 액자 (정적)
    px, py, pw, ph = 150, 220, 250, 200
    photo = f'''
<line x1="{px+40}" y1="{py-4}" x2="{px+pw/2}" y2="{py-34}" stroke="{N}" stroke-width="3"/>
<line x1="{px+pw-40}" y1="{py-4}" x2="{px+pw/2}" y2="{py-34}" stroke="{N}" stroke-width="3"/>
<circle cx="{px+pw/2}" cy="{py-36}" r="6" fill="{N}"/>
<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}" rx="6" fill="{N}"/>
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{W}"/>
{_land(px, py, pw, ph)}
<circle cx="{px+70}" cy="{py+62}" r="26" fill="{G}" stroke="{N}" stroke-width="4"/>
<path d="M{px+150} {py+52} q12 -18 30 -8 q14 -10 26 6 q14 2 8 16 l-62 0 q-14 -4 -2 -14 z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
'''
    # 창문 (움직임)
    wx, wy, ww, wh = 560, 220, 250, 200
    arc = f'M{wx+24} {wy+128} Q{wx+ww/2} {wy-40} {wx+ww-24} {wy+128}'
    ghosts = "".join(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{G}" opacity="{op}"/>'
                     for cx, cy, op in ((wx+52, wy+86, .35), (wx+88, wy+56, .6)))
    window = f'''
<rect x="{wx}" y="{wy}" width="{ww}" height="{ph}" fill="{W}"/>
{_land(wx, wy, ww, wh)}
<path d="{arc}" stroke="{N}" stroke-width="3" fill="none" stroke-dasharray="6 8" stroke-linecap="round"/>
{ghosts}
<circle cx="{wx+138}" cy="{wy+40}" r="26" fill="{G}" stroke="{N}" stroke-width="4"/>
<path d="M{wx+170} {wy+44} l10 -6 M{wx+168} {wy+28} l12 -12" stroke="{N}" stroke-width="3" stroke-linecap="round"/>
<path d="M{wx+170} {wy+100} q12 -18 30 -8 q14 -10 26 6 q14 2 8 16 l-62 0 q-14 -4 -2 -14 z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
{_sw(f"M{wx+120} {wy+104} L{wx+156} {wy+104} M{wx+132} {wy+116} L{wx+162} {wy+116}", 3)}
<rect x="{wx-14}" y="{wy-14}" width="{ww+28}" height="{wh+28}" rx="4" fill="none" stroke="{O}" stroke-width="16"/>
<line x1="{wx+ww/2}" y1="{wy}" x2="{wx+ww/2}" y2="{wy+wh}" stroke="{O}" stroke-width="9"/>
<line x1="{wx}" y1="{wy+wh/2}" x2="{wx+ww}" y2="{wy+wh/2}" stroke="{O}" stroke-width="9"/>
<rect x="{wx-34}" y="{wy+wh+14}" width="{ww+68}" height="14" rx="4" fill="{N}"/>
'''
    s = .7
    py0 = 665 - 152 * s
    p = person(1065, py0, s,
               extra_back=parm(54, -140, 70, -30),
               extra_front=parm(-54, -140, -14, -176, -70, -110), legs=True)
    r = robot(900, 665, 1.15, rarm(-44, -86, -90, -170, -96, -120) + rarm(44, -86, 70, -36), mouth="grin")
    return floor(800, 665, 420) + photo + window + p + r


# ── ② 창문을 벽에 건다 ───────────────────────────────────
def hang_window():
    fx, fy, fw, fh = 640, 200, 270, 190
    bars = [(0.55,), (0.8,), (0.4,), (0.95,), (0.7,)]
    chart = "".join(
        f'<rect x="{fx+40+i*42}" y="{fy+fh-30-h*110}" width="26" height="{h*110}" rx="3" fill="{N if i==3 else G}"/>'
        for i, (h,) in enumerate(bars))
    frame = f'''
<circle cx="{fx+fw/2}" cy="{fy-34}" r="7" fill="{N}"/>
<path d="M{fx+40} {fy} L{fx+fw/2} {fy-34} L{fx+fw-40} {fy}" stroke="{N}" stroke-width="3" fill="none"/>
<g transform="rotate(-3 {fx+fw/2} {fy+fh/2})">
<rect x="{fx-14}" y="{fy-14}" width="{fw+28}" height="{fh+28}" rx="6" fill="{N}"/>
<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{W}"/>
{chart}
<line x1="{fx+28}" y1="{fy+fh-24}" x2="{fx+fw-24}" y2="{fy+fh-24}" stroke="{N}" stroke-width="3"/>
{lines(fx+28, fx+120, [fy+22], G, 6)}
</g>'''
    # 시트 상자 (격자)
    bx, by, bw, bh = 560, 520, 170, 130
    grid = "".join(f'<line x1="{bx+i*bw/5}" y1="{by}" x2="{bx+i*bw/5}" y2="{by+bh}" stroke="{N}" stroke-width="2.5"/>' for i in range(1, 5))
    grid += "".join(f'<line x1="{bx}" y1="{by+j*bh/4}" x2="{bx+bw}" y2="{by+j*bh/4}" stroke="{N}" stroke-width="2.5"/>' for j in range(1, 4))
    box = f'''
<path d="M{bx} {by} L{bx+24} {by-22} L{bx+bw+24} {by-22} L{bx+bw} {by} Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M{bx+bw} {by} L{bx+bw+24} {by-22} L{bx+bw+24} {by+bh-22} L{bx+bw} {by+bh} Z" fill="{N}"/>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{W}" stroke="{N}" stroke-width="4"/>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh/4}" fill="{G}" stroke="{N}" stroke-width="4"/>
{grid}
<rect x="{bx+bw/2-6}" y="{by-18}" width="30" height="10" rx="3" fill="{N}"/>'''
    cable = f'''
<path d="M{fx+40} {fy+fh+10} C{fx+20} {fy+fh+80} {fx+120} {fy+fh+90} 712 486 S 680 470 {bx+bw/2+12} {by-30}" stroke="{O}" stroke-width="8" fill="none" stroke-linecap="round"/>
<rect x="{bx+bw/2}" y="{by-42}" width="24" height="22" rx="4" fill="{O}" stroke="{N}" stroke-width="3"/>'''
    rb = robot(790, 662, 1.0, rarm(-44, -86, -118, -168, -100, -100) + rarm(44, -86, 66, -34), mouth="grin")
    s = .78
    p = person(1050, 665 - 152 * s, s,
               extra_back=parm(54, -140, 84, -24, 80, -80),
               extra_front=parm(-54, -140, -150, -210, -120, -150), legs=True)
    hammer = (f'<g transform="translate({1050+84*s},{665-152*s-24*s}) rotate(20)">'
              f'<rect x="-6" y="-8" width="12" height="70" rx="4" fill="{N}"/>'
              f'<rect x="-26" y="54" width="52" height="22" rx="4" fill="{G}" stroke="{N}" stroke-width="3"/></g>'
              + _hand_p(1050 + 84 * s, 665 - 152 * s - 24 * s))
    return floor(880, 662, 335) + frame + box + cable + rb + p + hammer


# ── ③ 메뉴판 카드 갈아 끼우기 ─────────────────────────────
def _card(x, y, w, h, stroke=N, sw=3):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{W}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<rect x="{x+8}" y="{y+8}" width="{w*.32}" height="{h-16}" rx="3" fill="{G}"/>'
            + lines(x + w * .32 + 18, x + w - 10, [y + h * .34, y + h * .66], G, 5))


def menu_board():
    bx, by, bw, bh = 570, 190, 392, 290
    cw, ch, gx, gy = 96, 64, 22, 20
    cards = []
    empty = (2, 2)
    for r in range(3):
        for c in range(3):
            x, y = bx + 30 + c * (cw + gx) + 0, by + 34 + r * (ch + gy)
            if (c, r) == empty:
                cards.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="4" fill="{N}" fill-opacity=".15" stroke="{N}" stroke-width="2" stroke-dasharray="6 5"/>')
            else:
                cards.append(_card(x, y, cw, ch))
    ex, ey = bx + 30 + 2 * (cw + gx), by + 34 + 2 * (ch + gy)
    board = f'''
<circle cx="{bx+bw/2}" cy="{by-22}" r="6" fill="{N}"/>
<path d="M{bx+60} {by} L{bx+bw/2} {by-22} L{bx+bw-60} {by}" stroke="{N}" stroke-width="3" fill="none"/>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{N}"/>
<rect x="{bx+14}" y="{by+14}" width="{bw-28}" height="{bh-28}" rx="4" fill="{G}" fill-opacity=".35"/>
{"".join(cards)}'''
    new = _card(ex - 26, ey - 10, cw, ch, O, 5)
    s = .76
    pxx = 1060
    wy = 665 - 152 * s
    hx, hy = ex + cw - 14, ey + 30
    # 손 위치를 회사원 좌표로
    lx, ly = (hx - pxx) / s, (hy - wy) / s
    old = (f'<g transform="rotate(-14 1170 560)">' + _card(1120, 530, cw * .9, ch * .9) + '</g>')
    p = person(pxx, wy, s,
               extra_front=parm(-54, -140, lx, ly, -90, -150) + parm(54, -140, (1150 - pxx) / s, (565 - wy) / s, 110, -70),
               legs=True)
    # 새 카드 상자 (발치)
    k = f'''
<rect x="1170" y="590" width="92" height="70" rx="4" fill="{G}" stroke="{N}" stroke-width="4"/>
{"".join(f'<rect x="{1178+i*9}" y="{566+i*3}" width="64" height="40" rx="3" fill="{W}" stroke="{N}" stroke-width="2.5"/>' for i in range(3))}
<rect x="1170" y="590" width="92" height="70" rx="4" fill="{G}" stroke="{N}" stroke-width="4"/>
<line x1="1180" y1="606" x2="1252" y2="606" stroke="{N}" stroke-width="2"/>'''
    return floor(900, 662, 355) + board + k + p + old + new + _hand_p(hx, hy)


# ── ④ 알람과 세 상자 ────────────────────────────────────
def _crate(x, y, w=110, h=96):
    return (f'<path d="M{x} {y} L{x+16} {y-14} L{x+w+16} {y-14} L{x+w} {y} Z" fill="{N}"/>'
            f'<path d="M{x+w} {y} L{x+w+16} {y-14} L{x+w+16} {y+h-14} L{x+w} {y+h} Z" fill="{N}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{G}" stroke="{N}" stroke-width="4"/>'
            f'<line x1="{x}" y1="{y+22}" x2="{x+w}" y2="{y+22}" stroke="{N}" stroke-width="3"/>')


def alarm():
    cx, cy = 664, 270
    clock = f'''
<path d="M{cx-34} {cy+36} L{cx-46} {cy+56} M{cx+34} {cy+36} L{cx+46} {cy+56}" stroke="{N}" stroke-width="7" stroke-linecap="round"/>
<circle cx="{cx-34}" cy="{cy-40}" r="17" fill="{O}" stroke="{N}" stroke-width="4"/>
<circle cx="{cx+34}" cy="{cy-40}" r="17" fill="{O}" stroke="{N}" stroke-width="4"/>
<line x1="{cx}" y1="{cy-56}" x2="{cx}" y2="{cy-66}" stroke="{N}" stroke-width="4"/>
<circle cx="{cx}" cy="{cy}" r="50" fill="{O}" stroke="{N}" stroke-width="5"/>
<circle cx="{cx}" cy="{cy}" r="36" fill="{W}"/>
<path d="M{cx} {cy} L{cx} {cy-24} M{cx} {cy} L{cx+18} {cy+8}" stroke="{N}" stroke-width="5" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="4" fill="{N}"/>
{_sw(f"M{cx-70} {cy-40} Q{cx-82} {cy-14} {cx-70} {cy+12} M{cx-88} {cy-52} Q{cx-104} {cy-14} {cx-88} {cy+24}")}
{_sw(f"M{cx+70} {cy-40} Q{cx+82} {cy-14} {cx+70} {cy+12} M{cx+88} {cy-52} Q{cx+104} {cy-14} {cx+88} {cy+24}")}
<rect x="{cx-80}" y="{cy+56}" width="160" height="12" rx="4" fill="{N}"/>
<path d="M{cx-56} {cy+68} L{cx-56} {cy+104} L{cx-20} {cy+68} Z M{cx+56} {cy+68} L{cx+56} {cy+104} L{cx+20} {cy+68} Z" fill="{N}"/>'''
    xs = [790, 950, 1110]
    top = 540
    boxes = "".join(_crate(x, top) for x in xs)
    # 상자 위 물건
    x1 = xs[0] + 55
    env = f'''<g transform="rotate(-6 {x1} {top-36})">
<rect x="{x1-44}" y="{top-66}" width="88" height="58" rx="4" fill="{W}" stroke="{N}" stroke-width="4"/>
<path d="M{x1-44} {top-64} L{x1} {top-30} L{x1+44} {top-64}" stroke="{N}" stroke-width="4" fill="none" stroke-linejoin="round"/></g>'''
    x2 = xs[1] + 55
    doc = f'''<rect x="{x2-34}" y="{top-92}" width="68" height="86" rx="4" fill="{W}" stroke="{N}" stroke-width="4"/>
{lines(x2-22, x2+22, [top-74, top-60, top-46, top-32], G, 5)}'''
    x3 = xs[2] + 55
    plane = f'''<g transform="translate({x3+14},{top-96}) rotate(-18)">
<path d="M-42 4 L44 -20 L-8 26 Z" fill="{W}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M-8 26 L4 -6 L44 -20" stroke="{N}" stroke-width="3" fill="none" stroke-linejoin="round"/>
<path d="M-8 26 L-4 8" stroke="{N}" stroke-width="3"/></g>
<path d="M{x3-20} {top-6} Q{x3-30} {top-40} {x3-8} {top-60}" stroke="{N}" stroke-width="3" fill="none" stroke-dasharray="4 6" stroke-linecap="round"/>'''
    arrows = f'''
<path d="M{cx+70} {cy+20} Q{cx+180} {cy+20} {x1-6} {top-90}" stroke="{N}" stroke-width="4" fill="none" stroke-dasharray="8 8" stroke-linecap="round"/>
<path d="M{x1-22} {top-100} L{x1-4} {top-86} L{x1+2} {top-110}" stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
{"".join(f'<path d="M{a} {top-50} L{b-10} {top-50}" stroke="{N}" stroke-width="4" stroke-dasharray="5 6" stroke-linecap="round"/><path d="M{b-20} {top-60} L{b-8} {top-50} L{b-20} {top-40}" stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for a, b in ((x1+54, x2-42), (x2+44, x3-58)))}'''
    rb = robot(690, 662, 1.05, rarm(44, -86, 108, -120, 86, -70) + rarm(-44, -86, -78, -40), mouth="grin")
    move = _sw("M600 520 L566 520 M596 548 L556 548 M604 576 L570 576", 4)
    return floor(910, 664, 365) + clock + move + boxes + env + doc + plane + arrows + rb


# ── ⑤ 두 가지 도구 ─────────────────────────────────────
def _gear(x, y, r, fill, teeth=8):
    t = "".join(f'<rect x="{x-r*.18}" y="{y-r-9}" width="{r*.36}" height="18" rx="3" fill="{fill}" stroke="{N}" stroke-width="3" transform="rotate({i*360/teeth} {x} {y})"/>' for i in range(teeth))
    return t + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{N}" stroke-width="3.5"/><circle cx="{x}" cy="{y}" r="{r*.32}" fill="{W}" stroke="{N}" stroke-width="3"/>'


def two_tools():
    # 왼쪽: 맞춤 제작
    bench = f'''
<rect x="210" y="550" width="420" height="16" rx="5" fill="{N}"/>
<rect x="226" y="566" width="388" height="58" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="226" y="566" width="14" height="96" fill="{N}"/><rect x="600" y="566" width="14" height="96" fill="{N}"/>'''
    device = f'''<g transform="translate(0,30)">
<path d="M300 520 L300 450 Q300 430 320 430 L360 430 L372 404 L420 404 L432 430 L452 430 L452 520 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="396" cy="384" r="10" fill="{N}"/><line x1="396" y1="384" x2="396" y2="404" stroke="{N}" stroke-width="5"/>
{_gear(352, 480, 24, O)}
{_gear(414, 466, 14, W, 6)}
<rect x="318" y="444" width="16" height="14" rx="3" fill="{N}"/>
<path d="M452 480 L462 480 L462 500 L452 500" fill="{W}" stroke="{N}" stroke-width="3"/></g>'''
    ruler = f'''<rect x="516" y="537" width="84" height="13" rx="2" fill="{W}" stroke="{N}" stroke-width="3"/>
{"".join(f'<line x1="{x}" y1="537" x2="{x}" y2="{543 if i%2 else 546}" stroke="{N}" stroke-width="2"/>' for i, x in enumerate(range(524, 596, 8)))}'''
    wrench = (f'<line x1="470" y1="520" x2="490" y2="500" stroke="{N}" stroke-width="11" stroke-linecap="round"/>'
              f'<g transform="translate(468,521) rotate(130)"><path d="M-15 -4 Q-16 -22 -4 -26 L-4 -12 L4 -12 L4 -26 Q16 -22 15 -4 Q8 6 0 6 Q-8 6 -15 -4 Z" fill="{N}"/></g>')
    rb = robot(560, 640, 1.2, mouth="grin")
    arms = (f'<g transform="translate(560,640) scale(1.2)">'
            + rarm(-44, -86, (490 - 560) / 1.2, (500 - 640) / 1.2, -66, -110)
            + rarm(44, -86, (606 - 560) / 1.2, (538 - 640) / 1.2, 62, -96) + '</g>')
    part = _gear(256, 537, 9, W, 6)
    s = .68
    wy = 665 - 152 * s
    bp_x, bp_y = 140, 330
    bp = (f'<rect x="{bp_x}" y="{bp_y}" width="120" height="90" rx="4" fill="{W}" stroke="{N}" stroke-width="4"/>'
          + "".join(f'<line x1="{bp_x+x}" y1="{bp_y+4}" x2="{bp_x+x}" y2="{bp_y+86}" stroke="{G}" stroke-width="2"/>' for x in range(20, 120, 20))
          + "".join(f'<line x1="{bp_x+4}" y1="{bp_y+y}" x2="{bp_x+116}" y2="{bp_y+y}" stroke="{G}" stroke-width="2"/>' for y in range(18, 90, 18))
          + f'<path d="M{bp_x+24} {bp_y+68} L{bp_x+24} {bp_y+40} L{bp_x+50} {bp_y+40} L{bp_x+58} {bp_y+26} L{bp_x+80} {bp_y+26} L{bp_x+86} {bp_y+40} L{bp_x+98} {bp_y+40} L{bp_x+98} {bp_y+68} Z" fill="none" stroke="{N}" stroke-width="3"/>'
          + f'<circle cx="{bp_x+48}" cy="{bp_y+56}" r="8" fill="none" stroke="{N}" stroke-width="2.5"/>')
    p1x = 110
    p = person(p1x, wy, s,
               extra_front=parm(54, -140, (bp_x + 18 - p1x) / s, (bp_y + 80 - wy) / s, 90, -100)
               + parm(-54, -140, -70, -30), legs=True)
    left = floor(330, 665, 290) + rb + bench + device + ruler + wrench + part + arms + p + bp + _hand_p(bp_x + 18, bp_y + 80)
    # 로봇 손: 렌치 쥔 손
    # 오른쪽: 말로 주문
    s2 = .7
    wy2 = 665 - 152 * s2
    p2 = person(745, wy2, s2, extra_back=parm(-54, -140, -70, -30),
                extra_front=parm(54, -140, 118, -196, 110, -110), legs=True)
    bub = _bubble(800, 200, 170, 96, 790, 342, "L")
    bx0, by0, bs = 850, 566, 62
    blocks = ""
    for i in range(3):
        x = bx0 + i * bs
        blocks += (f'<rect x="{x}" y="{by0}" width="{bs}" height="{bs*.75}" rx="4" fill="{G}" stroke="{N}" stroke-width="4"/>'
                   f'<rect x="{x+bs*.3}" y="{by0-12}" width="{bs*.4}" height="12" rx="2" fill="{G}" stroke="{N}" stroke-width="3"/>')
    hx, hy = bx0 + 3 * bs + 10, by0 - 66
    held = (f'<rect x="{hx}" y="{hy}" width="{bs}" height="{bs*.75}" rx="4" fill="{O}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{hx+bs*.3}" y="{hy-12}" width="{bs*.4}" height="12" rx="2" fill="{O}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M{hx+12} {hy+bs*.75+12} L{hx+12} {hy+bs*.75+26} M{hx+bs-12} {hy+bs*.75+12} L{hx+bs-12} {hy+bs*.75+26}" stroke="{N}" stroke-width="3" stroke-linecap="round"/>')
    rb2 = robot(1195, 662, 1.05, rarm(-44, -86, (hx + bs + 4 - 1195) / 1.05, (hy + 24 - 662) / 1.05, -70, -60) + rarm(44, -86, 66, -40), mouth="smile")
    plat = f'<rect x="830" y="{by0+bs*.75}" width="300" height="14" rx="4" fill="{N}"/>'
    right = floor(990, 665, 280) + p2 + bub + plat + blocks + rb2 + held + _hand_r(hx + bs + 4, hy + 24)
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── ⑥ 도미노 ──────────────────────────────────────────
def _check(x, y, s=1):
    return (f'<rect x="{x-14*s}" y="{y-14*s}" width="{28*s}" height="{28*s}" rx="{6*s}" fill="{W}" stroke="{O}" stroke-width="3"/>'
            f'<path d="M{x-8*s} {y} L{x-2*s} {y+7*s} L{x+9*s} {y-7*s}" stroke="{O}" stroke-width="{4.5*s}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def domino():
    base = 650
    bh = 112
    xs = list(range(310, 960, 60))

    def blk(x, rot=0):
        return (f'<g transform="rotate({rot} {x+15} {base})">'
                f'<path d="M{x+30} {base-bh} L{x+40} {base-bh-8} L{x+40} {base-8} L{x+30} {base}" fill="{N}"/>'
                f'<path d="M{x} {base-bh} L{x+10} {base-bh-8} L{x+40} {base-bh-8} L{x+30} {base-bh} Z" fill="{N}"/>'
                f'<rect x="{x}" y="{base-bh}" width="30" height="{bh}" rx="3" fill="{G}" stroke="{N}" stroke-width="4"/>'
                f'<circle cx="{x+15}" cy="{base-26}" r="4" fill="{N}"/></g>')
    blocks = "".join(blk(x) for x in xs)
    cy = base - 74
    checks = "".join(_check(x + 15, cy) for x in xs[:4])
    s = .74
    pxx = 470
    wy = 665 - 152 * s
    hx, hy = xs[4] + 15, cy
    p = person(pxx, wy, s,
               extra_front=parm(54, -140, (hx + 10 - pxx) / s, (hy + 6 - wy) / s, 130, -120) + parm(-54, -140, -80, -30),
               legs=True)
    sticker = _check(hx, hy)
    bub = _bubble(560, 200, 170, 96, 530, 336, "L")
    # 로봇이 막 세우는 블록
    nx = xs[-1] + 60
    new = f'<g transform="translate(0,-26)">{blk(nx)}</g>'
    rb = robot(1110, 662, 1.12, rarm(-44, -86, (nx + 34 - 1110) / 1.12, (base - 80 - 662) / 1.12, -70, -60)
               + rarm(44, -86, 70, -36))
    return (floor(740, 660, 480) + p + blocks + checks + sticker + _hand_p(hx + 10, hy + 6) + bub
            + rb + new + _hand_r(nx + 34, base - 80))


# ── ⑦ 날아간 편지 ──────────────────────────────────────
def envelope_fly():
    wx, wy, ww, wh = 960, 196, 240, 220
    window = f'''
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{G}" fill-opacity=".35"/>
<path d="M{wx} {wy+wh*.78} Q{wx+ww*.4} {wy+wh*.62} {wx+ww} {wy+wh*.74} L{wx+ww} {wy+wh} L{wx} {wy+wh} Z" fill="{G}"/>
<rect x="{wx-12}" y="{wy-12}" width="{ww+24}" height="{wh+24}" rx="4" fill="none" stroke="{N}" stroke-width="12"/>
<path d="M{wx} {wy} L{wx-60} {wy+24} L{wx-60} {wy+wh-24} L{wx} {wy+wh}" fill="{W}" fill-opacity=".85" stroke="{N}" stroke-width="6" stroke-linejoin="round"/>
<line x1="{wx-30}" y1="{wy+14}" x2="{wx-30}" y2="{wy+wh-14}" stroke="{N}" stroke-width="4"/>
<rect x="{wx-30}" y="{wy+wh+12}" width="{ww+60}" height="14" rx="4" fill="{N}"/>'''
    ex, ey = 1110, 270
    env = f'''<g transform="rotate(-18 {ex} {ey})">
<rect x="{ex-40}" y="{ey-26}" width="80" height="52" rx="4" fill="{O}" stroke="{N}" stroke-width="4"/>
<path d="M{ex-40} {ey-24} L{ex} {ey+6} L{ex+40} {ey-24}" stroke="{N}" stroke-width="4" fill="none" stroke-linejoin="round"/></g>
{_sw(f"M{ex-64} {ey+40} L{ex-112} {ey+60} M{ex-70} {ey+16} L{ex-130} {ey+34} M{ex-58} {ey+64} L{ex-96} {ey+82}", 4)}
<path d="M640 436 Q720 120 {ex-70} {ey+20}" stroke="{N}" stroke-width="3" fill="none" stroke-dasharray="6 9" stroke-linecap="round"/>'''
    desk = f'''
<path d="M570 520 L860 520 L876 544 L556 544 Z" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="556" y="544" width="320" height="14" fill="{N}"/>
<rect x="574" y="558" width="12" height="104" fill="{N}"/><rect x="846" y="558" width="12" height="104" fill="{N}"/>'''
    laptop = f'''
<path d="M590 446 L676 446 L684 516 L598 516 Z" fill="{N}"/>
<path d="M598 454 L670 454 L676 508 L604 508 Z" fill="{G}"/>
<rect x="580" y="514" width="150" height="10" rx="4" fill="{N}"/>
<ellipse cx="704" cy="514" rx="16" ry="6" fill="{G}" stroke="{N}" stroke-width="3"/>'''
    s = .82
    pxx = 760
    face = (f'<rect x="-14" y="-194" width="28" height="12" fill="{W}"/>'
            f'<ellipse cx="0" cy="-186" rx="7" ry="9" fill="{N}"/>'
            f'<path d="M-52 -262 L-62 -278 M-30 -272 L-34 -292 M44 -266 L56 -282" stroke="{N}" stroke-width="5" stroke-linecap="round"/>')
    p = person(pxx, 524, s,
               extra_front=face + parm(-54, -140, (704 - pxx) / s, (506 - 524) / s, -70, -40)
               + parm(54, -140, (880 - pxx) / s, (330 - 524) / s, 120, -170))
    rb = robot(1110, 662, 1.0, rarm(-44, -86, -70, -30) + rarm(44, -86, 96, -196, 96, -110), mouth="grin")
    wave = _sw("M1222 420 Q1236 436 1232 456 M1238 408 Q1258 432 1250 464", 4)
    return floor(910, 664, 365) + window + desk + p + laptop + rb + wave + env
