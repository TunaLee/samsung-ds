"""Ch5 장면: 비서 · 컨베이어 · 면접 · 아침 에이전트 · 공사 현장."""
from art import *  # noqa


# ── 비서: 매뉴얼을 낀 로봇이 회사원 옆에서 대기 ─────────────────
def secretary():
    # 로봇 로컬 좌표: 오른쪽 옆구리에 두꺼운 매뉴얼, 왼손은 표지를 들어 올리려는 중
    book = f'''
<rect x="48" y="-124" width="74" height="96" rx="4" fill="{W}" stroke="{N}" stroke-width="3"/>
{"".join(f'<line x1="{x}" y1="-120" x2="{x}" y2="-32" stroke="{G}" stroke-width="2"/>' for x in (94, 100, 106, 112))}
<path d="M46 -126 L86 -136 L86 -38 L46 -26 Z" fill="{N}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>
<rect x="54" y="-110" width="26" height="12" rx="2" fill="{G}" transform="skewY(-11)" transform-origin="54 -110"/>'''
    flap = f'<path d="M128 -110 L138 -116 M130 -80 L142 -80 M128 -52 L138 -46" stroke="{N}" stroke-width="3" stroke-linecap="round"/>'
    tag = f'<rect x="-36" y="-92" width="28" height="14" rx="3" fill="{O}" stroke="{N}" stroke-width="2"/>'
    arms = (rarm(44, -86, 66, -32, 74, -66)
            + rarm(-44, -86, 86, -88, 10, -16))
    bot = robot(1055, 655, 1.35, tag + book + flap + arms)
    return f'''
{floor(890, 660, 335)}
<rect x="610" y="330" width="160" height="200" rx="20" fill="{G}" stroke="{N}" stroke-width="4"/>
{person(690, 525, .85,
        extra_back=parm(-54, -140, -96, -6, -100, -80),
        extra_front=parm(54, -140, 128, -176, 110, -110))}
<rect x="560" y="520" width="330" height="16" rx="6" fill="{N}"/>
<rect x="580" y="536" width="14" height="118" fill="{N}"/>
<rect x="856" y="536" width="14" height="118" fill="{N}"/>
<rect x="590" y="488" width="96" height="30" rx="4" fill="{W}" stroke="{N}" stroke-width="3"/>
{lines(602, 670, [500], G, 4)}
<rect x="780" y="482" width="30" height="36" rx="5" fill="{W}" stroke="{N}" stroke-width="3"/>
<path d="M810 492 Q824 496 810 508" stroke="{N}" stroke-width="3" fill="none"/>
<path d="M800 210 h104 a22 22 0 0 1 22 22 v28 a22 22 0 0 1 -22 22 h-74 l-22 22 l4 -22 h-8 a22 22 0 0 1 -22 -22 v-28 a22 22 0 0 1 22 -22 z"
      fill="{W}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
{bot}

'''


# ── 컨베이어: 모든 서류 앞에 같은 지시 카드 ───────────────────
def _doc(x, y, card=False, rot=0):
    s = (f'<g transform="rotate({rot} {x+50} {y+65})">'
         f'<rect x="{x}" y="{y}" width="100" height="130" rx="5" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
         + lines(x + 14, x + 86, [y + 70, y + 86, y + 102, y + 116]))
    if card:
        s += _card(x + 12, y + 10)
    else:
        s += lines(x + 14, x + 70, [y + 22, y + 38, y + 54])
    return s + "</g>"


def _card(x, y):
    return (f'<rect x="{x}" y="{y}" width="76" height="50" rx="4" fill="{O}" stroke="{N}" stroke-width="2.5"/>'
            + lines(x + 10, x + 62, [y + 18], W, 4) + lines(x + 10, x + 46, [y + 32], W, 4)
            + f'<rect x="{x+30}" y="{y-8}" width="16" height="18" rx="3" fill="{G}" stroke="{N}" stroke-width="2.5"/>')


