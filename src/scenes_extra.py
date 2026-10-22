"""추가 장면: 입력 양식 · 사실과 추정 · 계산기 확인 · 초안 검토."""
from art import *  # noqa


HAPPY = (f'<circle cx="-13" cy="-204" r="6" fill="{W}"/><circle cx="13" cy="-204" r="6" fill="{W}"/>'
         f'<path d="M-19 -202 Q-13 -210 -7 -202 M7 -202 Q13 -210 19 -202" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>')


def _table(x0, x1, y, legs_to):
    return (f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="16" rx="6" fill="{N}"/>'
            f'<rect x="{x0+18}" y="{y+16}" width="14" height="{legs_to-y-16}" fill="{N}"/>'
            f'<rect x="{x1-32}" y="{y+16}" width="14" height="{legs_to-y-16}" fill="{N}"/>')


def _arrow_dash(x1, y1, x2, y2, color=N, op=.55):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    l, w = 13, .55
    p1 = (x2 - l * math.cos(a - w), y2 - l * math.sin(a - w))
    p2 = (x2 - l * math.cos(a + w), y2 - l * math.sin(a + w))
    return (f'<g stroke="{color}" stroke-opacity="{op}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{x1} {y1} L{x2} {y2}" stroke-dasharray="8 9"/>'
            f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}"/></g>')


# ── 메모 대신 주문서 ──────────────────────────────────────
def _postit(x, y, rot, s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-22 -22 L22 -22 L22 10 L10 22 L-22 22 Z" fill="{G}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M22 10 L10 10 L10 22" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
            f'<line x1="-12" y1="-8" x2="10" y2="-8" stroke="{N}" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="-12" y1="2" x2="2" y2="2" stroke="{N}" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/></g>')


def _chat(x, y, rot, s=1, flip=False):
    t = "M-14 16 L-22 30 L-2 16" if not flip else "M14 16 L22 30 L2 16"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="{t}" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="-32" y="-18" width="64" height="36" rx="14" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M-14 16 L-2 16" stroke="{W}" stroke-width="4"/>'
            f'{lines(-20, 18, [-6], G, 4)}{lines(-20, 6, [6], G, 4)}</g>')


def _crumple(x, y, rot, s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-24 -16 L-8 -24 L4 -18 L22 -22 L26 -4 L20 8 L24 22 L4 18 L-10 24 L-26 14 L-20 0 Z" '
            f'fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M-8 -24 L-4 -2 L-20 0 M-4 -2 L20 8 M-4 -2 L4 18" stroke="{G}" stroke-width="2.5" fill="none"/></g>')


def _whoosh(x, y, dx, dy):
    return (f'<path d="M{x} {y} l{dx} {dy} M{x+dy*.5} {y-dx*.5+8} l{dx*.6} {dy*.6}" '
            f'stroke="{N}" stroke-opacity=".45" stroke-width="3.5" stroke-linecap="round"/>')


