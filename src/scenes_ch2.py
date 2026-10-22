"""Ch2 장면."""
import random

from art import *  # noqa


def label(cx, y, w=140):
    """이름표를 붙일 빈 회색 칸."""
    return f'<rect x="{cx-w/2}" y="{y}" width="{w}" height="24" rx="12" fill="{G}" stroke="{N}" stroke-width="2.5"/>'


def box(x, y, w, h, fill=G):
    """정면에서 본 상자. (x, y) = 왼쪽 위."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{N}" stroke-width="3"/>'
            f'<line x1="{x+w*.5-8}" y1="{y}" x2="{x+w*.5-8}" y2="{y+h*.35}" stroke="{N}" stroke-width="2.5"/>'
            f'<line x1="{x+w*.5+8}" y1="{y}" x2="{x+w*.5+8}" y2="{y+h*.35}" stroke="{N}" stroke-width="2.5"/>')


# ── ① 사무실 지도 ─────────────────────────────────────────
def _st_search():
    lens = f'''
<rect x="10" y="-82" width="170" height="12" rx="4" fill="{N}"/>
<rect x="22" y="-70" width="10" height="70" fill="{N}"/><rect x="158" y="-70" width="10" height="70" fill="{N}"/>
<rect x="46" y="-98" width="96" height="16" rx="2" fill="{W}" stroke="{N}" stroke-width="3"/>
<rect x="52" y="-110" width="88" height="14" rx="2" fill="{W}" stroke="{N}" stroke-width="3" transform="rotate(-4 96 -103)"/>
<line x1="70" y1="-104" x2="50" y2="-84" stroke="{N}" stroke-width="9" stroke-linecap="round"/>
<circle cx="96" cy="-132" r="30" fill="{W}" fill-opacity=".6" stroke="{N}" stroke-width="7"/>
<path d="M80 -146 A20 20 0 0 1 94 -152" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round"/>
<line x1="75" y1="-110" x2="56" y2="-90" stroke="{N}" stroke-width="10" stroke-linecap="round"/>'''
    bot = robot(-70, 0, 1, rarm(-44, -86, -66, -40) + rarm(44, -86, 122, -86, 96, -60))
    return bot + lens


def _st_binder():
    b = f'''
<path d="M-92 -104 L0 -96 L92 -104 L92 -26 L0 -18 L-92 -26 Z" fill="{N}"/>
<path d="M-84 -100 L-4 -92 L-4 -24 L-84 -32 Z M4 -92 L84 -100 L84 -32 L4 -24 Z" fill="{W}" stroke="{N}" stroke-width="2.5"/>
{"".join(f'<line x1="-72" y1="{y}" x2="-16" y2="{y+5}" stroke="{G}" stroke-width="5" stroke-linecap="round"/><line x1="16" y1="{y+5}" x2="72" y2="{y}" stroke="{G}" stroke-width="5" stroke-linecap="round"/>' for y in (-82, -66, -50))}
{"".join(f'<circle cx="0" cy="{y}" r="5" fill="{W}" stroke="{N}" stroke-width="2.5"/>' for y in (-80, -60, -40))}'''
    hands = f'<circle cx="-90" cy="-62" r="10" fill="{G}" stroke="{N}" stroke-width="3"/><circle cx="90" cy="-62" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>'
    return robot(0, 0, 1, rarm(-44, -86, -90, -62, -76, -96, hand=False) + rarm(44, -86, 90, -62, 76, -96, hand=False) + b + hands, mouth="flat")


def _st_shelf():
    sh = f'''
<rect x="10" y="-236" width="170" height="236" rx="4" fill="none" stroke="{N}" stroke-width="5"/>
{"".join(f'<rect x="10" y="{y}" width="170" height="7" fill="{N}"/>' for y in (-160, -84))}
{box(26, -132, 52, 48)}{box(92, -126, 44, 42, W)}
{box(30, -56, 60, 52, W)}{box(102, -48, 48, 44)}
{box(118, -200, 46, 40, W)}'''
    held = box(36, -214, 58, 50)
    bot = robot(-80, 0, 1, rarm(-44, -86, -66, -40) + rarm(44, -86, 112, -190, 96, -120))
    return sh + bot + held + f'<circle cx="32" cy="-190" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>'


def _st_draft():
    board = f'''
<rect x="-150" y="-60" width="10" height="60" fill="{N}"/><rect x="140" y="-60" width="10" height="60" fill="{N}"/>
<path d="M-140 -112 L140 -112 L170 -52 L-170 -52 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M-112 -106 L112 -106 L134 -60 L-134 -60 Z" fill="{W}" stroke="{N}" stroke-width="2.5"/>
<path d="M-90 -100 L-100 -66 M-90 -100 L-6 -100 L-10 -66 M-96 -82 L-8 -82 M30 -100 L36 -66 M30 -100 L100 -100 L112 -66 M34 -84 L106 -84" stroke="{N}" stroke-width="2" fill="none"/>
<g transform="translate(58 -74) rotate(-35)"><path d="M0 0 L10 -5 L10 5 Z" fill="{N}"/><rect x="10" y="-5" width="44" height="10" fill="{W}" stroke="{N}" stroke-width="2"/></g>'''
    return robot(0, -30, 1, rarm(-44, -86, -70, -42, hand=False) + rarm(44, -86, 70, -44, 80, -70, hand=False)) + board + \
        f'<circle cx="-40" cy="-70" r="10" fill="{G}" stroke="{N}" stroke-width="3"/><circle cx="72" cy="-80" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>'


def _st_conveyor():
    clock = f'''
<rect x="-262" y="-60" width="60" height="60" rx="4" fill="{G}" stroke="{N}" stroke-width="3"/>
<circle cx="-254" cy="-110" r="12" fill="{N}"/><circle cx="-210" cy="-110" r="12" fill="{N}"/>
<line x1="-246" y1="-62" x2="-252" y2="-56" stroke="{N}" stroke-width="5" stroke-linecap="round"/><line x1="-218" y1="-62" x2="-212" y2="-56" stroke="{N}" stroke-width="5" stroke-linecap="round"/>
<circle cx="-232" cy="-88" r="28" fill="{W}" stroke="{N}" stroke-width="5"/>
<path d="M-232 -88 L-232 -106 M-232 -88 L-220 -82" stroke="{N}" stroke-width="4" stroke-linecap="round"/>
<path d="M-272 -122 L-282 -132 M-192 -122 L-182 -132 M-232 -128 L-232 -140" stroke="{N}" stroke-width="4" stroke-linecap="round"/>'''
    belt = f'''
<rect x="-16" y="-46" width="10" height="46" fill="{N}"/><rect x="186" y="-46" width="10" height="46" fill="{N}"/>
<rect x="-30" y="-74" width="240" height="30" rx="15" fill="{G}" stroke="{N}" stroke-width="4"/>
{"".join(f'<circle cx="{x}" cy="-59" r="8" fill="{W}" stroke="{N}" stroke-width="2.5"/>' for x in (-14, 34, 82, 130, 178, 194))}
{box(10, -122, 50, 48, W)}{box(96, -116, 46, 42)}
<path d="M160 -100 L178 -100 M166 -112 L182 -112" stroke="{N}" stroke-width="3" stroke-linecap="round"/>
<circle cx="-30" cy="-59" r="24" fill="{W}" stroke="{N}" stroke-width="4"/>
<line x1="-30" y1="-59" x2="-46" y2="-86" stroke="{N}" stroke-width="6" stroke-linecap="round"/>'''
    bot = robot(-120, 0, 1, rarm(-44, -86, -66, -40) + rarm(44, -86, 74, -86, 64, -60, hand=False))
    return clock + belt + bot + f'<circle cx="-46" cy="-86" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>'


def _st_manual():
    book = f'''
<g transform="rotate(-8 82 -60)">
<rect x="56" y="-104" width="58" height="80" rx="4" fill="{N}"/>
<rect x="62" y="-98" width="46" height="68" rx="2" fill="{G}"/>
{lines(70, 100, [-84, -72, -60], W, 5)}
</g>'''
    return robot(0, 0, 1, rarm(-44, -86, -66, -40) + book + rarm(44, -86, 66, -46, 70, -74), mouth="smile")


def office_map():
    k = .6
    st = [((400, 330), _st_search), ((880, 330), _st_binder), ((1112, 486), _st_shelf),
          ((880, 640), _st_draft), ((420, 640), _st_conveyor), ((168, 486), _st_manual)]
    out = [f'<ellipse cx="640" cy="440" rx="610" ry="248" fill="{G}" fill-opacity=".35"/>',
           f'<ellipse cx="640" cy="486" rx="472" ry="156" fill="none" stroke="{G}" stroke-width="10" stroke-dasharray="2 22" stroke-linecap="round"/>']
    for (x, y), f in st:
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="128" ry="18" fill="{G}"/>')
        out.append(f'<g transform="translate({x},{y}) scale({k})">{f()}</g>')
        out.append(label(x, y + 14, 214))
    s = .62
    out.append(floor(640, 604, 60))
    out.append(person(640, 600 - 152 * s, s,
                      extra_front=parm(-54, -140, -58, -30, -116, -84) + parm(54, -140, 58, -30, 116, -84), legs=True))
    return "".join(out)


# ── ② 책상 위 결과물 ────────────────────────────────────────
def desk_outputs():
    py = 520
    happy = (f'<circle cx="-13" cy="-204" r="6" fill="{W}"/><circle cx="13" cy="-204" r="6" fill="{W}"/>'
             f'<path d="M-19 -202 Q-13 -210 -7 -202 M7 -202 Q13 -210 19 -202" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    person_ = person(640, py, 1, extra_front=happy)
    desk = f'''
<path d="M190 500 L1090 500 L1140 572 L140 572 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<rect x="134" y="572" width="1012" height="16" rx="4" fill="{N}"/>
<rect x="160" y="588" width="16" height="92" fill="{N}"/><rect x="1104" y="588" width="16" height="92" fill="{N}"/>'''
    arms = (f'<g transform="translate(640,{py})">'
            + parm(-54, -140, -76, -6, -90, -80) + parm(54, -140, 76, -6, 90, -80) + "</g>")
    report = f'''
<rect x="356" y="500" width="16" height="30" fill="{O}"/>
<path d="M290 528 L410 528 L420 552 L282 552 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
<path d="M282 552 L420 552 L420 566 L282 566 Z" fill="{N}"/>
<line x1="300" y1="536" x2="344" y2="536" stroke="{G}" stroke-width="4" stroke-linecap="round"/>
<line x1="296" y1="544" x2="400" y2="544" stroke="{G}" stroke-width="4" stroke-linecap="round"/>
<path d="M356 528 L372 528 L372 552 L364 545 L356 552 Z" fill="{O}"/>'''
    cells = "".join(f'<rect x="{454+i*26}" y="{402+j*22}" width="24" height="20" fill="{G if j == 0 else W}" stroke="{N}" stroke-width="1.5"/>' for i in range(3) for j in range(4))
    tablet = f'''
<path d="M470 524 L486 500 L520 500 L534 524 Z" fill="{N}"/>
<g transform="rotate(-4 495 450)">
<rect x="440" y="386" width="110" height="120" rx="10" fill="{N}"/>
{cells}
</g>'''
    proposal = f'''
<path d="M592 530 L692 530 L702 562 L584 562 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
{lines(602, 646, [538], N, 4)}{lines(600, 684, [546, 554], G, 4)}'''
    bars = [(60, G), (90, N), (74, G), (118, N), (100, G)]
    monitor = f'''
<rect x="852" y="470" width="20" height="40" fill="{N}"/>
<path d="M818 516 L906 516 L898 504 L826 504 Z" fill="{N}"/>
<rect x="760" y="320" width="204" height="156" rx="10" fill="{N}"/>
<rect x="772" y="332" width="180" height="132" rx="3" fill="{W}"/>
{"".join(f'<rect x="{790+i*32}" y="{452-h}" width="22" height="{h}" fill="{c}" stroke="{N}" stroke-width="2"/>' for i, (h, c) in enumerate(bars))}
<line x1="782" y1="452" x2="944" y2="452" stroke="{N}" stroke-width="2.5"/>'''
    env = f'''
<path d="M972 530 L1078 530 L1090 562 L962 562 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
<path d="M972 530 L1026 550 L1078 530" stroke="{N}" stroke-width="3" fill="none" stroke-linejoin="round"/>'''
    bot = robot(232, 556, .42, rarm(-44, -86, -96, -158, -94, -110) + rarm(44, -86, 66, -40), mouth="grin")
    sparkle = f'<path d="M700 300 L716 286 M712 316 L732 312 M580 300 L564 286" stroke="{N}" stroke-width="4" stroke-linecap="round"/>'
    return person_ + desk + bot + report + tablet + proposal + monitor + env + arms + sparkle


# ── ③ 표 두 개 ──────────────────────────────────────────
def _messy():
    rnd = random.Random(7)
    x0, y0, cols, rows, cw, ch = 82, 252, 8, 6, 46, 44
    used = set()
    out = []
    for r in range(rows):
        for c in range(cols):
            if (c, r) in used:
                continue
            w = rnd.choice([1, 1, 2, 3])
            h = rnd.choice([1, 1, 2])
            w = min(w, cols - c)
            h = min(h, rows - r)
            while any((c + i, r + j) in used for i in range(w) for j in range(h)):
                w = max(1, w - 1)
                h = max(1, h - 1) if w == 1 else h
                if w == 1 and h == 1:
                    break
            for i in range(w):
                for j in range(h):
                    used.add((c + i, r + j))
            f = rnd.choice([W, G, N, G, W])
            op = rnd.choice([1, .55, 1, .35])
            dx = rnd.choice([0, 0, 3, -3])
            out.append(f'<rect x="{x0+c*cw+dx}" y="{y0+r*ch}" width="{w*cw}" height="{h*ch}" fill="{f}" fill-opacity="{op}" stroke="{N}" stroke-width="{rnd.choice([2, 3.5])}"/>')
            if f == W and rnd.random() < .6:
                out.append(f'<line x1="{x0+c*cw+8}" y1="{y0+r*ch+h*ch/2+rnd.choice([-6, 4])}" x2="{x0+(c+w)*cw-8}" y2="{y0+r*ch+h*ch/2}" stroke="{G}" stroke-width="5" stroke-linecap="round"/>')
    return "".join(out)


def tables():
    W_, H_ = 368, 264
    left = f'''
{floor(330, 668, 280)}
<rect x="104" y="500" width="12" height="166" fill="{N}"/><rect x="406" y="500" width="12" height="166" fill="{N}"/>
<rect x="66" y="236" width="400" height="296" rx="10" fill="{W}" stroke="{N}" stroke-width="6"/>
{_messy()}
{robot(540, 666, 1.05, rarm(-44, -86, -62, -150, -100, -110) + rarm(44, -86, 62, -150, 100, -110), mouth="wavy")}
<path d="M512 400 C496 376 530 352 548 372 C566 392 520 404 524 382 C528 356 586 352 578 382 C572 404 534 398 546 376 C556 360 600 368 588 392" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'''
    x0, y0, cols, rows = 714, 252, 5, 6
    cw, ch = W_ / cols, H_ / rows
    hl = 5
    grid = []
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * cw, y0 + r * ch
            f = G if r == 0 else W
            grid.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{f}" stroke="{N}" stroke-width="2.5"/>')
            if r > 0:
                col = O if r == hl else G
                grid.append(f'<line x1="{x+12}" y1="{y+ch/2}" x2="{x+cw-12 - (c % 2)*14}" y2="{y+ch/2}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    ry = y0 + hl * ch
    grid.append(f'<rect x="{x0}" y="{ry}" width="{W_}" height="{ch}" fill="{O}" fill-opacity=".14" stroke="{O}" stroke-width="5"/>')
    right = f'''
{floor(960, 668, 280)}
<rect x="738" y="500" width="12" height="166" fill="{N}"/><rect x="1040" y="500" width="12" height="166" fill="{N}"/>
<rect x="698" y="236" width="400" height="296" rx="10" fill="{W}" stroke="{N}" stroke-width="6"/>
{"".join(grid)}
<path d="M1020 552 L920 552" stroke="{N}" stroke-width="3.5" stroke-dasharray="6 7" stroke-linecap="round"/>
<path d="M930 543 L918 552 L930 561" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
{robot(1150, 666, 1.05, rarm(44, -86, 66, -40) + rarm(-44, -86, -80, -round((666-(ry+ch/2))/1.05), -70, -100), mouth="grin")}'''
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── ④ 내비게이션 ─────────────────────────────────────────
def navigation():
    sx0, sy0, sx1, sy1 = 742, 206, 1082, 438
    roads = f'''
<clipPath id="navclip"><rect x="{sx0}" y="{sy0}" width="{sx1-sx0}" height="{sy1-sy0}" rx="4"/></clipPath>
<g clip-path="url(#navclip)" stroke="{G}" fill="none" stroke-linecap="round">
<rect x="{sx0}" y="{sy0}" width="{sx1-sx0}" height="{sy1-sy0}" fill="{W}" stroke="none"/>
<path d="M730 300 L1100 286 M730 392 L1100 410 M820 190 L842 450 M950 190 L930 450 M1040 190 L1030 450" stroke-width="14"/>
<path d="M730 250 Q880 260 1100 230 M760 450 Q900 340 1100 352 M880 190 L900 450 M990 300 L1100 420" stroke-width="7"/>
</g>'''
    route = "M900 426 L838 338 L940 300 L990 250 L1040 236"
    nav = f'''
{floor(910, 662, 340)}
<rect x="900" y="438" width="22" height="210" fill="{N}"/>
<rect x="846" y="646" width="130" height="14" rx="6" fill="{N}"/>
<rect x="726" y="190" width="372" height="264" rx="16" fill="{N}"/>
{roads}
<path d="M900 426 L920 362 L940 300" stroke="{N}" stroke-opacity=".35" stroke-width="5" fill="none" stroke-dasharray="8 8" stroke-linecap="round"/>
<path d="{route}" stroke="{O}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="920" cy="362" r="11" fill="{W}" stroke="{N}" stroke-opacity=".5" stroke-width="3" stroke-dasharray="4 3"/>
<circle cx="900" cy="426" r="11" fill="{N}"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{O}" stroke="{W}" stroke-width="4"/>' for x, y in ((940, 300), (990, 250)))}
<path d="M1040 236 L1040 206" stroke="{N}" stroke-width="4"/><path d="M1040 206 L1062 214 L1040 222 Z" fill="{N}"/>
<circle cx="1040" cy="236" r="6" fill="{N}"/>'''
    # 경유지를 손가락으로 옮기는 회사원
    s = .85
    px, wy = 668, 660 - 152 * s
    tx, ty = 838, 338
    lx, ly = (tx - px) / s, (ty - wy) / s
    man = person(px, wy, s, extra_back=parm(-54, -140, -66, -30, -78, -90),
                 extra_front=parm(54, -140, lx - 4, ly + 16, 120, -150, hand=False), legs=True)
    finger = (f'<circle cx="{tx}" cy="{ty}" r="15" fill="{O}" stroke="{W}" stroke-width="4"/>'
              f'<circle cx="{tx-3}" cy="{ty+14}" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>'
              f'<path d="M902 360 L866 350" stroke="{N}" stroke-width="3.5" stroke-dasharray="5 5" stroke-linecap="round"/>'
              f'<path d="M874 343 L864 350 L873 358" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # 출발 버튼에 손만 올리고 기다리는 로봇
    rs = 1.05
    btn = f'''
<rect x="1082" y="548" width="56" height="110" rx="6" fill="{G}" stroke="{N}" stroke-width="4"/>
<rect x="1074" y="540" width="72" height="14" rx="5" fill="{N}"/>
<ellipse cx="1110" cy="534" rx="24" ry="9" fill="{W}" stroke="{N}" stroke-width="4"/>
<path d="M1086 534 L1086 526 Q1110 510 1134 526 L1134 534" fill="{W}" stroke="{N}" stroke-width="4"/>'''
    bot = robot(1186, 660, rs, rarm(44, -86, 62, -40) + rarm(-44, -86, -72, -122, -84, -96), mouth="smile")
    return nav + man + finger + btn + bot


# ── ⑤ 계기판 두 개 ───────────────────────────────────────
def _dial(cx, cy, r, ang, color=N, op=1):
    import math
    a = math.radians(180 - ang)
    x, y = cx + r * math.cos(a), cy - r * math.sin(a)
    return f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}" stroke-opacity="{op}" stroke-width="7" stroke-linecap="round"/>'


def _ticks(cx, cy, r, color=N):
    import math
    out = [f'<path d="M{cx-r} {cy} A{r} {r} 0 0 1 {cx+r} {cy}" stroke="{color}" stroke-width="5" fill="none"/>']
    for i in range(7):
        a = math.radians(180 - i * 30)
        x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
        x2, y2 = cx + (r - 14) * math.cos(a), cy - (r - 14) * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
    return "".join(out)


def _wiggle(x, y):
    return (f'<path d="M{x} {y} Q{x+6} {y-8} {x} {y-16} M{x+10} {y+4} Q{x+18} {y-8} {x+10} {y-20}" '
            f'stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')


def gauges():
    # 왼쪽: 판자에 붙은 스티커. 상자가 바뀌어도 그대로
    left = f'''
{floor(270, 660, 240)}
<rect x="186" y="430" width="16" height="222" fill="{N}"/><rect x="150" y="646" width="88" height="12" rx="5" fill="{N}"/>
<rect x="74" y="228" width="240" height="210" rx="10" fill="{W}" stroke="{N}" stroke-width="5"/>
<path d="M104 262 L284 262 L284 380 L260 404 L104 404 Z" fill="{G}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
<path d="M284 380 L260 380 L260 404 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
{_ticks(194, 370, 74)}
{_dial(194, 370, 60, 50)}
<circle cx="194" cy="370" r="9" fill="{N}"/>
{box(342, 590, 64, 60)}{box(412, 590, 64, 60, W)}
<g transform="rotate(8 410 560)">{box(374, 528, 64, 58, W)}</g>
{_wiggle(486, 556)}{_wiggle(332, 548)}'''
    # 가운데 회사원: 오른쪽 계기판을 가리키며 끄덕
    s = .8
    px, wy = 596, 660 - 152 * s
    man = person(px, wy, s, extra_back=parm(-54, -140, -66, -30, -78, -90),
                 extra_front=parm(54, -140, 150, -236, 120, -150), legs=True)
    nod = f'<path d="M548 324 Q540 340 548 356 M644 324 Q652 340 644 356" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    # 오른쪽: 케이블로 연결된 바늘 계기판
    cx, cy = 834, 384
    right = f'''
{floor(970, 660, 290)}
<rect x="826" y="440" width="16" height="212" fill="{N}"/><rect x="790" y="646" width="88" height="12" rx="5" fill="{N}"/>
<path d="M968 300 C1150 300 1200 420 1200 590" stroke="{O}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M968 350 C1090 350 1130 440 1130 560" stroke="{O}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M968 400 C1040 400 1060 480 1060 590" stroke="{O}" stroke-width="7" fill="none" stroke-linecap="round"/>
<rect x="714" y="228" width="254" height="210" rx="10" fill="{W}" stroke="{N}" stroke-width="5"/>
{"".join(f'<rect x="960" y="{y-8}" width="16" height="16" rx="3" fill="{N}"/>' for y in (300, 350, 400))}
{_ticks(cx, cy, 96)}
{_dial(cx, cy, 78, 48, N, .22)}
{_dial(cx, cy, 78, 128)}
<path d="M{cx-58} {cy-52} A80 80 0 0 1 {cx+38} {cy-66}" stroke="{N}" stroke-width="3.5" fill="none" stroke-dasharray="2 8" stroke-linecap="round"/>
<path d="M{cx+30} {cy-74} L{cx+42} {cy-64} L{cx+28} {cy-58}" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="{cx}" cy="{cy}" r="11" fill="{N}"/>
{box(1028, 590, 64, 60, W)}{box(1098, 560, 64, 90)}{box(1168, 590, 64, 60, W)}
<rect x="1102" y="560" width="56" height="90" rx="4" fill="none"/>
{_wiggle(1238, 600)}{_wiggle(1016, 596)}'''
    for x, y in ((1130, 560), (1200, 590), (1060, 590)):
        right += f'<circle cx="{x}" cy="{y}" r="6" fill="{N}"/>'
    return left + right + man + nod


# ── ⑥ 두 장만 대조 ──────────────────────────────────────
def _flat_sheet(x, y, w, h, check=False):
    out = (f'<path d="M{x+6} {y} L{x+w-6} {y} L{x+w} {y+h} L{x} {y+h} Z" fill="{W}" stroke="{O if check else N}" stroke-width="{4 if check else 3}" stroke-linejoin="round"/>'
           + "".join(f'<line x1="{x+14}" y1="{y+12+i*12}" x2="{x+w-18-(i%2)*16}" y2="{y+12+i*12}" stroke="{G}" stroke-width="4" stroke-linecap="round"/>' for i in range(int((h - 16) / 12))))
    if check:
        out += f'<path d="M{x+w-34} {y-4} L{x+w-22} {y+10} L{x+w+2} {y-26}" stroke="{O}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    return out


def two_sheets():
    s = .9
    px, wy = 740, 560
    man = person(px, wy, s)
    desk = f'''
{floor(900, 668, 340)}
<path d="M590 494 L1100 494 L1140 588 L556 588 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<rect x="550" y="588" width="596" height="16" rx="4" fill="{N}"/>
<rect x="572" y="604" width="16" height="62" fill="{N}"/><rect x="1108" y="604" width="16" height="62" fill="{N}"/>'''
    # 높은 서류 더미 (회색)
    stack = []
    offs = [0, 4, -3, 2, -4, 3, -2, 5, -1, 3, -3, 1, 4, -2, 2, -4, 1, 3, -1, 0]
    for i, o in enumerate(offs):
        y = 540 - i * 14
        stack.append(f'<rect x="{968+o}" y="{y}" width="120" height="12" rx="2" fill="{W}" stroke="{N}" stroke-width="2.5"/>')
    stack = "".join(stack)
    sheets = _flat_sheet(684, 508, 112, 64, True) + _flat_sheet(818, 508, 112, 64, True)
    calc = f'''
<path d="M590 518 L656 514 L666 572 L594 576 Z" fill="{N}"/>
<path d="M598 524 L650 521 L652 534 L600 537 Z" fill="{W}"/>
{"".join(f'<circle cx="{606+i*14+j*1.5}" cy="{546+j*10}" r="4" fill="{G}"/>' for i in range(4) for j in range(3))}'''
    lh = (636, 552)
    rh = (868, 548)
    arms = (f'<g transform="translate({px},{wy}) scale({s})">'
            + parm(-54, -140, (lh[0]-px)/s, (lh[1]-wy)/s, -120, -80, hand=False)
            + parm(54, -140, (rh[0]-px)/s, (rh[1]-wy)/s, 120, -80, hand=False) + "</g>")
    hands = (f'<g transform="translate({rh[0]+4} {rh[1]-2}) rotate(-140)"><path d="M0 0 L8 -4 L8 4 Z" fill="{N}"/><rect x="8" y="-4" width="44" height="8" fill="{W}" stroke="{N}" stroke-width="2"/></g>'
             f'<circle cx="{lh[0]}" cy="{lh[1]}" r="11" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<circle cx="{rh[0]}" cy="{rh[1]}" r="11" fill="{W}" stroke="{N}" stroke-width="3"/>')
    bot = robot(1184, 666, 1.1, rarm(44, -86, 62, -40) + rarm(-44, -86, -84, -150, -86, -110), mouth="grin")
    return man + desk + sheets + calc + stack + arms + hands + bot