def conveyor():
    belt_y = 520
    rollers = "".join(f'<circle cx="{x}" cy="{belt_y+20}" r="13" fill="{G}" stroke="{N}" stroke-width="3"/><circle cx="{x}" cy="{belt_y+20}" r="3" fill="{N}"/>'
                      for x in range(70, 900, 64))
    belt = f'''
<rect x="50" y="{belt_y}" width="860" height="40" rx="20" fill="{W}" stroke="{N}" stroke-width="4"/>
{rollers}
<rect x="110" y="{belt_y+40}" width="14" height="110" fill="{N}"/>
<rect x="470" y="{belt_y+40}" width="14" height="110" fill="{N}"/>
<rect x="836" y="{belt_y+40}" width="14" height="110" fill="{N}"/>'''
    docs = (_doc(80, 388) + _doc(250, 388) + _doc(420, 388)
            + _doc(600, 388) + _doc(770, 388, True))
    speed = "".join(f'<line x1="{x}" y1="{y}" x2="{x+28}" y2="{y}" stroke="{G}" stroke-width="4" stroke-linecap="round"/>'
                    for x in (36, 206, 376) for y in (430, 452))
    # 위에서 내려온 기계 팔: 천장 레일은 회색 구역 아래에 둔다
    arm = f'''
<rect x="430" y="190" width="420" height="16" rx="6" fill="{N}"/>
<rect x="548" y="200" width="44" height="26" rx="5" fill="{G}" stroke="{N}" stroke-width="3"/>
<line x1="570" y1="226" x2="570" y2="290" stroke="{N}" stroke-width="12" stroke-linecap="round"/>
<circle cx="570" cy="292" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>
<line x1="570" y1="292" x2="610" y2="330" stroke="{N}" stroke-width="12" stroke-linecap="round"/>
<circle cx="610" cy="332" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>
<path d="M600 340 L596 362 M620 340 L624 362" stroke="{N}" stroke-width="6" stroke-linecap="round"/>
{_card(572, 362)}'''
    # 로봇: 지시 카드부터 읽는다
    held = (f'<g transform="translate(-40,-112) scale(.8)">{_doc(0, 0, True)}</g>'
            + rarm(-44, -86, -42, -60, -64, -76) + rarm(44, -86, 42, -60, 64, -76))
    bot = robot(1110, 660, 1.35, mouth="flat")
    held_g = f'<g transform="translate(1110,660) scale(1.35)">{held}</g>'
    stack = (f'<rect x="1176" y="610" width="90" height="40" fill="{W}" stroke="{N}" stroke-width="3"/>'
             + "".join(f'<line x1="1176" y1="{y}" x2="1266" y2="{y}" stroke="{N}" stroke-width="2"/>' for y in (620, 630, 640)))
    return floor(1110, 664, 150) + belt + speed + docs + arm + bot + held_g + stack


