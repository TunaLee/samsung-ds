"""웹 구조 도해 (농심 덱 deck_gas 에서 가져와 문구를 일반 사무용으로 바꿈)."""
from art import G, N, O, W

_P = ["a"]  # 그림마다 화살표 머리 id 를 다르게 (숨은 장의 id 를 참조하면 안 보인다)
_MARKERS = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{N}"/></marker>'
            f'<marker id="aho" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{O}"/></marker></defs>')
SOFT = "#F1F1F4"


def markers(prefix):
    _P[0] = prefix
    return _MARKERS.replace('id="ah"', f'id="{prefix}ah"').replace('id="aho"', f'id="{prefix}aho"')


def box(x, y, w, h, title, sub="", fill=W, stroke=N, tcolor=N, rx=14, scls="bs"):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    s += f'<text x="{x+w/2}" y="{y+(h/2 if not sub else h/2-8)}" text-anchor="middle" dominant-baseline="middle" class="bt" fill="{tcolor}">{title}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" dominant-baseline="middle" class="{scls}">{sub}</text>'
    return s


def arrow(x1, y1, x2, y2, color=N, dash="", w=3, mid="ah"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d} marker-end="url(#{_P[0]}{mid})"/>'


def browser(x, y, w, h, inner):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{G}"/><rect x="{x}" y="{y+14}" width="{w}" height="12" fill="{G}"/>'
            + "".join(f'<circle cx="{x+16+i*14}" cy="{y+13}" r="4" fill="{N}"/>' for i in range(3))
            + inner)


def bars(x, y, hs, color=N, bw=22, gap=12):
    return "".join(f'<rect x="{x+i*(bw+gap)}" y="{y-h}" width="{bw}" height="{h}" rx="3" fill="{color}"/>' for i, h in enumerate(hs))


def db(x, y, w=120, h=130, label="시트"):
    ry = 16
    return (f'<path d="M{x} {y+ry} L{x} {y+h-ry} A{w/2} {ry} 0 0 0 {x+w} {y+h-ry} L{x+w} {y+ry}" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+ry}" rx="{w/2}" ry="{ry}" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M{x} {y+h*0.45} A{w/2} {ry} 0 0 0 {x+w} {y+h*0.45}" fill="none" stroke="{N}" stroke-width="2"/>'
            f'<path d="M{x} {y+h*0.7} A{w/2} {ry} 0 0 0 {x+w} {y+h*0.7}" fill="none" stroke="{N}" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{y+h+30}" text-anchor="middle" class="bt" fill="{N}">{label}</text>')


def folder(x, y, w=140, h=104, label="드라이브"):
    return (f'<path d="M{x} {y+18} Q{x} {y} {x+18} {y} L{x+50} {y} L{x+64} {y+16} L{x+w-14} {y+16} Q{x+w} {y+16} {x+w} {y+30} '
            f'L{x+w} {y+h-14} Q{x+w} {y+h} {x+w-14} {y+h} L{x+14} {y+h} Q{x} {y+h} {x} {y+h-14} Z" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{x+22}" y="{y+34}" width="{w*0.32}" height="{h*0.42}" rx="4" fill="{W}" stroke="{N}" stroke-width="2"/>'
            f'<rect x="{x+w*0.5}" y="{y+42}" width="{w*0.32}" height="{h*0.42}" rx="4" fill="{W}" stroke="{N}" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{y+h+30}" text-anchor="middle" class="bt" fill="{N}">{label}</text>')


def static_web():
    mk = markers("st")
    page = browser(760, 70, 330, 250, bars(800, 290, [90, 140, 70, 170, 120], G))
    file_ = (f'<path d="M140 90 L250 90 L290 130 L290 300 L140 300 Z" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<path d="M250 90 L250 130 L290 130" fill="none" stroke="{N}" stroke-width="3"/>'
             + "".join(f'<rect x="160" y="{150+i*26}" width="{100 - (i%2)*30}" height="9" rx="4" fill="{G}"/>' for i in range(5))
             + f'<text x="215" y="340" text-anchor="middle" class="bt" fill="{N}">완성된 HTML 파일</text>'
             + f'<text x="215" y="366" text-anchor="middle" class="bs">숫자가 파일 안에 고정</text>')
    flowline = arrow(310, 195, 740, 195, N, w=4) + '<text x="525" y="178" text-anchor="middle" class="bs">메일 첨부 · 그대로 전달</text>'
    return f'''<svg viewBox="0 0 1180 400" class="websvg">{mk}{file_}{flowline}{page}
<text x="925" y="352" text-anchor="middle" class="bt" fill="{N}">브라우저</text>
<text x="925" y="378" text-anchor="middle" class="bs">숫자를 바꾸려면 파일을 다시 만듦</text></svg>'''