def forms_inlet():
    # 왼쪽: 사방에서 날아와 책상에 쌓이는 메모
    pile = "".join([
        _crumple(150, 498, 8), _chat(214, 500, -6), _postit(296, 500, 10), _crumple(372, 502, -14),
        _postit(178, 466, -16), _chat(258, 462, 12, .95, True), _crumple(330, 466, 20, .9),
        _postit(222, 430, 6, .9), _chat(300, 428, -10, .85), _crumple(262, 396, -6, .8),
    ])
    flying = "".join([
        _postit(96, 238, -22), _whoosh(60, 214, -26, -14),
        _chat(250, 214, 8, .9), _whoosh(240, 186, -2, -1),
        _crumple(400, 236, 25, .9), _whoosh(432, 210, 22, -14),
        _chat(120, 340, -12, .9, True), _whoosh(78, 336, -30, 0),
        _postit(440, 330, 18, .85), _whoosh(470, 306, 26, -10),
        _crumple(52, 434, -10, .8), _whoosh(30, 420, -14, -16),
    ])
    left = f'''
{floor(300, 668, 270)}
{_table(110, 420, 520, 666)}
{pile}
{flying}
{robot(520, 666, 1.1, rarm(-44, -86, -62, -176, -96, -118) + rarm(44, -86, 70, -36), mouth="wavy")}
<path d="M596 410 Q604 424 598 434 Q590 424 596 410 Z" fill="{W}" stroke="{N}" stroke-width="3"/>
<path d="M454 404 L440 392 M450 422 L432 420" stroke="{N}" stroke-width="3.5" stroke-linecap="round"/>'''

    # 오른쪽: 벽의 입력 양식 → 표에 한 줄씩
    fx, fy, fw = 678, 196, 160
    fields = []
    for i in range(7):
        y = fy + 40 + i * 40
        fields.append(lines(fx + 16, fx + 38, [y + 13], G, 6))
        fields.append(f'<rect x="{fx+48}" y="{y}" width="{fw-64}" height="26" rx="4" fill="{W}" stroke="{N}" stroke-width="2.5"/>')
        if i in (1, 4):
            fields.append(f'<path d="M{fx+fw-34} {y+10} L{fx+fw-22} {y+10} L{fx+fw-28} {y+17} Z" fill="{N}"/>'
                          f'<line x1="{fx+fw-40}" y1="{y+4}" x2="{fx+fw-40}" y2="{y+22}" stroke="{N}" stroke-width="2"/>')
    form = (f'<rect x="{fx}" y="{fy}" width="{fw}" height="336" rx="8" fill="{W}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{fx+2}" y="{fy+2}" width="{fw-4}" height="20" rx="6" fill="{G}"/>'
            f'<rect x="{fx+fw/2-18}" y="{fy-8}" width="36" height="16" rx="3" fill="{G}" stroke="{N}" stroke-width="2" transform="rotate(-4 {fx+fw/2} {fy})"/>'
            + "".join(fields))
    tx, ty, tw, rh, rows = 916, 196, 220, 24, 7
    cw = tw / 3
    grid = []
    for r in range(rows):
        y = ty + r * rh
        last = r == rows - 1
        for c in range(3):
            x = tx + c * cw
            f = N if r == 0 else (O if last else W)
            grid.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{rh}" fill="{f}" stroke="{N}" stroke-width="2.5"/>')
            if r > 0:
                grid.append(f'<line x1="{x+10}" y1="{y+rh/2}" x2="{x+cw-12-(c % 2)*16}" y2="{y+rh/2}" stroke="{W if last else G}" stroke-width="5" stroke-linecap="round"/>')
    arrow = (f'<path d="M848 330 L898 330" stroke="{O}" stroke-width="8" stroke-linecap="round"/>'
             f'<path d="M888 316 L906 330 L888 344 Z" fill="{O}" stroke="{O}" stroke-width="3" stroke-linejoin="round"/>')
    s = .7
    px, wy = 958, 666 - 152 * s
    tgx, tgy = 852, 448
    lx, ly = (tgx - px) / s, (tgy - wy) / s
    man = person(px, wy, s, extra_back=parm(54, -140, 70, -30, 74, -90),
                 extra_front=HAPPY + parm(-54, -140, lx, ly, -110, -170), legs=True)
    finger = f'<line x1="{tgx}" y1="{tgy}" x2="{tgx-14}" y2="{tgy-6}" stroke="{N}" stroke-width="6" stroke-linecap="round"/><circle cx="{tgx}" cy="{tgy}" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
    right = f'''
{floor(960, 668, 270)}
{form}
{arrow}
{"".join(grid)}
{man}{finger}
<path d="M1004 390 L1016 380 M1010 410 L1026 408" stroke="{N}" stroke-width="3.5" stroke-linecap="round"/>'''
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── 확인된 것과 추정 ──────────────────────────────────────
def _bar_card(x, y, rot, s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<rect x="-30" y="-40" width="60" height="80" rx="5" fill="{G}" stroke="{N}" stroke-width="3"/>'
            + "".join(f'<rect x="{-18+i*13}" y="{24-h}" width="9" height="{h}" fill="{N}"/>' for i, h in enumerate((20, 34, 26, 44)))
            + f'<line x1="-22" y1="25" x2="22" y2="25" stroke="{N}" stroke-width="2.5"/></g>')


