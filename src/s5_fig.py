"""5교시 도해 · 요청문 가이드 부품 (원본 교안 그림을 이 덱 스타일로 다시 그림)."""
from fig import ic

R, K, G, M = "#E8002D", "#26262B", "#DCDCE1", "#6B6B73"


# ── 요청문 작성 가이드 ─────────────────────────────────────────

def guide(qs, keys, conds=None, where=""):
    """왼쪽: 가이드라인 질문 + 키워드 · 오른쪽: 실습 조건."""
    w = f'<div class="g5-where">{ic("chat")}<span>Claude Code · 직접 작성{" · " + where if where else ""}</span></div>'
    q = "".join(f"<li>{x}</li>" for x in qs)
    k = "".join(f"<span>{x}</span>" for x in keys)
    left = f'{w}<div class="g5-h">작성 가이드라인</div><ul class="g5-q">{q}</ul><div class="g5-h">키워드</div><div class="g5-kw">{k}</div>'
    if conds is None:
        return f'<div class="g5 one">{left}</div>'
    return f'<div class="g5"><div class="g5-l">{left}</div><div class="g5-r">{cond(conds)}</div></div>'


def cond(rows, title="실습 조건"):
    li = "".join(f'<div class="c5-r"><b>{a}</b><span>{b}</span></div>' for a, b in rows)
    return f'<div class="c5"><div class="c5-h">{title}</div>{li}</div>'


# ── 개념 도해 ─────────────────────────────────────────────────

def api_fig():
    """내 앱 ↔ 다른 서비스: 정해진 형식으로 요청 · 결과."""
    return ('<div class="a5">'
            f'<div class="a5-box">{ic("window")}<b>내 앱</b><span>내가 만드는 것</span></div>'
            '<div class="a5-mid"><div class="a5-arr">정해진 형식으로 <b>요청</b><i></i></div>'
            '<div class="a5-gate">API</div>'
            '<div class="a5-arr back"><i></i>정해진 형식으로 <b>결과</b></div></div>'
            f'<div class="a5-box on">{ic("globe")}<b>다른 서비스</b><span>환율 · 날씨 · 지도 · 번역</span></div>'
            '</div>')


def chain(items, back=""):
    """아이콘 타일 연쇄. items: [(icon, title, desc, hl)]"""
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc{" t5on" if hl else ""}"><div class="fi">{ic(i)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>'
        for i, t, d, hl in items)
    b = f'<div class="tback">{back}</div>' if back else ""
    return f'<div class="tcall">{cells}</div>{b}'


def arch(tags=None):
    """agent-sim → MCP(8790) → rag-sim 기존 검색, MCP 서버는 rag-sim 관리 탭에서 On/off."""
    t = tags or ["", "", ""]
    tg = lambda i: f'<em>{t[i]}</em>' if t[i] else ""
    return ('<div class="r5">'
            '<div class="r5-row">'
            f'<div class="r5-n">{tg(0)}{ic("model")}<b>agent-sim</b><span>127.0.0.1:8770</span><span>LLM이 도구 선택</span></div>'
            '<div class="r5-a">tools/call<i>→</i></div>'
            f'<div class="r5-n on">{tg(1)}{ic("plug")}<b>MCP 서버</b><span>127.0.0.1:8790/mcp</span><span>rag_search Tool</span></div>'
            '<div class="r5-a">함수 호출<i>→</i></div>'
            f'<div class="r5-n">{tg(2)}{ic("folder")}<b>rag-sim 기존 검색</b><span>저장소 · 검색 설정</span><span>원문 · 출처</span></div>'
            '</div>'
            '<div class="r5-tab"><b>rag-sim 화면 · 127.0.0.1:8765 · [MCP 관리] 탭</b>'
            '<span>MCP 서버 On/off · 실행 상태 · 접속 주소 · 호출 로그</span></div>'
            '</div>')