# ── 면접: 세 종류의 질문 카드 ─────────────────────────────
def interview():
    c1 = (f'<rect x="-36" y="-110" width="72" height="100" rx="5" fill="{W}" stroke="{N}" stroke-width="3"/>'
          + lines(-24, 24, [-90, -74, -58, -42]))
    c2 = (f'<rect x="-36" y="-110" width="72" height="100" rx="5" fill="{W}" stroke="{N}" stroke-width="3" stroke-dasharray="7 5"/>'
          + lines(-24, 20, [-90]) + lines(-24, 0, [-74]))
    c3 = (f'<path d="M-36 -110 L16 -110 L36 -90 L36 -10 L-36 -10 Z" fill="{O}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
          f'<path d="M16 -110 L16 -90 L36 -90 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'
          f'<rect x="-46" y="-66" width="92" height="16" fill="{G}" fill-opacity=".9" stroke="{N}" stroke-width="2" transform="rotate(-14 0 -58)"/>')
    hx, hy = 510, 420
    fan = (f'<g transform="translate({hx},{hy})">'
           f'<g transform="rotate(-36)">{c1}</g><g transform="rotate(-6)">{c2}</g>'
           f'<g transform="translate(34,-22) rotate(26)">{c3}</g></g>')
    hand = f'<circle cx="{hx}" cy="{hy-6}" r="13" fill="{W}" stroke="{N}" stroke-width="3"/>'
    table = f'''
<rect x="220" y="500" width="840" height="18" rx="6" fill="{N}"/>
<rect x="240" y="518" width="800" height="120" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="250" y="638" width="14" height="40" fill="{N}"/><rect x="1016" y="638" width="14" height="40" fill="{N}"/>'''
    chair_l = f'<rect x="230" y="300" width="150" height="200" rx="20" fill="{G}" stroke="{N}" stroke-width="4"/>'
    chair_r = f'<rect x="868" y="330" width="164" height="170" rx="20" fill="{G}" stroke="{N}" stroke-width="4"/>'
    p = person(305, 505, .85,
               extra_back=parm(-54, -140, -70, -14, -90, -80),
               extra_front=parm(54, -140, (hx - 305) / .85, (hy - 505) / .85, 110, -70, hand=False))
    bot = robot(950, 570, 1.3,
                rarm(-44, -86, -78, -54, -74, -70) + rarm(44, -86, 88, -50, 76, -70))
    pad = (f'<path d="M1030 490 L1100 490 L1108 504 L1022 504 Z" fill="{W}" stroke="{N}" stroke-width="3"/>'
           f'<line x1="1036" y1="497" x2="1090" y2="497" stroke="{G}" stroke-width="3"/>'
           f'<line x1="1064" y1="500" x2="1074" y2="478" stroke="{N}" stroke-width="5" stroke-linecap="round"/>'
           f'<circle cx="1064" cy="505" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>'
           f'<circle cx="849" cy="502" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>')
    motion = f'<path d="M610 286 L632 276 M622 310 L648 306" stroke="{N}" stroke-width="4" stroke-linecap="round"/>'
    return chair_l + chair_r + p + bot + table + pad + fan + hand + motion