def _cloud_card(x, y, rot, s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<rect x="-30" y="-40" width="60" height="80" rx="5" fill="{O}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M-14 6 Q-24 6 -22 -4 Q-24 -16 -10 -14 Q-6 -26 6 -20 Q20 -22 18 -8 Q26 0 16 6 Z" fill="{W}" stroke="{N}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<circle cx="-14" cy="16" r="4" fill="{W}" stroke="{N}" stroke-width="2"/><circle cx="-20" cy="26" r="2.5" fill="{W}" stroke="{N}" stroke-width="2"/></g>')


def _tray(x, y, w, h, dashed):
    da = ' stroke-dasharray="12 8"' if dashed else ""
    return (f'<path d="M{x} {y} L{x+w} {y} L{x+w-10} {y+h} L{x+10} {y+h} Z" fill="{W}" stroke="{N}" stroke-width="5" stroke-linejoin="round"{da}/>')


def fact_hypothesis():
    desk_y = 560
    lx, rx, tw, th = 590, 890, 150, 64
    ty = desk_y - th
    # 트레이 안 카드 (트레이 앞판보다 먼저)
    in_left = _bar_card(lx + 46, ty + 4, -6) + _bar_card(lx + 80, ty + 2, 4) + _bar_card(lx + 110, ty + 8, 10)
    in_right = _cloud_card(rx + 56, ty + 6, -8) + _cloud_card(rx + 98, ty + 4, 6)
    check = (f'<circle cx="{lx+tw/2}" cy="{ty+34}" r="18" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<path d="M{lx+tw/2-9} {ty+34} L{lx+tw/2-2} {ty+42} L{lx+tw/2+10} {ty+26}" stroke="{N}" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    mx, my = rx + tw / 2, ty + 34
    lens = (f'<circle cx="{mx}" cy="{my}" r="18" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<circle cx="{mx-3}" cy="{my-3}" r="7" fill="none" stroke="{N}" stroke-width="3.5"/>'
            f'<line x1="{mx+2}" y1="{my+2}" x2="{mx+9}" y2="{my+9}" stroke="{N}" stroke-width="4" stroke-linecap="round"/>')
    rs = 1.25
    bx, by = 812, 680
    held_gray = (708, 440)
    held_or = (916, 434)
    lxl, lyl = (held_gray[0] + 14 - bx) / rs, (held_gray[1] + 34 - by) / rs
    rxl, ryl = (held_or[0] - 14 - bx) / rs, (held_or[1] + 34 - by) / rs
    bot = robot(bx, by, rs, rarm(-44, -86, lxl, lyl, -80, -150, hand=False) + rarm(44, -86, rxl, ryl, 80, -150, hand=False))
    hands = (_bar_card(*held_gray, -10) + _cloud_card(*held_or, 8)
             + f'<circle cx="{held_gray[0]+14}" cy="{held_gray[1]+34}" r="12.5" fill="{G}" stroke="{N}" stroke-width="3.5"/>'
             + f'<circle cx="{held_or[0]-14}" cy="{held_or[1]+34}" r="12.5" fill="{G}" stroke="{N}" stroke-width="3.5"/>')
    s = .72
    px, wy = 1176, 680 - 152 * s
    tgx, tgy = 1052, 474
    plx, ply = (tgx - px) / s, (tgy - wy) / s
    man = person(px, wy, s, extra_back=parm(54, -140, 66, -30, 70, -90),
                 extra_front=parm(-54, -140, plx, ply, -110, -150), legs=True)
    finger = f'<line x1="{tgx}" y1="{tgy}" x2="{tgx-16}" y2="{tgy+8}" stroke="{N}" stroke-width="6" stroke-linecap="round"/><circle cx="{tgx}" cy="{tgy}" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
    return f'''
{floor(890, 682, 336)}
{bot}
<rect x="562" y="{desk_y}" width="506" height="18" rx="6" fill="{N}"/>
<rect x="580" y="{desk_y+18}" width="470" height="44" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="584" y="{desk_y+18}" width="14" height="{680-desk_y-18}" fill="{N}"/><rect x="1032" y="{desk_y+18}" width="14" height="{680-desk_y-18}" fill="{N}"/>
{in_left}{in_right}
{_tray(lx, ty, tw, th, False)}{_tray(rx, ty, tw, th, True)}
{check}{lens}
{hands}
{man}{finger}'''


# ── 새 계산기 확인 ────────────────────────────────────────
def calculator_test():
    desk_y = 560
    # 계산기
    cx0, cy0, cw, ch = 626, 428, 132, 140
    keys = "".join(f'<rect x="{cx0+12+i*28}" y="{cy0+58+j*20}" width="22" height="14" rx="4" fill="{G}" stroke="{N}" stroke-width="2"/>'
                   for i in range(4) for j in range(4))
    bar_w = 74
    calc = (f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="16" fill="{W}" stroke="{N}" stroke-width="5"/>'
            f'<rect x="{cx0+12}" y="{cy0+14}" width="{cw-24}" height="34" rx="6" fill="{G}" stroke="{N}" stroke-width="2.5"/>'
            f'<rect x="{cx0+cw-20-bar_w}" y="{cy0+27}" width="{bar_w}" height="16" rx="4" fill="{O}"/>'
            + keys)
    s = .95
    px, wy = 770, desk_y
    # 왼손(화면 왼쪽)은 계산기 옆을 받치고, 오른손 검지는 버튼을 누른다
    hold = ((cx0 + 2 - px) / s, (cy0 + 90 - wy) / s)
    press = ((cx0 + 82 - px) / s, (cy0 + 86 - wy) / s)
    man = person(px, wy, s,
                 extra_back=parm(-54, -140, hold[0], hold[1], -100, -60, hand=False))
    hand_l = f'<circle cx="{cx0+2}" cy="{cy0+90}" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="3"/>'
    arm_r = (f'<g transform="translate({px},{wy}) scale({s})">'
             + parm(54, -140, press[0] + 12, press[1] + 18, 80, -30, hand=True) + "</g>"
             + f'<line x1="{cx0+93}" y1="{cy0+103}" x2="{cx0+83}" y2="{cy0+88}" stroke="{N}" stroke-width="7" stroke-linecap="round"/>')
    taps = f'<path d="M{cx0+70} {cy0+76} L{cx0+64} {cy0+70} M{cx0+82} {cy0+72} L{cx0+82} {cy0+64} M{cx0+94} {cy0+76} L{cx0+100} {cy0+70}" stroke="{N}" stroke-width="3" stroke-linecap="round"/>'
    # 세워 둔 정답 카드
    kx, ky, kw, kh = 900, 418, 150, 120
    card = (f'<path d="M{kx+30} {ky+kh} L{kx+54} {desk_y} M{kx+kw-30} {ky+kh} L{kx+kw-54} {desk_y}" stroke="{N}" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="6" fill="{W}" stroke="{N}" stroke-width="4"/>'
            + lines(kx + 18, kx + kw - 18, [ky + 24], G, 7) + lines(kx + 18, kx + kw - 50, [ky + 46], G, 7)
            + lines(kx + 18, kx + 50, [ky + 78], G, 7)
            + f'<rect x="{kx+kw-30-bar_w}" y="{ky+70}" width="{bar_w}" height="16" rx="4" fill="{O}"/>'
            + f'<circle cx="{kx+kw-17}" cy="{ky+78}" r="9" fill="none" stroke="{O}" stroke-width="4"/>'
            + lines(kx + 18, kx + kw - 70, [ky + 102], G, 7))
    bot = robot(1160, 680, 1.1, rarm(-44, -86, -30, -112, -60, -86) + rarm(44, -86, 18, -114, 60, -86), mouth="grin")
    sparkle = f'<path d="M1080 410 L1066 398 M1076 432 L1058 430 M1240 410 L1254 398 M1244 432 L1262 430" stroke="{N}" stroke-width="3.5" stroke-linecap="round"/>'
    return f'''
{floor(905, 682, 350)}
{man}
{_table(580, 1090, desk_y, 680)}
{card}
{calc}{hand_l}{arm_r}{taps}
{bot}{sparkle}'''


# ── 초안까지, 보내는 건 사람 ────────────────────────────────
def draft_review():
    desk_y = 540
    # 로봇과 검토 트레이
    tray = (f'<path d="M262 {desk_y} L262 {desk_y-34} L420 {desk_y-34} L420 {desk_y} Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="250" y="{desk_y-44}" width="182" height="12" rx="4" fill="{N}"/>'
            f'<rect x="318" y="{desk_y-24}" width="46" height="12" rx="3" fill="{W}" stroke="{N}" stroke-width="2"/>')
    ex, ey = 300, 400   # 봉투 왼쪽 위
    env = (f'<path d="M{ex} {ey} L{ex+50} {ey-44} L{ex+100} {ey} Z" fill="{G}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
           f'<rect x="{ex+12}" y="{ey-30}" width="76" height="70" rx="3" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
           + lines(ex + 22, ex + 78, [ey - 18, ey - 6], G, 4)
           + f'<path d="M{ex} {ey} L{ex+100} {ey} L{ex+100} {ey+60} L{ex} {ey+60} Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
           + f'<path d="M{ex} {ey} L{ex+50} {ey+34} L{ex+100} {ey}" stroke="{N}" stroke-width="3" fill="none" stroke-linejoin="round"/>')
    rs = 1.1
    bx, by = 150, 668
    grip = (ex + 6, ey + 30)
    bot = robot(bx, by, rs, rarm(-44, -86, -62, -40) + rarm(44, -86, (grip[0] - bx) / rs, (grip[1] - by) / rs, 90, -150, hand=False), mouth="smile")
    grip_hand = f'<circle cx="{grip[0]}" cy="{grip[1]}" r="11" fill="{G}" stroke="{N}" stroke-width="3.3"/>'
    drop = f'<path d="M350 472 L350 488 M336 476 L340 488 M364 476 L360 488" stroke="{N}" stroke-opacity=".45" stroke-width="3" stroke-linecap="round"/>'
    left = f'''
{floor(250, 670, 230)}
{_table(240, 450, desk_y, 668)}
{tray}
{bot}{env}{grip_hand}{drop}'''

    # 가운데 회사원: 돋보기로 숫자 막대 확인
    s = .95
    px, wy = 770, 560
    dx, dy = 576, 468   # 문서 왼쪽 위 (세워 든 서류)
    doc = (f'<rect x="{dx}" y="{dy}" width="104" height="84" rx="4" fill="{W}" stroke="{N}" stroke-width="3.5" transform="rotate(-6 {dx+52} {dy+42})"/>'
           f'<g transform="rotate(-6 {dx+52} {dy+42})">{lines(dx+14, dx+90, [dy+18, dy+32], G, 5)}{lines(dx+14, dx+60, [dy+66], G, 5)}'
           f'<rect x="{dx+14}" y="{dy+44}" width="50" height="10" rx="3" fill="{N}" fill-opacity=".55"/></g>')
    lens_c = (612, 514)
    lens_hand = (650, 556)
    man = person(px, wy, s,
                 extra_back=parm(54, -140, (1000 - px) / s, (418 - wy) / s, 160, -170, hand=False),
                 extra_front="")
    arm_l = (f'<g transform="translate({px},{wy}) scale({s})">'
             + parm(-54, -140, (lens_hand[0] - px) / s, (lens_hand[1] - wy) / s, -120, -40, hand=False) + "</g>")
    lens = (f'<line x1="{lens_hand[0]}" y1="{lens_hand[1]}" x2="{lens_c[0]+20}" y2="{lens_c[1]+20}" stroke="{N}" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="{lens_c[0]}" cy="{lens_c[1]}" r="30" fill="{W}" fill-opacity=".55" stroke="{N}" stroke-width="7"/>'
            f'<path d="M{lens_c[0]-16} {lens_c[1]-14} A20 20 0 0 1 {lens_c[0]-2} {lens_c[1]-20}" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{lens_hand[0]}" cy="{lens_hand[1]}" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="3"/>')
    mid = f'''
{floor(800, 670, 250)}
{man}
{_table(560, 880, desk_y + 20, 668)}
{doc}
{arm_l}{lens}'''

    # 오른쪽: 아직 눌리지 않은 발송 버튼
    bx2 = 1010
    btn = f'''
<ellipse cx="{bx2}" cy="664" rx="70" ry="10" fill="{N}"/>
<rect x="{bx2-34}" y="512" width="68" height="152" rx="6" fill="{G}" stroke="{N}" stroke-width="4"/>
<rect x="{bx2-62}" y="498" width="124" height="18" rx="6" fill="{N}"/>
<path d="M{bx2-46} 498 L{bx2-46} 486 Q{bx2} 444 {bx2+46} 486 L{bx2+46} 498 Z" fill="{O}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M{bx2-26} 474 Q{bx2-14} 462 {bx2} 460" stroke="{W}" stroke-width="5" fill="none" stroke-linecap="round"/>'''
    hover = (f'<circle cx="1000" cy="418" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<path d="M{bx2-30} 440 L{bx2+30} 440" stroke="{N}" stroke-opacity=".45" stroke-width="3.5" stroke-dasharray="4 6" stroke-linecap="round"/>')
    arrows = _arrow_dash(455, 470, 560, 470) + _arrow_dash(866, 520, 930, 500)
    return left + mid + btn + hover + arrows
