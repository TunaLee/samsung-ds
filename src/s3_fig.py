"""3교시 도해 (원본 교안 그림을 이 덱 스타일로 다시 그림). 클래스 접두사 x3-."""
from fig import ic


def n(t, s="", cls="", icon=None, tag=""):
    i = f'<div class="x3i">{ic(icon)}</div>' if icon else ""
    tg = f'<em class="x3tag">{tag}</em>' if tag else ""
    sub = f"<span>{s}</span>" if s else ""
    return f'<div class="x3n {cls}">{tg}{i}<b>{t}</b>{sub}</div>'


def a(sym="→", cls=""):
    return f'<div class="x3a {cls}">{sym}</div>'


def row(*items, cls=""):
    return f'<div class="x3row {cls}">{"".join(items)}</div>'


def grp(label, chips, sub="", cls=""):
    c = ""
    for x in chips:
        if isinstance(x, tuple):
            c += f'<span class="x3chip {x[1]}">{x[0]}</span>'
        else:
            c += f'<span class="x3chip">{x}</span>'
    s = f'<div class="gs">{sub}</div>' if sub else ""
    return f'<div class="x3g {cls}"><div class="gl">{label}</div>{s}{c}</div>'


def lanes(rows, lead=(), merge=(), w="1fr", lw="1fr", mw="1fr"):
    """rows: [[노드 html]] 여러 줄 · lead: 앞에서 모든 줄로 갈라지는 노드 · merge: 뒤에서 모이는 노드."""
    R, k = len(rows), len(rows[0])
    cols, cells, c = [], [], 1
    for x in lead:
        cols += [lw, "30px"]
        cells.append(f'<div style="grid-column:{c};grid-row:1/span {R}" class="x3cell">{x}</div>')
        cells.append(f'<div style="grid-column:{c + 1};grid-row:1/span {R}" class="x3cell">{a()}</div>')
        c += 2
    for i in range(k):
        cols.append(w)
        for r, rw in enumerate(rows):
            cells.append(f'<div style="grid-column:{c};grid-row:{r + 1}" class="x3cell">{rw[i]}</div>')
        c += 1
        if i < k - 1:
            cols.append("30px")
            for r, rw in enumerate(rows):
                sym = "" if rw[i] == "" or rw[i + 1] == "" else a()
                cells.append(f'<div style="grid-column:{c};grid-row:{r + 1}" class="x3cell">{sym}</div>')
            c += 1
    for x in merge:
        cols += ["30px", mw]
        cells.append(f'<div style="grid-column:{c};grid-row:1/span {R}" class="x3cell">{a()}</div>')
        cells.append(f'<div style="grid-column:{c + 1};grid-row:1/span {R}" class="x3cell">{x}</div>')
        c += 2
    return f'<div class="x3lanes" style="grid-template-columns:{" ".join(cols)}">{"".join(cells)}</div>'


def legend(items):
    return '<div class="x3leg">' + "".join(f'<span><i class="{k}"></i>{t}</span>' for k, t in items) + "</div>"


# ── 1. 어디를 고칠 것인가 ─────────────────────────────

def adv_pipe():
    return (row(n("질문", icon="chat"), a(),
                grp("Pre-retrieval", ["Query Rewriting", "Query Expansion", "HyDE", ("Metadata Filter · 설명만", "d")], "질문을 검색에 맞게"),
                a(), n("검색", icon="search"), a(),
                grp("Post-retrieval", ["Reranking", "점수 기준으로 버리기"], "찾은 후보를 다시 고르기"),
                a(), n("생성", icon="model"), cls="pipe3")
            + legend([("k", "naive RAG의 단계"), ("r", "Advanced RAG가 더하는 단계"), ("d", "오늘은 설명만")]))


def fix_cycle():
    st = [("증상", "무엇이 이상한가"), ("원인", "어느 단계인가"), ("처방", "증상에 맞는 기법"), ("대조", "정말 나아졌나")]
    items = []
    for i, (t, s) in enumerate(st):
        items.append(n(t, s, "r" if i == 1 else "", tag=f"{i + 1:02d}"))
        if i < 3:
            items.append(a())
    return (row(*items, cls="big")
            + '<div class="x3back"><span>나아지지 않았으면 증상을 다시</span></div>')


# ── 2. Pre-retrieval ─────────────────────────────────

def rewrite_flow():
    return row(
        n("재작성", "원래 질의 + 문서 맥락 → LLM<br>검색할 질의 하나 생성", "", tag="1 · 원래 질의"), a(),
        n("검색", "재작성된 질의로 청크 찾기<br>문서 범위 · 검색 방식 · 최종 근거 수 유지", "r", tag="2 · 검색 질의"), a(),
        n("답변 생성", "원래 질문 + 검색된 근거 → 답변", "k", tag="3 · 원래 질문"), cls="big")