def mcp_seq():
    """등록부터 호출까지 6단계 (앱의 MCP 클라이언트가 서버와 통신)."""
    X = {"L": 170, "A": 580, "S": 990}
    s = [f'<defs><marker id="m5a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 Z" fill="{K}"/></marker>'
         f'<marker id="m5r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 Z" fill="{R}"/></marker></defs>']
    heads = [("L", "LLM", "도구 선택 · 답변"), ("A", "앱 · MCP 클라이언트", "agent-sim"), ("S", "MCP 서버", "도구 제공 · 실행")]
    for k, t, d in heads:
        x = X[k]
        fill, tc = (K, "#fff") if k == "A" else ("#fff", K)
        s.append(f'<rect x="{x-140}" y="8" width="280" height="58" rx="12" fill="{fill}" stroke="{K}" stroke-width="2"/>'
                 f'<text x="{x}" y="34" text-anchor="middle" class="q5t" fill="{tc}">{t}</text>'
                 f'<text x="{x}" y="55" text-anchor="middle" class="q5s" fill="{"#C9C9CF" if k == "A" else M}">{d}</text>'
                 f'<line x1="{x}" y1="66" x2="{x}" y2="455" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>')
    rows = [  # (단계, from, to, 글, 빨강)
        ("1", "A", "A", "활성 서버 설정 읽기 · URL은 HTTP 접속 · 로컬 명령은 별도 프로세스", False),
        ("2", "A", "S", "initialize · 초기화 완료 알림", False),
        ("3", "A", "S", "tools/list", False),
        ("", "S", "A", "도구 이름 · 설명 · 입력 형식", False),
        ("4", "A", "A", "OpenAI 도구 선언 형식으로 변환 · 도구 목록에 등록", False),
        ("5", "A", "L", "질문 + 도구 선언", False),
        ("", "L", "A", "도구 이름 · 인자", True),
        ("", "A", "S", "tools/call", True),
        ("6", "S", "A", "실제 검색 결과", True),
        ("", "A", "L", "다음 입력에 결과 포함 → 답변", True),
    ]
    y = 100
    for no, a, b, txt, red in rows:
        c, mk = (R, "m5r") if red else (K, "m5a")
        if no:
            s.append(f'<circle cx="40" cy="{y-4}" r="14" fill="{R}"/><text x="40" y="{y+1}" text-anchor="middle" class="q5n">{no}</text>')
        if a == b:
            x = X[a]
            s.append(f'<rect x="{x-250}" y="{y-20}" width="500" height="32" rx="8" fill="#F5F5F7" stroke="{G}"/>'
                     f'<text x="{x}" y="{y+2}" text-anchor="middle" class="q5s" fill="{K}">{txt}</text>')
        else:
            x1, x2 = X[a], X[b]
            d = 1 if x2 > x1 else -1
            s.append(f'<line x1="{x1 + d*6}" y1="{y}" x2="{x2 - d*8}" y2="{y}" stroke="{c}" stroke-width="2.6" marker-end="url(#{mk})"/>'
                     f'<text x="{(x1+x2)/2}" y="{y-8}" text-anchor="middle" class="q5l" fill="{c}">{txt}</text>')
        y += 37
    return f'<svg viewBox="0 0 1180 460" class="q5">{"".join(s)}</svg>'


def mapping():
    """Tool의 question → API의 query."""
    return ('<div class="m5">'
            '<div class="m5-c"><div class="m5-h">LLM이 고르는 Tool</div><code>rag_search(</code>'
            '<div class="m5-k">question <small>문자열 · 필수</small></div>'
            '<div class="m5-k">top_k <small>정수 · 선택 · 기본 5</small></div><code>)</code></div>'
            '<div class="m5-m"><span>question → query</span><span>top_k → top_k</span><span>URL 인코딩</span></div>'
            '<div class="m5-c on"><div class="m5-h">rag-sim 검색 API</div><code>GET 127.0.0.1:8780/api/search</code>'
            '<div class="m5-k">?query= <small>질문</small></div>'
            '<div class="m5-k">&amp;top_k= <small>청크 수</small></div><code>→ JSON 반환</code></div>'
            '</div>')
