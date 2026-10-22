"""그림 공통 부품. 모든 장면은 viewBox 0 0 1280 720 안의 SVG 조각을 돌려준다.

색은 남색 N · 밝은 회색 G · 주황 O · 흰색 W 네 가지만 쓴다.
로봇: robot(x, y, s, extra, mouth) — 원점은 발 가운데, 어깨 (±44,-86), 머리 중심 (0,-147), 키 약 210*s.
회사원: person(x, y, s, extra_back, extra_front, legs) — 원점은 허리, 어깨 (±54,-140), 머리 중심 (0,-210).
  legs=True 면 다리(허리 아래 152*s)까지 그린다. 서 있게 하려면 y = 바닥 - 152*s.
팔: rarm / parm 은 각 인물의 로컬 좌표로 extra 안에 넣는다.
"""

N, G, O, W = "#26262B", "#DCDCE1", "#E8002D", "#FFFFFF"  # 코리안리 덱 색 (원본: 농심 덱 ai-grounding)

# ── 공통 인물 ─────────────────────────────────────────────
# 로봇: 원점 = 발 가운데. 어깨 (±44,-86). 입·팔은 장면마다 따로 그린다.
ROBOT = f'''<g id="robot">
  <line x1="0" y1="-190" x2="0" y2="-206" stroke="{N}" stroke-width="4"/>
  <circle cx="0" cy="-210" r="7" fill="{N}"/>
  <rect x="-12" y="-108" width="24" height="14" fill="{N}"/>
  <rect x="-30" y="-34" width="20" height="34" rx="6" fill="{N}"/>
  <rect x="10" y="-34" width="20" height="34" rx="6" fill="{N}"/>
  <rect x="-44" y="-98" width="88" height="70" rx="20" fill="{G}" stroke="{N}" stroke-width="4"/>
  <circle cx="0" cy="-64" r="9" fill="{W}" stroke="{N}" stroke-width="3"/>
  <rect x="-54" y="-190" width="108" height="86" rx="43" fill="{G}" stroke="{N}" stroke-width="4"/>
  <rect x="-38" y="-172" width="76" height="50" rx="22" fill="{W}" stroke="{N}" stroke-width="3"/>
  <circle cx="-15" cy="-152" r="7.5" fill="{O}"/>
  <circle cx="15" cy="-152" r="7.5" fill="{O}"/>
</g>'''

# 회사원 상반신: 원점 = 허리. 어깨 (±54,-140). 머리 중심 (0,-210).
PERSON = f'''<g id="person">
  <circle cx="-38" cy="-206" r="8" fill="{W}" stroke="{N}" stroke-width="3"/>
  <circle cx="38" cy="-206" r="8" fill="{W}" stroke="{N}" stroke-width="3"/>
  <rect x="-11" y="-178" width="22" height="24" fill="{W}" stroke="{N}" stroke-width="3"/>
  <path d="M-58 0 L-62 -118 Q-60 -150 -28 -158 L28 -158 Q60 -150 62 -118 L58 0 Z" fill="{N}"/>
  <path d="M-20 -158 L0 -116 L20 -158 Z" fill="{W}"/>
  <path d="M-5 -152 L5 -152 L8 -112 L0 -102 L-8 -112 Z" fill="{G}"/>
  <path d="M-20 -158 L-6 -96 M20 -158 L6 -96" stroke="{G}" stroke-width="2" fill="none"/>
  <circle cx="0" cy="-210" r="38" fill="{W}" stroke="{N}" stroke-width="4"/>
  <path d="M-41 -206 Q-46 -256 0 -256 Q44 -256 41 -208 Q30 -234 -2 -234 Q-28 -232 -41 -206 Z" fill="{N}"/>
  <circle cx="-13" cy="-204" r="3.8" fill="{N}"/>
  <circle cx="13" cy="-204" r="3.8" fill="{N}"/>
  <path d="M-10 -188 Q0 -180 10 -188" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>
</g>
<g id="legs">
  <rect x="-50" y="-4" width="44" height="146" rx="8" fill="{G}" stroke="{N}" stroke-width="3"/>
  <rect x="6" y="-4" width="44" height="146" rx="8" fill="{G}" stroke="{N}" stroke-width="3"/>
  <ellipse cx="-30" cy="148" rx="28" ry="10" fill="{N}"/>
  <ellipse cx="30" cy="148" rx="28" ry="10" fill="{N}"/>
</g>'''

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
{ROBOT}
{PERSON}
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
</defs></svg>'''


def robot(x, y, s, extra="", mouth="smile"):
    """extra = 로봇 좌표계에서 그릴 팔·소품. 몸 위에 그려진다."""
    m = {
        "smile": f'<path d="M-9 -138 Q0 -131 9 -138" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "grin": f'<path d="M-14 -140 Q0 -124 14 -140" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "wavy": f'<path d="M-12 -134 Q-6 -140 0 -134 Q6 -128 12 -134" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "flat": f'<path d="M-9 -135 L9 -135" stroke="{N}" stroke-width="3" stroke-linecap="round"/>',
    }[mouth]
    return f'<g transform="translate({x},{y}) scale({s})"><use href="#robot"/>{m}{extra}</g>'


def rarm(x1, y1, x2, y2, cx=None, cy=None, hand=True):
    """로봇 팔. 손은 회색 원."""
    d = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}" if cx is not None else f"M{x1} {y1} L{x2} {y2}"
    h = f'<circle cx="{x2}" cy="{y2}" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>' if hand else ""
    return f'<path d="{d}" stroke="{N}" stroke-width="9" fill="none" stroke-linecap="round"/>{h}'


def person(x, y, s, extra_back="", extra_front="", legs=False):
    lg = '<use href="#legs"/>' if legs else ""
    return (f'<g transform="translate({x},{y}) scale({s})">{lg}{extra_back}'
            f'<use href="#person"/>{extra_front}</g>')


def parm(x1, y1, x2, y2, cx=None, cy=None, hand=True):
    """회사원 팔. 남색 소매 + 흰 손."""
    d = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}" if cx is not None else f"M{x1} {y1} L{x2} {y2}"
    h = f'<circle cx="{x2}" cy="{y2}" r="12" fill="{W}" stroke="{N}" stroke-width="3"/>' if hand else ""
    return f'<path d="{d}" stroke="{N}" stroke-width="22" fill="none" stroke-linecap="round"/>{h}'


def lines(x1, x2, ys, color=G, w=6):
    return "".join(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>' for y in ys)


def floor(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="14" fill="{G}"/>'




def webdoc(x, y, w, h, rot):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
            f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="14" rx="4" fill="{G}"/>'
            + "".join(f'<circle cx="{x+12+i*10}" cy="{y+9}" r="3" fill="{N}"/>' for i in range(3))
            + lines(x + 14, x + w - 14, [y + 34, y + 50, y + 66][: max(1, (h - 30) // 18)])
            + "</g>")

