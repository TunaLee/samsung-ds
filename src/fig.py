"""그림 요소: 개념 도해와 화면 모형. 모두 HTML · 인라인 SVG라 외부 파일 없이 그려진다."""

ICONS = {  # 24×24 선 아이콘 (stroke = currentColor)
    "model": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><rect x="10" y="10" width="4" height="4"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-2.5z"/>',
    "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
    "folder": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "plug": '<path d="M9 2v5M15 2v5"/><path d="M6 7h12v4a6 6 0 0 1-12 0z"/><path d="M12 17v5"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M2 20h20"/>',
    "rule": '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
    "clip": '<path d="M21 11l-8.5 8.5a5 5 0 0 1-7-7L14 4a3.5 3.5 0 0 1 5 5l-8.5 8.5a2 2 0 0 1-3-3L15 7"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M7 9l2 7 3-6 3 6 2-7M6.5 12h11"/>',
    "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "form": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "nodes": '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M8.5 6h7M7.3 8.2l3.5 7.6M16.7 8.2l-3.5 7.6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "report": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 17v-3M12 17v-6M15 17v-4"/>',
    "window": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    "html": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M10 12l-2 2 2 2M14 12l2 2-2 2"/>',
}


def ic(name):
    return (f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')



def _tile(icon, title, desc, cls=""):
    return f'<div class="ftile {cls}"><div class="fi">{ic(icon)}</div><div class="ft">{title}</div><div class="fd">{desc}</div></div>'


# ── 개념 도해 ───────────────────────────────────────────────

def agent_parts():
    """에이전트 = 모델 + 도구 + 지침 + 자료."""
    return ('<div class="parts">'
            + _tile("model", "모델", "읽기 · 판단 · 작성", "core")
            + '<div class="plus">+</div>'
            + _tile("tool", "도구", "검색 · 파일 · 시트 · 캘린더<br>외부 자료 조회")
            + '<div class="plus">+</div>'
            + _tile("book", "지침", "팀의 작업 규칙<br>업무 매뉴얼")
            + '<div class="plus">+</div>'
            + _tile("folder", "자료", "양식 · 예시 · 지난 결과<br>참고자료")
            + '</div>')


def agent_loop(ask="「이번 주 보고서 써 줘」", out="보고서 초안", steps=None):
    """요청 → 계획 → 도구 실행 → 결과 확인 → (반복) → 답."""
    st = steps or [("계획", "무엇이 필요한지"), ("도구 실행", "시트 · 캘린더 읽기"), ("결과 확인", "빠진 것 · 틀린 것"), ("다시", "부족하면 한 번 더")]
    nodes = [(t, d, x, y) for (t, d), (x, y) in zip(st, [(300, 70), (500, 190), (300, 310), (100, 190)])]
    svg = ['<svg viewBox="0 0 600 380" class="loop">',
           '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#E8002D"/></marker></defs>',
           '<circle cx="300" cy="190" r="120" fill="none" stroke="#F3C0CB" stroke-width="3" stroke-dasharray="8 8"/>']
    arcs = ["M370 95 Q450 120 470 160", "M470 225 Q450 270 370 290", "M230 290 Q150 270 130 225", "M130 160 Q150 115 230 95"]
    for d in arcs:
        svg.append(f'<path d="{d}" fill="none" stroke="#E8002D" stroke-width="3" marker-end="url(#ah)"/>')
    for t, s, x, y in nodes:
        svg.append(f'<rect x="{x - 78}" y="{y - 32}" width="156" height="64" rx="12" fill="#fff" stroke="#111" stroke-width="2"/>'
                   f'<text x="{x}" y="{y - 4}" text-anchor="middle" class="lt">{t}</text>'
                   f'<text x="{x}" y="{y + 18}" text-anchor="middle" class="ls">{s}</text>')
    svg.append('<text x="300" y="186" text-anchor="middle" class="lc">스스로 반복</text>'
               '<text x="300" y="210" text-anchor="middle" class="ls">끝날 때까지</text></svg>')
    return (f'<div class="loopwrap"><div class="lend">요청<br><b>{ask}</b></div>'
            + "".join(svg) + f'<div class="lend r">답<br><b>{out}</b></div></div>')


def tool_call():
    """모델은 직접 접속하지 않는다 — 도구에 부탁하고, 도구는 내 권한으로 가져온다."""
    st = [("chat", "나", "「이번 주 현황 요약해 줘」"), ("model", "ChatGPT", "「시트가 필요해」 판단"),
          ("plug", "플러그인", "Google Drive"), ("key", "내 권한", "연결할 때 허용한 범위만"),
          ("chart", "내 시트", "팀 업무 현황")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc"><div class="fi">{ic(i)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>' for i, t, d in st)
    return (f'<div class="tcall">{cells}</div>'
            '<div class="tback">읽어 온 내용으로 ChatGPT가 요약</div>')


def disclosure():
    """스킬은 설명만 먼저 읽고, 필요할 때 본문 · 파일을 펼친다."""
    return ('<div class="disc">'
            '<div class="dl"><div class="dk">항상</div><div class="dbar w1"><b>이름 · 설명</b> 한두 줄</div>'
            '<div class="dn">스킬이 30개여도 설명만 확인</div></div>'
            '<div class="dl"><div class="dk">요청이 맞으면</div><div class="dbar w2"><b>지침 본문</b> 규칙 · 순서 · 형식</div>'
            '<div class="dn">「주간 보고」 요청 → 이 스킬의 지침만 불러옴</div></div>'
            '<div class="dl"><div class="dk">더 필요하면</div><div class="dbar w3"><b>참고 파일</b> 양식 · 예시 · 메일</div>'
            '<div class="dn">작성 중 필요한 파일만 열람</div></div>'
            '</div>')


def bundle():
    """플러그인 = 스킬 + 앱 묶음."""
    return ('<div class="bundle"><div class="bh">플러그인 · 「팀 업무 보고」</div><div class="bb">'
            '<div class="bs"><span>SKILL</span><b>주간업무보고</b><i>4항목 · 마감 초과 맨 위 · 추정 금지</i></div>'
            '<div class="bs app"><span>APP</span><b>Google Drive</b><i>팀 업무 현황 시트 읽기</i></div>'
            '<div class="bs app"><span>APP</span><b>Google Calendar</b><i>팀 일정 읽기</i></div>'
            '</div><div class="bf">한 번 설치로 지침과 앱 연결을 함께 사용</div></div>')


def forgetting():
    """대화창 지시는 흘러가고, 저장한 지침은 남는다."""
    lines = ["지난주: 「4항목 · 마감 초과 맨 위로」", "…", "다른 질문", "다른 질문", "…", "이번 주: 「보고서 써 줘」"]
    chat = "".join(f'<div class="fl" style="opacity:{0.25 + i * 0.15:.2f}">{t}</div>' for i, t in enumerate(lines))
    return ('<div class="forget">'
            f'<div class="fc"><div class="fh">대화창에만 말한 규칙</div>{chat}<div class="fx">앞서 말한 규칙은 잊힘 · 매번 다시 설명</div></div>'
            '<div class="fc good"><div class="fh">스킬로 저장한 규칙</div>'
            '<div class="pin">주간업무보고<br><small>4항목 · 마감 초과 맨 위 · 추정 금지</small></div>'
            '<div class="fl">이번 주: 「보고서 써 줘」</div><div class="fx ok">새 대화에서도 같은 규칙</div></div></div>')


def timeline(items):
    """items: [(시기, 제목, 설명, 강조여부)]"""
    out = "".join(f'<div class="tl{" on" if hl else ""}"><div class="ty">{y}</div><div class="tdot"></div>'
                  f'<div class="tt">{t}</div><div class="td">{d}</div></div>' for y, t, d, hl in items)
    return f'<div class="tline">{out}</div>'


# ── 화면 모형 ───────────────────────────────────────────────

def window(title, body, kind="app"):
    return (f'<div class="win {kind}"><div class="wbar"><i></i><i></i><i></i><span>{title}</span></div>'
            f'<div class="wbody">{body}</div></div>')


def sheet(rows, title="팀 업무 현황"):
    head = '<tr><th></th>' + "".join(f"<th>{c}</th>" for c in "ABCDE") + "</tr>"
    body = "".join(f'<tr><th>{i + 1}</th>' + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for i, r in enumerate(rows))
    return window(title + " · Google 시트", f'<table class="gsheet">{head}{body}</table>', "gs")


def calendar(events):
    """events: [(요일 0~4, 시작 시 9~18 소수, 길이 시간, 제목)]"""
    days = "월화수목금"
    cols = ""
    for d in range(5):
        ev = "".join(f'<div class="ev" style="top:{(s - 9) * 14}px;height:{max(l * 14, 14)}px">{t}</div>'
                     for dd, s, l, t in events if dd == d)
        cols += f'<div class="cd"><div class="ch">{days[d]}</div><div class="cb">{ev}</div></div>'
    return window("실습용 팀 일정 · Google 캘린더", f'<div class="gcal">{cols}</div>', "gc")


def skill_editor(name, desc, guide, files):
    f = "".join(f'<span class="file">{ic("doc")}{x}</span>' for x in files)
    return window("스킬 만들기", (
        f'<div class="se"><label>이름</label><div class="in">{name}</div>'
        f'<label>설명 <em>← 언제 부를지 정함</em></label><div class="in">{desc}</div>'
        f'<label>지침</label><div class="in ta">{guide}</div>'
        f'<label>참고 파일</label><div class="files">{f}</div>'
        '<div class="sv">저장</div></div>'), "se-w")


def report_card(rows, title="주간업무보고_결과"):
    """rows: [(업무, 진행률, 배지, 배지종류)]"""
    body = "".join(f'<div class="rr"><span>{a}</span><b>{b}</b><em class="{k}">{c}</em></div>' for a, b, c, k in rows)
    return window(title, f'<div class="rcard">{body}</div>', "doc")


def bars(items, unit="%", hl=None, top=100):
    """가로 막대. items: [(이름, 값)]"""
    out = ""
    for i, (n, v) in enumerate(items):
        c = " on" if hl is not None and (i == hl or n == hl) else ""
        out += (f'<div class="br{c}"><span class="bn">{n}</span><span class="bt"><i style="width:{v / top * 100:.1f}%"></i></span>'
                f'<span class="bv">{v}{unit}</span></div>')
    return f'<div class="bars">{out}</div>'


def kpis(items):
    """items: [(라벨, 값, 단위, 보조)]"""
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><span>{l}</span><b>{v}<small>{u}</small></b><em>{s}</em></div>' for l, v, u, s in items) + "</div>"


def browser(url, body):
    return (f'<div class="win br-w"><div class="wbar"><i></i><i></i><i></i><span class="url">{url}</span></div>'
            f'<div class="wbody">{body}</div></div>')


def file_flow():
    """요청문 → 미리보기 → .html 파일 → 브라우저."""
    st = [("chat", "요청문", "만들 화면을 말로"), ("window", "미리보기", "대화창 코드 블록에서 확인"),
          ("html", ".html 파일", "내려받기 · 한 파일"), ("globe", "브라우저", "더블클릭 · 메일 첨부")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc"><div class="fi">{ic(i)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>' for i, t, d in st)
    return f'<div class="tcall">{cells}</div>'


def research_flow():
    st = [("search", "웹 검색", "ChatGPT가 공개 자료 찾기"), ("link", "링크 확인", "직접 열어 숫자 대조"),
          ("chart", "표 · CSV", "확인한 값만"), ("report", "보고서 HTML", "요약 · 근거 · 출처")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc"><div class="fi">{ic(i)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>' for i, t, d in st)
    return f'<div class="tcall">{cells}</div>'


def a4(cut):
    """인쇄 미리보기: 잘린 것 vs 맞춘 것."""
    w = 150 if cut else 100
    cls = "cut" if cut else "fit"
    return (f'<div class="a4 {cls}"><div class="a4h"></div><div class="a4l"></div><div class="a4l s"></div>'
            f'<div class="a4t" style="width:{w}%"></div><div class="a4t" style="width:{w}%"></div>'
            f'<div class="a4c" style="width:{w * .9}%"></div></div>')
