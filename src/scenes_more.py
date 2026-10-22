"""추가 장면: 하네스 장비 · 피벗 분류 · 개인/회사 계정."""
from art import *  # noqa


def _hand(x, y, r=10):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G}" stroke="{N}" stroke-width="3"/>'


def _phand(x, y, s=1):
    return f'<circle cx="{x}" cy="{y}" r="{12*s}" fill="{W}" stroke="{N}" stroke-width="3"/>'


def _doc(x, y, rot=0, s=1):
    """작은 서류 한 장. (x, y) = 가운데."""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-20 -26 L10 -26 L20 -16 L20 26 L-20 26 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M10 -26 L10 -16 L20 -16" fill="{G}" stroke="{N}" stroke-width="2.5" stroke-linejoin="round"/>'
            + lines(-11, 10, [-10, 0, 10], G, 4) + "</g>")


def _arrow_dash(x1, y1, x2, y2, color=N, op=.55, w=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    l, k = 13, .55
    p1 = (x2 - l * math.cos(a - k), y2 - l * math.sin(a - k))
    p2 = (x2 - l * math.cos(a + k), y2 - l * math.sin(a + k))
    return (f'<g stroke="{color}" stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{x1} {y1} L{x2} {y2}" stroke-dasharray="8 9"/>'
            f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}"/></g>')


# ── 하네스 = 로봇에 채우는 장비 한 벌 ─────────────────────────
def harness_rig():
    rs = 1.3
    bx, by = 800, 668
    # 배낭 (로봇 뒤) — 로컬 좌표
    pack = (f'<g transform="translate({bx},{by}) scale({rs})">'
            f'<rect x="-96" y="-128" width="92" height="104" rx="20" fill="{O}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="-88" y="-146" width="62" height="26" rx="4" fill="{W}" stroke="{N}" stroke-width="3" transform="rotate(-8 -57 -133)"/>'
            f'<path d="M-82 -138 L-34 -145" stroke="{G}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M-96 -96 Q-60 -88 -40 -96" stroke="{N}" stroke-width="3.5" fill="none"/>'
            f'</g>')
    # 멜빵 + 허리 벨트(케이블 단자)
    straps = (f'<path d="M-36 -96 L-30 -38 M36 -96 L30 -38" stroke="{N}" stroke-width="7" stroke-linecap="round"/>'
              f'<rect x="-46" y="-46" width="92" height="12" rx="5" fill="{N}"/>'
              f'<rect x="40" y="-50" width="18" height="20" rx="4" fill="{G}" stroke="{N}" stroke-width="3"/>')
    # 왼손(화면 왼쪽)에 서류 가방
    hx, hy = -84, -64
    case = (f'<path d="M{hx-14} {hy+6} L{hx-14} {hy-4} Q{hx} {hy-14} {hx+14} {hy-4} L{hx+14} {hy+6}" stroke="{N}" stroke-width="5" fill="none"/>'
            f'<rect x="{hx-36}" y="{hy+6}" width="72" height="48" rx="7" fill="{G}" stroke="{N}" stroke-width="4"/>'
            f'<line x1="{hx-36}" y1="{hy+22}" x2="{hx+36}" y2="{hy+22}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{hx-7}" y="{hy+17}" width="14" height="10" rx="2" fill="{W}" stroke="{N}" stroke-width="2.5"/>')
    # 오른손: 결과물(서류)을 내민다
    dx, dy = 118, -112
    arms = (rarm(-44, -86, hx, hy - 6, -70, -96) + case
            + rarm(44, -86, dx - 14, dy + 22, 96, -70, hand=False))
    result = (f'<g transform="rotate(8 {dx} {dy})">'
              f'<rect x="{dx-20}" y="{dy-34}" width="54" height="68" rx="3" fill="{W}" stroke="{N}" stroke-width="3"/>'
              + lines(dx - 10, dx + 24, [dy - 20, dy - 8, dy + 4], G, 4) + "</g>"
              + _hand(dx - 14, dy + 22))
    bot = robot(bx, by, rs, straps + arms + result, mouth="smile")
    # 도구 상자 + 케이블
    tx, ty, tw = 930, 584, 112
    tool = (f'<rect x="{tx}" y="{ty}" width="{tw}" height="78" rx="10" fill="{G}" stroke="{N}" stroke-width="4"/>'
            f'<rect x="{tx+14}" y="{ty+12}" width="48" height="26" rx="4" fill="{W}" stroke="{N}" stroke-width="3"/>'
            + lines(tx + 22, tx + 54, [ty + 25], G, 5)
            + f'<circle cx="{tx+86}" cy="{ty+25}" r="12" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<line x1="{tx+86}" y1="{ty+25}" x2="{tx+93}" y2="{ty+18}" stroke="{N}" stroke-width="3" stroke-linecap="round"/>'
            + "".join(f'<rect x="{tx+16+i*22}" y="{ty+50}" width="14" height="14" rx="3" fill="{N}"/>' for i in range(4))
            + f'<rect x="{tx-12}" y="{ty+16}" width="14" height="20" rx="3" fill="{N}"/>')
    jx, jy = bx + 58 * rs, by - 40 * rs
    cable = (f'<path d="M{jx} {jy} C{jx+30} {jy+10} {jx+10} {by-6} {tx-30} {by-30} S{tx-36} {ty+26} {tx-12} {ty+26}" '
             f'stroke="{N}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    # 확인하는 회사원
    s = .82
    px, wy = 1176, 668 - 152 * s
    cbx, cby = 1058, 424   # 클립보드 왼쪽 위
    cw, ch = 84, 112
    clip = (f'<g transform="rotate(-8 {cbx+cw/2} {cby+ch/2})">'
            f'<rect x="{cbx}" y="{cby}" width="{cw}" height="{ch}" rx="7" fill="{N}"/>'
            f'<rect x="{cbx+8}" y="{cby+12}" width="{cw-16}" height="{ch-20}" rx="2" fill="{W}"/>'
            f'<rect x="{cbx+cw/2-18}" y="{cby-6}" width="36" height="16" rx="4" fill="{G}" stroke="{N}" stroke-width="2.5"/>'
            + "".join(f'<rect x="{cbx+16}" y="{cby+26+i*26}" width="14" height="14" rx="2" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
                      + lines(cbx + 38, cbx + cw - 16, [cby + 33 + i * 26], G, 5) for i in range(3))
            + "".join(f'<path d="M{cbx+17} {cby+32+i*26} L{cbx+23} {cby+38+i*26} L{cbx+33} {cby+22+i*26}" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for i in range(2))
            + "</g>")
    hold = (cbx + 4, cby + 76)
    pen_hand = (cbx + 66, cby + 92)
    L = lambda p: ((p[0] - px) / s, (p[1] - wy) / s)
    man = person(px, wy, s, legs=True)
    arm_l = (f'<g transform="translate({px},{wy}) scale({s})">'
             + parm(-54, -140, *L(hold), -130, -40, hand=False) + "</g>")
    arm_r = (f'<g transform="translate({px},{wy}) scale({s})">'
             + parm(54, -140, *L(pen_hand), 76, -10, hand=False) + "</g>")
    pen = (f'<line x1="{pen_hand[0]}" y1="{pen_hand[1]}" x2="{pen_hand[0]-16}" y2="{pen_hand[1]-30}" stroke="{N}" stroke-width="6" stroke-linecap="round"/>')
    return f'''
{floor(880, 670, 330)}
{pack}
{tool}{cable}
{bot}
{man}{arm_l}{clip}{arm_r}{pen}{_phand(*hold, s)}{_phand(*pen_hand, s)}'''


# ── 피벗 = 기준별로 묶어 합치기 ─────────────────────────────
def _tag(x, y, kind, size=16):
    f = {"n": N, "g": G, "w": W}[kind]
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{f}" stroke="{N}" stroke-width="2.5"/>'


def _card(x, y, kind, rot=0, w=150, h=40):
    """회색 카드 한 장. (x, y) = 왼쪽 위."""
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{G}" stroke="{N}" stroke-width="3"/>'
            + _tag(x + 10, y + 8, kind)
            + lines(x + 38, x + w - 20, [y + 14], W, 5) + lines(x + 38, x + w - 50, [y + 27], W, 5)
            + "</g>")


def pivot_bins():
    floor_y = 668
    # 왼쪽: 길게 쌓인 카드 더미
    tx0, tx1, ty = 50, 290, 540
    order = "ngwgnwngw"
    pile = "".join(_card(tx0 + 44 + (i % 3) * 6 - 6, ty - 40 - i * 30, k, (-2, 1, 3, -1)[i % 4], 140, 40)
                   for i, k in enumerate(order))
    table = (f'<rect x="{tx0}" y="{ty}" width="{tx1-tx0}" height="16" rx="6" fill="{N}"/>'
             f'<rect x="{tx0+18}" y="{ty+16}" width="14" height="{floor_y-ty-16}" fill="{N}"/>'
             f'<rect x="{tx1-32}" y="{ty+16}" width="14" height="{floor_y-ty-16}" fill="{N}"/>')
    # 오른쪽: 통 세 개 + 막대
    bins = [(600, "n", 140), (760, "g", 250), (920, "w", 96)]
    bw, btop = 128, 524
    bars, binsvg, inside = [], [], []
    tallest = max(h for _, _, h in bins)
    for x, k, h in bins:
        c = O if h == tallest else (N if k == "n" else G)
        bars.append(f'<rect x="{x+bw/2-24}" y="{btop-h}" width="48" height="{h+6}" rx="4" fill="{c}" stroke="{N}" stroke-width="3"/>')
        inside.append(_card(x + 6, btop - 20, k, -10, 104, 32) + _card(x + 20, btop - 14, k, 8, 104, 32))
        binsvg.append(f'<path d="M{x} {btop} L{x+bw} {btop} L{x+bw-12} {floor_y-2} L{x+12} {floor_y-2} Z" fill="{W}" stroke="{N}" stroke-width="5" stroke-linejoin="round"/>'
                      f'<rect x="{x-6}" y="{btop-6}" width="{bw+12}" height="14" rx="5" fill="{N}"/>'
                      + _tag(x + bw / 2 - 18, btop + 44, k, 36))
    # 로봇: 왼손은 더미에서 뽑은 카드, 오른손은 통에 넣는다
    rs = 1.35
    bx, by = 450, floor_y
    grab = (318, 452)
    drop = (596, 488)
    L = lambda p: ((p[0] - bx) / rs, (p[1] - by) / rs)
    held_l = _card(grab[0] - 70, grab[1] - 32, "g", -12, 104, 32)
    held_r = _card(drop[0] - 6, drop[1] - 30, "n", 28, 104, 32)
    bot = robot(bx, by, rs, rarm(-44, -86, *L(grab), -100, -110, hand=False)
                + rarm(44, -86, *L(drop), 80, -150, hand=False), mouth="grin")
    hands = _hand(*grab, 12) + _hand(*drop, 12)
    # 오른쪽 회사원: 막대를 보고 끄덕
    s = .74
    px, wy = 1170, floor_y - 152 * s
    hy = wy - 210 * s
    man = person(px, wy, s, extra_back=parm(54, -140, 62, -30, 70, -90),
                 extra_front=parm(-54, -140, -60, -30, -76, -90), legs=True)
    nod = (f'<path d="M{px-46} {hy-14} Q{px-54} {hy} {px-46} {hy+14} M{px+46} {hy-14} Q{px+54} {hy} {px+46} {hy+14}" '
           f'stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    return f'''
{floor(640, 670, 610)}
{table}{pile}
{"".join(bars)}
{"".join(inside)}{"".join(binsvg)}
{bot}{held_l}{held_r}{hands}
{man}{nod}'''


# ── 개인 계정과 회사 계정 ───────────────────────────────────
def account_privacy():
    floor_y = 668
    # 왼쪽: 집 → 컨베이어 → 학습 공장
    hx, hw = 40, 120
    house = (f'<rect x="{hx}" y="{floor_y-120}" width="{hw}" height="120" fill="{W}" stroke="{N}" stroke-width="4"/>'
             f'<path d="M{hx-14} {floor_y-116} L{hx+hw/2} {floor_y-186} L{hx+hw+14} {floor_y-116} Z" fill="{N}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
             f'<rect x="{hx+18}" y="{floor_y-94}" width="32" height="30" rx="2" fill="{G}" stroke="{N}" stroke-width="3"/>'
             f'<rect x="{hx+70}" y="{floor_y-70}" width="32" height="70" rx="2" fill="{G}" stroke="{N}" stroke-width="3"/>'
             f'<circle cx="{hx+94}" cy="{floor_y-36}" r="3" fill="{N}"/>')
    # 컨베이어
    cy = 600
    cx0, cx1 = 176, 392
    belt = (f'<rect x="{cx0+16}" y="{cy+14}" width="10" height="{floor_y-cy-14}" fill="{N}"/>'
            f'<rect x="{cx1-30}" y="{cy+14}" width="10" height="{floor_y-cy-14}" fill="{N}"/>'
            f'<rect x="{cx0}" y="{cy-6}" width="{cx1-cx0}" height="24" rx="12" fill="{G}" stroke="{N}" stroke-width="4"/>'
            + "".join(f'<circle cx="{x}" cy="{cy+6}" r="6" fill="{W}" stroke="{N}" stroke-width="2.5"/>' for x in range(cx0 + 14, cx1 - 6, 34)))
    docs_belt = _doc(222, cy - 34, -4, .9) + _doc(290, cy - 34, 6, .9) + _doc(356, cy - 36, -8, .9)
    # 학습 공장
    fx, fw, ftop = 404, 210, 400
    gear = lambda x, y, r: (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{W}" stroke="{N}" stroke-width="4" stroke-dasharray="{r*.5:.1f} {r*.35:.1f}"/>'
                            f'<circle cx="{x}" cy="{y}" r="{r*.72:.1f}" fill="{G}" stroke="{N}" stroke-width="3.5"/>'
                            f'<circle cx="{x}" cy="{y}" r="{r*.25:.1f}" fill="{W}" stroke="{N}" stroke-width="3"/>')
    factory = (f'<rect x="{fx+130}" y="{ftop-150}" width="30" height="150" fill="{G}" stroke="{N}" stroke-width="4"/>'
               f'<rect x="{fx+170}" y="{ftop-110}" width="26" height="110" fill="{G}" stroke="{N}" stroke-width="4"/>'
               f'<circle cx="{fx+150}" cy="{ftop-176}" r="14" fill="{G}"/><circle cx="{fx+170}" cy="{ftop-190}" r="18" fill="{G}"/><circle cx="{fx+184}" cy="{ftop-136}" r="11" fill="{G}"/>'
               f'<path d="M{fx} {floor_y} L{fx} {ftop} L{fx+60} {ftop-40} L{fx+60} {ftop} L{fx+120} {ftop-40} L{fx+120} {ftop} L{fx+fw} {ftop} L{fx+fw} {floor_y} Z" '
               f'fill="{G}" stroke="{N}" stroke-width="5" stroke-linejoin="round"/>'
               + gear(fx + 70, ftop + 70, 34) + gear(fx + 150, ftop + 90, 24)
               + f'<path d="M{fx-2} {cy-58} L{fx+44} {cy-58} L{fx+44} {cy+18} L{fx-2} {cy+18} Z" fill="{N}"/>'
               f'<path d="M{fx+4} {cy-50} L{fx+38} {cy-50} L{fx+38} {cy+12} L{fx+4} {cy+12} Z" fill="{N}" stroke="{W}" stroke-width="2" stroke-opacity=".4"/>'
               + "".join(f'<rect x="{fx+70+i*44}" y="{floor_y-74}" width="30" height="30" rx="3" fill="{W}" stroke="{N}" stroke-width="3"/>' for i in range(3)))
    left = f'''
{floor(320, 670, 300)}
{house}{belt}{factory}{docs_belt}
{_arrow_dash(186, 512, 390, 512)}'''

    # 오른쪽: 사무실 + 금고 + 회사원
    ox, ow, otop = 690, 300, 230
    win = "".join(f'<rect x="{ox+24+i*66}" y="{otop+26+j*60}" width="48" height="38" rx="3" fill="{G}" stroke="{N}" stroke-width="3"/>'
                  for i in range(4) for j in range(2))
    # 1층 단면: 금고가 보이는 방
    ry0 = otop + 150
    room = (f'<rect x="{ox+20}" y="{ry0}" width="{ow-40}" height="{floor_y-ry0-4}" rx="4" fill="{W}" stroke="{N}" stroke-width="3"/>')
    vx, vy, vw, vh = ox + 120, ry0 + 40, 140, 230
    vault = (f'<rect x="{vx}" y="{vy}" width="{vw}" height="{floor_y-vy-4}" rx="10" fill="{N}"/>'
             f'<rect x="{vx+12}" y="{vy+12}" width="{vw-24}" height="{floor_y-vy-30}" rx="6" fill="none" stroke="{W}" stroke-opacity=".35" stroke-width="3"/>'
             f'<circle cx="{vx+50}" cy="{vy+80}" r="26" fill="{G}" stroke="{W}" stroke-opacity=".4" stroke-width="3"/>'
             + "".join(f'<line x1="{vx+50}" y1="{vy+80}" x2="{vx+50+22*c}" y2="{vy+80+22*d}" stroke="{N}" stroke-width="4" stroke-linecap="round"/>'
                       for c, d in ((1, 0), (-.5, .87), (-.5, -.87)))
             + f'<rect x="{vx+vw-22}" y="{vy+50}" width="10" height="60" rx="3" fill="{G}"/>')
    lk = (vx + vw - 10, vy + 150)
    lock = (f'<path d="M{lk[0]-14} {lk[1]} L{lk[0]-14} {lk[1]-14} Q{lk[0]} {lk[1]-34} {lk[0]+14} {lk[1]-14} L{lk[0]+14} {lk[1]}" stroke="{O}" stroke-width="7" fill="none"/>'
            f'<rect x="{lk[0]-24}" y="{lk[1]}" width="48" height="40" rx="7" fill="{O}" stroke="{N}" stroke-width="3"/>'
            f'<circle cx="{lk[0]}" cy="{lk[1]+16}" r="5" fill="{N}"/><rect x="{lk[0]-2.5}" y="{lk[1]+18}" width="5" height="12" fill="{N}"/>')
    shelf_docs = _doc(ox + 60, floor_y - 120, -6, .85) + _doc(ox + 70, floor_y - 60, 4, .85)
    keep = _arrow_dash(ox + 88, floor_y - 120, vx - 6, floor_y - 120)
    office = (f'<rect x="{ox}" y="{otop}" width="{ow}" height="{floor_y-otop}" rx="6" fill="{G}" stroke="{N}" stroke-width="5"/>'
              f'<rect x="{ox-10}" y="{otop-14}" width="{ow+20}" height="18" rx="6" fill="{N}"/>'
              + win + room + vault + lock + shelf_docs + keep)
    s = .78
    px, wy = 1120, floor_y - 152 * s
    man = person(px, wy, s, extra_back=parm(54, -140, 64, -30, 72, -90),
                 extra_front=parm(-54, -140, -100, -150, -110, -90), legs=True)
    right = f'''
{floor(950, 670, 290)}
{office}
{man}'''
    return left + f'<line x1="652" y1="190" x2="652" y2="690" stroke="{G}" stroke-width="3"/>' + right