def dynamic_web():
    mk = markers("dy")
    page = browser(40, 80, 300, 230, bars(80, 280, [80, 120, 150, 100, 170], O))
    server = box(470, 120, 220, 150, "Apps Script", "화면 틀 + 데이터", fill=SOFT)
    sheet = db(880, 110)
    req = (arrow(345, 130, 465, 130, N, "7 6") + '<text x="405" y="112" text-anchor="middle" class="bs">① 요청</text>'
           + arrow(695, 150, 875, 150, N, "7 6") + '<text x="785" y="132" text-anchor="middle" class="bs">② 조회</text>')
    res = (arrow(875, 250, 695, 250, O, w=4, mid="aho") + '<text x="785" y="282" text-anchor="middle" class="bso">③ 최신 데이터</text>'
           + arrow(465, 270, 345, 270, O, w=4, mid="aho") + '<text x="405" y="302" text-anchor="middle" class="bso">④ 화면 그리기</text>')
    dots = "".join(
        f'<circle r="8" fill="{O}"><animateMotion dur="2.4s" begin="{d}s" repeatCount="indefinite" path="M875 250 L695 250 L580 260 L465 270 L345 270"/></circle>'
        for d in (0, .8, 1.6))
    return f'''<svg viewBox="0 0 1180 400" class="websvg">{mk}{page}{server}{sheet}{req}{res}{dots}
<text x="190" y="350" text-anchor="middle" class="bt" fill="{N}">브라우저</text>
<text x="190" y="376" text-anchor="middle" class="bs">열 때마다 지금 숫자</text></svg>'''


def pipeline():
    """업무 관리 웹 전체 구조 — 화면 입력 · 업로드 → Apps Script → 시트 · 드라이브 → 화면 · AI."""
    s = markers("pl")
    s += browser(40, 30, 300, 150, bars(80, 160, [40, 70, 55, 90], O, bw=26, gap=16))
    s += f'<text x="190" y="210" text-anchor="middle" class="bt" fill="{N}">업무 관리 웹</text><text x="190" y="236" text-anchor="middle" class="bs">입력 · 수정 · 파일 올리기</text>'
    s += box(470, 60, 240, 110, "Apps Script", "검증 · 저장 · 조회", fill=SOFT)
    s += db(840, 40, 120, 110, "시트 · 기록")
    s += folder(1000, 46, 140, 104, "드라이브 · 파일")
    s += arrow(345, 100, 465, 100, O, w=4, mid="aho") + arrow(715, 90, 835, 90, O, w=4, mid="aho")
    s += arrow(715, 140, 995, 140, O, w=4, mid="aho")
    s += box(470, 300, 240, 100, "ChatGPT + 플러그인", "시트 · 드라이브 읽기", fill=N, stroke=N, tcolor=W, scls="bsw")
    s += arrow(900, 230, 715, 330, N, "7 6") + arrow(1070, 230, 715, 360, N, "7 6")
    s += box(840, 330, 300, 90, "주간 보고 · 분석 초안", "AI가 쌓인 기록을 정리", fill=W)
    s += arrow(715, 375, 835, 375, N, w=3)
    return f'<svg viewBox="0 0 1180 440" class="websvg pipe2">{s}</svg>'


def lock(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-12 0 V-10 A12 12 0 0 1 12 -10 V0" fill="none" stroke="{O}" stroke-width="5"/>'
            f'<rect x="-18" y="0" width="36" height="28" rx="6" fill="{O}"/><circle cx="0" cy="12" r="4" fill="{W}"/></g>')


def proxy():
    """원본 시트는 잠가 두고, 웹 앱(실행: 나)이 대신 접근."""
    s = markers("px")
    s += f'<rect x="30" y="20" width="560" height="420" rx="22" fill="#F7F7F9" stroke="{N}" stroke-width="2.5" stroke-dasharray="9 7"/>'
    s += f'<text x="58" y="56" class="bt" fill="{N}">내 Google 계정</text>'
    s += db(110, 120, 130, 140, "")
    s += lock(175, 104, 1.1)
    s += f'<text x="175" y="300" text-anchor="middle" class="bt" fill="{N}">시트 · 드라이브</text>'
    s += '<text x="175" y="326" text-anchor="middle" class="bs">공유: 제한됨 · 나만</text>'
    s += box(360, 150, 190, 120, "Apps Script", "실행: 나", fill=SOFT)
    s += arrow(355, 190, 245, 190) + arrow(245, 230, 355, 230)
    s += '<text x="300" y="176" text-anchor="middle" class="bs">읽기</text><text x="300" y="256" text-anchor="middle" class="bs">쓰기</text>'
    s += '<text x="455" y="300" text-anchor="middle" class="bs">내 권한으로 대신 접근</text>'
    s += arrow(555, 210, 740, 210, O, w=4, mid="aho") + '<text x="648" y="192" text-anchor="middle" class="bso">웹 앱 주소</text>'
    for i, y in enumerate((60, 190, 320)):
        s += browser(760, y, 220, 110, bars(790, y + 95, [30, 50, 40, 60], O if i == 1 else G, bw=16, gap=10))
    s += f'<text x="1010" y="190" class="bt" fill="{N}">화면으로만</text>'
    s += '<text x="1010" y="218" class="bs">시트 직접 수정 없음</text><text x="1010" y="242" class="bs">정해진 입력만 저장</text><text x="1010" y="266" class="bs">원본은 안전</text>'
    return f'<svg viewBox="0 0 1240 460" class="websvg">{s}</svg>'