def expansion():
    qs = "".join(f'<span class="x3chip mono">{q}</span>' for q in ["package delamination cause", "moisture induced delamination", "popcorn cracking"])
    return row(n("패키지 박리 원인", "원래 질문", "k"), a(),
               f'<div class="x3g"><div class="gl">질의 N개</div>{qs}</div>', a(),
               n("각각 검색", "질의마다 검색 1회", icon="search"), a(),
               n("결과 합치기", "문서마다 다른 표현을 놓칠 가능성 감소", "r"))


# ── 3. Reranking ─────────────────────────────────────

def bookstore():
    books = [("책 1", "Agent 개념은 많음 · 통신 설명 없음", ""), ("책 2", "Agent 간 메시지 전달 방식 설명", "on"),
             ("책 3", "Tool 사용 설명만", "")]
    bl = "".join(f'<div class="x3bk {c}"><b>{t}</b><span>{d}</span></div>' for t, d, c in books)
    return ('<div class="x3two">'
            f'<div class="x3side"><div class="x3sh">1차 검색 · 빠르게 모으기</div>'
            + row(n("수많은 책", "서점 전체", icon="book"), a(), n("관련 있어 보이는 10권", "AI Agent 주제", "r", icon="search"))
            + '<div class="x3cap">관련 있어 보이는 후보를 빠르게</div></div>'
            f'<div class="x3side"><div class="x3sh">재정렬 · 펼쳐서 다시 읽기</div>'
            f'<div class="x3q">질문: AI Agent들이 서로 어떻게 통신하는지</div>{bl}'
            '<div class="x3cap">질문에 답할 내용을 가진 책부터 다시 정렬</div></div></div>')


def bi_enc():
    return lanes([[n("질문", "AI Agent들은 어떻게 통신하나요?", "k"), n("임베딩 모델", icon="model"), n("벡터 Q", "<code>[0.12, −0.31, 0.77, …]</code>")],
                  [n("문서", "Multi-Agent 시스템은 Agent 간 메시지를 주고받을 수 있다…", tag="미리 계산 · 저장"), n("임베딩 모델", icon="model"), n("벡터 D", "<code>[0.18, −0.29, 0.71, …]</code>")]],
                 merge=[n("코사인 유사도", "벡터 공간에서 가까운 정도", "r"), n("Top-K 후보", "1. 문서 A<br>2. 문서 B<br>3. 문서 C")],
                 w="1.15fr", mw=".9fr")


def cross_enc():
    pairs = "".join(f'<div class="x3pr"><span>{q}</span><i>↔</i><span>{d}</span></div>' for q, d in [("AI Agent", "Agent"), ("통신", "메시지 교환")])
    core = f'<div class="x3n r wide"><b>Cross-encoder</b><span>질문과 후보를 함께 읽기</span>{pairs}</div>'
    return lanes([[n("질문", "AI Agent들은 어떻게 통신하나요?", "k")], [n("후보 문서", "Multi-Agent 시스템은 Agent 간 메시지를 주고받을 수 있다…")]],
                 merge=[core, n("관련성 점수", '<strong class="x3big">0.93</strong>예시 값')], w="1fr", mw="1.2fr")


def pair_score():
    rows = [[n("질문 + 후보 A"), n("Reranking 모델", icon="model"), n("관련성 점수 A", cls="r")],
            [n("질문 + 후보 B"), n("Reranking 모델", icon="model"), n("관련성 점수 B", cls="r")]]
    return lanes(rows, merge=[n("점수가 높은 후보부터 선택"), n("선택된 원문 + 원래 질문"), n("답변 생성 LLM", cls="k", icon="model")], mw=".85fr")


def yn_score():
    rows = [[n("질문 + 후보 1"), n("gpt-5.4-mini", "reasoning 끔"), n("첫 토큰의 P(Y) · P(N)"), n("점수 1", cls="r")],
            ['<div class="x3dots">⋮</div>', "", "", '<div class="x3dots">⋮</div>'],
            [n("질문 + 후보 2"), n("gpt-5.4-mini", "reasoning 끔"), n("첫 토큰의 P(Y) · P(N)"), n("점수 2", cls="r")]]
    return (lanes(rows, merge=[n("점수가 높은 후보부터 정렬", cls="k")], mw=".9fr")
            + '<div class="x3formula">점수 = P(Y) ÷ (P(Y) + P(N))</div>')