# ── 아침의 에이전트: 알람 → 메일함 → 검토 트레이 ─────────────────
def agent_morning():
    clock = f'''
<path d="M88 214 L104 196 M190 214 L174 196" stroke="{N}" stroke-width="6" stroke-linecap="round"/>
<circle cx="102" cy="222" r="16" fill="{O}" stroke="{N}" stroke-width="3"/>
<circle cx="176" cy="222" r="16" fill="{O}" stroke="{N}" stroke-width="3"/>
<circle cx="139" cy="270" r="56" fill="{O}" stroke="{N}" stroke-width="4"/>
<circle cx="139" cy="270" r="42" fill="{W}"/>
<path d="M139 270 L139 240 M139 270 L160 282" stroke="{N}" stroke-width="5" stroke-linecap="round"/>
<circle cx="139" cy="270" r="4" fill="{N}"/>
<path d="M60 236 Q50 270 60 304 M42 228 Q30 270 42 312 M218 236 Q228 270 218 304 M236 228 Q248 270 236 312"
      stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round"/>'''
    window = f'''
<rect x="60" y="390" width="160" height="150" rx="6" fill="{W}" stroke="{N}" stroke-width="4"/>
<circle cx="140" cy="520" r="34" fill="{G}"/>
<rect x="64" y="520" width="152" height="16" fill="{W}"/>
<line x1="140" y1="390" x2="140" y2="540" stroke="{N}" stroke-width="3"/>
<line x1="60" y1="465" x2="220" y2="465" stroke="{N}" stroke-width="3"/>'''
    mailbox = f'''
<rect x="404" y="500" width="14" height="160" fill="{N}"/>
<path d="M346 500 L346 410 Q346 360 411 360 Q476 360 476 410 L476 500 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M362 488 L362 416 Q362 378 411 378 Q460 378 460 416 L460 488 Z" fill="{N}"/>
<path d="M362 488 L460 488 L460 560 Q460 596 411 596 Q362 596 362 560 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<rect x="398" y="566" width="26" height="8" rx="4" fill="{N}"/>
<rect x="476" y="400" width="10" height="56" fill="{N}"/><rect x="486" y="400" width="26" height="18" fill="{G}" stroke="{N}" stroke-width="3"/>'''
    letter = (f'<g transform="rotate(-10 452 440)"><rect x="410" y="420" width="70" height="44" rx="3" fill="{W}" stroke="{N}" stroke-width="3"/>'
              f'<path d="M410 422 L445 446 L480 422" stroke="{N}" stroke-width="2.5" fill="none"/></g>')
    book = (f'<rect x="40" y="-120" width="34" height="84" rx="4" fill="{N}" transform="rotate(-6 57 -78)"/>'
            f'<rect x="70" y="-116" width="8" height="78" fill="{W}" stroke="{N}" stroke-width="2" transform="rotate(-6 57 -78)"/>')
    bot = robot(610, 655, 1.2, book + rarm(44, -86, 56, -40, 64, -66) + rarm(-44, -86, -112, -180, -100, -100, hand=False))
    hand = f'<circle cx="476" cy="439" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>'
    desk = f'''
<rect x="860" y="540" width="250" height="16" rx="6" fill="{N}"/>
<rect x="876" y="556" width="14" height="104" fill="{N}"/><rect x="1080" y="556" width="14" height="104" fill="{N}"/>
<g transform="rotate(-4 975 516)"><rect x="936" y="494" width="76" height="34" fill="{W}" stroke="{N}" stroke-width="2.5"/>{lines(944, 1000, [503, 512, 520], G, 3)}</g>
<path d="M920 540 L1030 540 L1036 516 L1022 516 L1018 528 L932 528 L928 516 L914 516 Z" fill="{G}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'''
    p = person(1150, 665 - 152 * .75, .75,
               extra_back=parm(54, -140, 76, -20) +
               f'<rect x="54" y="-24" width="70" height="56" rx="8" fill="{N}"/><path d="M68 -24 Q89 -54 110 -24" stroke="{N}" stroke-width="6" fill="none"/>',
               extra_front=parm(-54, -140, -164, -40, -120, -130), legs=True)
    arrows = f'''
<path d="M230 220 Q400 170 500 330" stroke="{N}" stroke-width="3" fill="none" stroke-dasharray="8 8"/>
<path d="M488 320 L502 334 L506 314" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M760 330 Q850 300 920 470" stroke="{N}" stroke-width="3" fill="none" stroke-dasharray="8 8"/>
<path d="M906 458 L922 474 L928 452" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''
    return (floor(640, 662, 600) + clock + window + arrows + mailbox + bot + letter + hand
            + desk + p)


# ── 공사 현장: 멈춘 큰 탑 vs 완성된 작은 집 ─────────────────────
def construction():
    # 왼쪽: 골조만 선 탑. 위쪽 절반은 점선으로만
    cols = [230, 302, 374, 446]
    frame = "".join(f'<rect x="{x-6}" y="410" width="12" height="240" fill="{N}"/>' for x in cols)
    frame += "".join(f'<rect x="224" y="{y}" width="228" height="10" fill="{N}"/>' for y in (410, 490))
    frame += "".join(f'<line x1="{a}" y1="{y}" x2="{a+72}" y2="{y+80}" stroke="{N}" stroke-width="4"/>' for a in (230, 374) for y in (410, 490))
    stub = "".join(f'<rect x="{x-6}" y="{344 + (i % 2) * 30}" width="12" height="{66 - (i % 2) * 30}" fill="{N}"/>' for i, x in enumerate(cols))
    ghost = f'<rect x="224" y="196" width="228" height="214" fill="none" stroke="{N}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="10 8"/>'
    walls = f'<rect x="224" y="570" width="228" height="80" fill="{G}" stroke="{N}" stroke-width="3"/>'
    crane = f'''