def fair_compare():
    rows = [[n("기존 순서", "검색 점수 그대로"), n("상위 5개 원문"), n("답변 A", cls="k")],
            [n("쌍별 Y/N 판정", "점수순 정렬", "r"), n("상위 5개 원문"), n("답변 B", cls="k")]]
    return (lanes(rows, lead=[n("원래 질문", cls="k"), n("후보를 한 번 검색", "현재 설정 그대로 · 같은 후보를 두 경로에서 공유", "r")], lw="1fr")
            + '<div class="x3foot">두 답변의 원래 질문 · 생성 모델 · 지시문 · 설정은 동일</div>')


def sim_rel():
    def doc(k, t, rel):
        return (f'<div class="x3doc"><div class="x3dk">문서 {k}</div><p>{t}</p>'
                f'<div class="x3m"><span>Similarity</span><i><u style="width:82%"></u></i><b>높음</b></div>'
                f'<div class="x3m r"><span>Relevance</span><i><u style="width:{88 if rel else 26}%"></u></i><b>{"높음" if rel else "낮음"}</b></div></div>')
    return ('<div class="x3q big">질문: AI Agent에서 여러 Agent가 서로 통신하는 방법은 무엇인가요?</div>'
            '<div class="x3two">' + doc("A", "AI Agent는 LLM과 Tool을 사용하여 작업을 수행한다.", False)
            + doc("B", "Multi-Agent 시스템에서는 Agent 간 메시지를 전달하여 작업 결과를 공유할 수 있다.", True) + "</div>")


def rerank_order():
    d = {1: "AI Agent는 LLM과 Tool을 이용하여 작업을 수행한다.", 2: "Multi-Agent에서는 Agent 간 메시지를 전달하여 작업 결과를 공유할 수 있다.",
         3: "AI Agent는 사용자의 요청을 분석하고 행동을 결정한다."}

    def lst(order, hl):
        return "".join(f'<div class="x3li{" on" if k == hl else ""}"><b>{i + 1}</b><span><em>문서 {k}</em>{d[k]}</span></div>' for i, k in enumerate(order))
    sc = "".join(f'<div class="x3sc{" on" if k == 2 else ""}"><span>문서 {k}</span><i>→</i><b>{v}</b></div>' for k, v in [(1, "0.42"), (2, "0.95"), (3, "0.30")])
    return ('<div class="x3ro">'
            f'<div class="x3col"><div class="x3sh">1차 검색 · 비슷한 순</div>{lst([1, 2, 3], 0)}</div>'
            f'{a()}<div class="x3col mid"><div class="x3sh">Cross-encoder 재평가</div>{sc}<div class="x3cap">예시 점수 · 질문에 도움이 되는 정도</div></div>{a()}'
            f'<div class="x3col"><div class="x3sh r">재정렬 · 답에 쓸모 있는 순</div>{lst([2, 1, 3], 2)}</div></div>')


# ── 4. 정리 ──────────────────────────────────────────

def naive_adv():
    naive = row('<div class="x3lab">Naive RAG</div>', n("Query"), a(), n("Retrieval"), a(), n("Generate"), a(), n("Response", cls="k"), cls="nv")
    adv = row('<div class="x3lab r">OpenAI<br>Advanced RAG</div>', n("Query"), a(),
              grp("Pre-Retrieval", [("Query Rewriting<br><small>질문 1개 → 1개</small>", ""), ("Query Expansion · Multi-query<br><small>질문 1개 → N개</small>", ""), ("HyDE<br><small>가상 답변 문서 · 조합 시 마지막</small>", "")], "Query Transformation · 택일 또는 조합", "pre"),
              a(), grp("Retrieval", [("Query Construction<br><small>Text-to-SQL → RDBMS</small>", "k"), ("Vector Retrieval", "")], "질문에 따라 분기", "blk"),
              a(), grp("Post-Retrieval", ["Reranking"], "", "post"), a(), n("Generate"), a(), n("Response", cls="k"), cls="av")
    return f'<div class="x3na">{naive}{adv}</div>'


# ── 5. GraphRAG ──────────────────────────────────────

def _edge(lbl, ev=""):
    e = f"<em>{ev}</em>" if ev else ""
    return f'<div class="x3edge"><span>{lbl}</span><i></i>{e}</div>'


def _gn(t, s, cls=""):
    return f'<div class="x3gn {cls}"><b>{t}</b><span>{s}</span></div>'


def graph_index():
    docs = ('<div class="x3docs">'
            '<div class="x3doc s"><div class="x3dk">문서 D1 · p.2 · 청크 C12</div><p>「설비 EQ-A는 공정 PR-1에 사용된다.」</p></div>'
            '<div class="x3doc s"><div class="x3dk">문서 D2 · p.4 · 청크 C41</div><p>「공정 PR-1로 제품 P-7을 생산한다.」</p></div></div>')
    g = (f'<div class="x3graph">{_gn("설비 EQ-A", "노드: 설비")}{_edge("사용된다", "근거 C12")}'
         f'{_gn("공정 PR-1", "노드: 공정")}{_edge("생산한다", "근거 C41")}{_gn("제품 P-7", "노드: 제품")}</div>')
    return (f'<div class="x3gi">{docs}<div class="x3a">→<small>대상 · 관계 · 근거 추출</small></div>{g}</div>'
            '<div class="x3store"><div class="x3sh">관계 한 건에 함께 저장할 정보</div><div class="x3two">'
            '<span class="x3chip">시작 노드 · 관계 종류 · 끝 노드 · 조건/버전</span>'
            '<span class="x3chip r">근거 청크 ID · 문서명 · 페이지 · 원문 구절</span></div></div>')


def graph_path():
    g = (f'<div class="x3graph">{_gn("EQ-A", "시작 노드", "on")}{_edge("사용된다", "1 hop")}'
         f'{_gn("PR-1", "공정")}{_edge("생산한다", "2 hop")}{_gn("P-7", "제품", "on")}</div>')
    return ('<div class="x3q big">질문: 「EQ-A와 연결된 제품은 무엇인가요?」</div>' + g
            + row(n("근거 원문 모으기", "C12: EQ-A → PR-1<br>C41: PR-1 → P-7", icon="doc"), a(),
                  n("LLM에 전달", "원래 질문 + 관계 경로 + 근거 원문", "r", icon="model"), a(),
                  n("답변과 출처", "시작 노드 · 실제 탐색 경로 · 관계별 원문 · 연결되지 않은 정보", "k"), cls="mt"))


def kg_intro():
    """문장 하나 → 세 묶음(트리플) → 그래프. 설명용 예시."""
    sent = ('소프트 에러는 <mark>알파 입자</mark>나 <mark>중성자</mark>가 <mark>RAM</mark> 셀의 값을 뒤집는 현상이다.')
    trip = [("알파 입자", "일으킨다", "소프트 에러"), ("중성자", "일으킨다", "소프트 에러"), ("소프트 에러", "발생 위치", "RAM")]
    rows = "".join(f'<div class="kg-tr"><b>{a}</b><i>— {r} →</i><b>{c}</b></div>' for a, r, c in trip)
    R, K, M = "#E8002D", "#26262B", "#55555C"
    nodes = {"알파 입자": (60, 40), "중성자": (60, 150), "소프트 에러": (200, 95), "RAM": (330, 95)}

    def nd(n):
        x, y = nodes[n]
        w = sum(9 if ch.isascii() else 15 for ch in n) + 24
        fill = R if n == "소프트 에러" else "#fff"
        tc = "#fff" if n == "소프트 에러" else K
        return (f'<rect x="{x - w / 2}" y="{y - 17}" width="{w}" height="34" rx="17" fill="{fill}" stroke="{R if n == "소프트 에러" else K}" stroke-width="2"/>'
                f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="{tc}">{n}</text>')
    svg = (f'<svg viewBox="0 0 380 190" class="kg-svg"><defs><marker id="kgm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           f'<path d="M0 0 L10 5 L0 10 Z" fill="{M}"/></marker></defs>'
           f'<line x1="104" y1="50" x2="150" y2="80" stroke="{M}" stroke-width="2" marker-end="url(#kgm)"/>'
           f'<line x1="95" y1="140" x2="150" y2="110" stroke="{M}" stroke-width="2" marker-end="url(#kgm)"/>'
           f'<line x1="250" y1="95" x2="306" y2="95" stroke="{M}" stroke-width="2" marker-end="url(#kgm)"/>'
           f'<text x="140" y="52" font-size="12" fill="{M}" font-weight="700">일으킨다</text>'
           f'<text x="128" y="148" font-size="12" fill="{M}" font-weight="700">일으킨다</text>'
           f'<text x="278" y="84" text-anchor="middle" font-size="12" fill="{M}" font-weight="700">발생 위치</text>'
           + "".join(nd(n) for n in nodes) + "</svg>")
    return (f'<div class="kg-in">'
            f'<div class="kg-col"><div class="kg-h">① 문장 · 청크 1 · p.3</div><div class="kg-sent">{sent}</div></div>'
            f'<div class="kg-arr">→</div>'
            f'<div class="kg-col"><div class="kg-h">② 세 묶음 (대상, 관계, 대상)</div>{rows}</div>'
            f'<div class="kg-arr">→</div>'
            f'<div class="kg-col"><div class="kg-h">③ 지식 그래프</div>{svg}</div></div>'
            f'<div class="kg-def"><span><b>노드</b>대상 · 부품 · 현상 · 방법</span><span><b>연결</b>관계 · 방향이 있음</span>'
            f'<span><b>같은 대상</b>문서 여러 곳에 나와도 노드 하나</span><span><b>근거</b>연결마다 청크 ID · 페이지</span></div>')