<rect x="532" y="220" width="18" height="430" fill="{N}"/>
{"".join(f'<line x1="532" y1="{y}" x2="550" y2="{y+30}" stroke="{W}" stroke-width="3"/>' for y in range(234, 640, 34))}
<rect x="260" y="206" width="350" height="16" fill="{N}"/>
<rect x="572" y="222" width="34" height="30" fill="{G}" stroke="{N}" stroke-width="3"/>
<line x1="340" y1="222" x2="340" y2="300" stroke="{N}" stroke-width="3"/>
<path d="M334 300 L346 300 L346 310 Q346 322 336 320" stroke="{N}" stroke-width="4" fill="none"/>'''
    mess = f'''
<g transform="rotate(-8 520 640)"><rect x="470" y="628" width="140" height="14" fill="{G}" stroke="{N}" stroke-width="2.5"/></g>
<rect x="478" y="640" width="130" height="14" fill="{G}" stroke="{N}" stroke-width="2.5"/>
<rect x="566" y="604" width="34" height="22" fill="{G}" stroke="{N}" stroke-width="2.5"/>
<rect x="584" y="582" width="34" height="22" fill="{G}" stroke="{N}" stroke-width="2.5" transform="rotate(10 601 593)"/>'''
    crate = (f'<rect x="60" y="586" width="130" height="66" rx="4" fill="{G}" stroke="{N}" stroke-width="3.5"/>'
             f'<line x1="60" y1="619" x2="190" y2="619" stroke="{N}" stroke-width="3"/>')
    sitter = robot(125, 618, .95,
                   rarm(-44, -86, -40, -20, -66, -50) + rarm(44, -86, 40, -20, 66, -50)
                   + f'<path d="M62 -168 Q53 -152 62 -146 Q71 -152 62 -168 Z" fill="{W}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>',
                   mouth="wavy")
    left = floor(320, 656, 290) + ghost + crane + stub + frame + walls + mess + crate + sitter
    # 오른쪽: 작지만 완성된 집
    house = f'''
<rect x="790" y="470" width="220" height="180" fill="{W}" stroke="{N}" stroke-width="5"/>
<path d="M770 480 L900 370 L1030 480 Z" fill="{N}" stroke="{N}" stroke-width="5" stroke-linejoin="round"/>
<rect x="870" y="560" width="56" height="90" rx="4" fill="{G}" stroke="{N}" stroke-width="4"/>
<circle cx="914" cy="606" r="4" fill="{N}"/>
<rect x="808" y="506" width="44" height="40" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="948" y="506" width="44" height="40" fill="{G}" stroke="{N}" stroke-width="3"/>
<line x1="830" y1="506" x2="830" y2="546" stroke="{N}" stroke-width="2"/><line x1="970" y1="506" x2="970" y2="546" stroke="{N}" stroke-width="2"/>
<line x1="900" y1="372" x2="900" y2="270" stroke="{N}" stroke-width="5" stroke-linecap="round"/>
<path d="M902 274 L966 290 L902 308 Z" fill="{O}" stroke="{N}" stroke-width="3" stroke-linejoin="round"/>'''
    owner = person(1130, 655 - 152 * .7, .7,
                   extra_back=parm(-54, -140, -56, -34, -120, -84) + parm(54, -140, 56, -34, 120, -84),
                   legs=True)
    sparkle = f'<path d="M1000 300 L1000 324 M988 312 L1012 312 M1060 350 L1060 366 M1052 358 L1068 358" stroke="{N}" stroke-width="4" stroke-linecap="round"/>'
    right = floor(960, 656, 270) + house + owner + sparkle
    return left + f'<line x1="640" y1="190" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right
