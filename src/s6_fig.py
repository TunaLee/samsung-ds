"""6교시 도식: 멀티에이전트 연결 방식 · 운영 방식 · Decisions 판정과 조사 흐름 (원본 그림을 덱 스타일로 다시 그림)."""
from fig import ic, window

R, K, G, M, S = "#E8002D", "#26262B", "#DCDCE1", "#6B6B73", "#F5F5F7"


def _mk(p):
    def m(i, c):
        return (f'<marker id="{p}{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{c}"/></marker>')
    return f'<defs>{m("k", K)}{m("r", R)}{m("g", M)}</defs>'


def _b(x, y, w, h, t, s="", k="ag", small=""):
    """k: io(회색 입출력) · ag(흰 Agent) · hl(빨강 강조) · tl(도구)"""
    fill, st, sw, tc = {"io": (S, K, 2, K), "ag": ("#fff", K, 2.5, K), "hl": ("#FFF5F7", R, 3, R),
                        "tl": ("#fff", "#9A9AA2", 2, K)}[k]
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>'
    cx = x + w / 2
    if small:
        o += f'<text x="{cx}" y="{y + 26}" text-anchor="middle" class="sk">{small}</text>'
    ty = y + h / 2 + (-6 if s else 7) + (8 if small else 0)
    o += f'<text x="{cx}" y="{ty}" text-anchor="middle" class="st" fill="{tc}">{t}</text>'
    if s:
        o += f'<text x="{cx}" y="{ty + 26}" text-anchor="middle" class="ss">{s}</text>'
    return o


def _l(p, pts, c="k", head="end", dash=""):
    col = {"k": K, "r": R, "g": M}[c]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ms = ""
    if head in ("end", "both"):
        ms += f' marker-end="url(#{p}{c})"'
    if head in ("start", "both"):
        ms += f' marker-start="url(#{p}{c})"'
    pts = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"{d}{ms}/>'


def _t(x, y, s, cls="sl", anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{s}</text>'


def _grp(x, y, w, h, label="", red=False):
    st = R if red else "#B4B4BB"
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{"#FFFBFC" if red else "#FAFAFB"}" stroke="{st}" stroke-width="1.6" stroke-dasharray="7 6"/>'
    if label:
        o += _t(x + 20, y + 30, label, "sg", "start")
    return o


def _svg(body, vb, cls=""):
    return f'<svg viewBox="0 0 {vb}" class="s6svg {cls}">{body}</svg>'


def sequential():
    p = "sq"
    o = _mk(p)
    o += _b(10, 50, 160, 100, "사용자 요청", k="io")
    xs = [(250, "Agent 1", "요청 분석"), (500, "Agent 2", "자료 검색"), (750, "Agent 3", "답변 작성")]
    o += _l(p, [(170, 100), (246, 100)])
    for i, (x, t, s) in enumerate(xs):
        o += _b(x, 50, 200, 100, t, s, "hl" if i == 1 else "ag")
        o += _l(p, [(x + 200, 100), (x + 246, 100)], "r" if i < 2 else "k")
        if i < 2:
            o += _t(x + 223, 88, "결과", "sl")
    o += _b(1000, 50, 160, 100, "응답", k="io")
    o += _grp(10, 200, 1150, 90)
    o += _t(585, 238, "앞 단계의 결과 = 다음 단계의 입력", "sb")
    o += _t(585, 268, "앞 단계가 끝나야 다음 단계 시작 · 순서 변경 · 동시 실행 불가", "ss")
    return _svg(o, "1170 300")


def aggregator():
    p = "ag"
    o = _mk(p)
    o += _b(10, 180, 160, 90, "사용자 요청", k="io")
    o += _grp(270, 10, 300, 430, "동시에 실행")
    ys = [60, 185, 310]
    for i, y in enumerate(ys):
        o += _b(300, y, 240, 90, f"Agent {'ABC'[i]}", f"주제 {i + 1} 조사")
        o += _l(p, [(170, 225), (230, 225), (230, y + 45), (296, y + 45)])
        o += _l(p, [(540, y + 45), (610, y + 45), (610, 225), (676, 225)], "r")
    o += _b(680, 170, 230, 110, "집계 Agent", "결과 통합", "hl")
    o += _l(p, [(910, 225), (986, 225)])
    o += _b(990, 180, 170, 90, "결과", k="io")
    o += _grp(680, 330, 480, 100)
    o += _t(920, 370, "서로 독립적인 일만 나누기", "sb")
    o += _t(920, 402, "다른 Agent의 결과를 모른 채 · 마지막에 하나로", "ss")
    return _svg(o, "1170 450")


def hierarchical():
    p = "hi"
    o = _mk(p)
    o += _b(10, 150, 160, 80, "사용자 입력", k="io")
    o += _b(10, 260, 160, 80, "응답", k="io")
    o += _b(250, 130, 250, 230, "상위 Agent", "작업 분해 · 위임", "hl", small="Supervisor")
    o += _l(p, [(170, 190), (246, 190)])
    o += _l(p, [(250, 300), (174, 300)])
    subs = [(30, "하위 Agent A", "문서 조사", "벡터 검색", "사내 문서"), (195, "하위 Agent B", "웹 조사", "웹 검색", "외부 자료"),
            (360, "하위 Agent C", "보고서 작성", "파일 쓰기", "report.md")]
    for y, t, s, tt, ts in subs:
        o += _l(p, [(504, 245), (580, 245), (580, y + 45), (636, y + 45)], "r", head="end")
        o += _b(640, y, 230, 90, t, s)
        o += _l(p, [(874, y + 45), (946, y + 45)], "g", head="both")
        o += _b(950, y + 5, 210, 80, tt, ts, "tl")
    o += _l(p, [(580, 245), (508, 245)], "r")
    return _svg(o, "1170 460")


def shared_tools():
    p = "sh"
    o = _mk(p)
    o += _b(10, 140, 160, 80, "사용자 입력", k="io")
    o += _b(10, 250, 160, 80, "응답", k="io")
    o += _b(250, 120, 240, 230, "상위 Agent", "작업 분해 · 위임", "ag")
    o += _l(p, [(170, 180), (246, 180)])
    o += _l(p, [(250, 290), (174, 290)])
    for y, s in [(60, "기술 문서 조사"), (300, "시장 동향 조사")]:
        o += _l(p, [(494, 235), (560, 235), (560, y + 45), (616, y + 45)])
        o += _b(620, y, 220, 90, f"Agent {'A' if y == 60 else 'B'}", s)
        o += _l(p, [(840, y + 45), (900, y + 45)], "r", head="none")
    o += _l(p, [(560, 235), (498, 235)])
    o += _l(p, [(900, 105), (900, 345)], "r", head="none")
    o += _grp(940, 10, 225, 440, "MCP 서버", red=True)
    for i, t in enumerate(["문서 검색", "웹 검색", "파일 저장"]):
        y = 60 + i * 130
        o += _l(p, [(900, y + 45), (961, y + 45)], "r")
        o += _b(965, y, 180, 90, t, k="tl")
    return _svg(o, "1170 460")


def hitl():
    p = "hl"
    o = _mk(p)
    o += _b(10, 120, 160, 80, "사용자 요청", k="io")
    o += _b(10, 230, 160, 80, "응답", k="io")
    o += _b(250, 100, 230, 230, "Agent", k="ag")
    o += _l(p, [(170, 160), (246, 160)])
    o += _l(p, [(250, 270), (174, 270)])
    o += _l(p, [(484, 215), (560, 215)], head="start")
    o += _l(p, [(560, 215), (560, 70), (896, 70)], "k")
    o += _t(730, 56, "바로 실행 · 되돌릴 수 있는 행동", "sb")
    o += _b(900, 25, 260, 90, "읽기 도구", "검색 · 조회", "tl")
    o += _l(p, [(560, 215), (560, 330), (606, 330)], "r")
    o += _b(610, 285, 230, 90, "사람 승인", "허용 / 거부", "hl")
    o += _l(p, [(840, 330), (896, 330)], "r")
    o += _t(868, 316, "승인 후", "sl")
    o += _b(900, 285, 260, 90, "쓰기 도구", "삭제 · 전송 · 수정", "tl")
    o += _t(1030, 405, "되돌릴 수 없는 행동", "sl")
    return _svg(o, "1170 420")


def decision_flow():
    p = "df"
    o = _mk(p)
    o += _grp(10, 10, 1150, 200, "앱이 정하는 부분 · 언제 판정하고 언제 조사를 부를지")
    top = [(30, 250, "모의 생산라인", "이벤트를 차례로 재생", "ag"), (320, 250, "[decisions] 탭", "새 이벤트 확인", "ag"),
           (610, 250, "Decisions 판정", "조사 필요 조건의 추정 확률", "hl"), (900, 240, "확률 ≥ 기준값?", "기본값 0.5", "ag")]
    for i, (x, w, t, s, k) in enumerate(top):
        o += _b(x, 70, w, 110, t, s, k)
        if i < 3:
            o += _l(p, [(x + w, 125), (top[i + 1][0] - 4, 125)])
    o += _l(p, [(1020, 180), (1020, 255), (600, 255), (600, 318)], "r")
    o += _t(810, 245, "넘을 때마다 · 판정 입력과 함께", "sl")
    o += _grp(10, 280, 1150, 250, "Agent가 판단하는 부분 · 어떤 도구로 무엇을 조회할지", red=True)
    o += _b(470, 322, 260, 110, "조사 Agent", "원인 가설 · 근거 · 추가 확인", "hl")
    o += _b(60, 330, 260, 80, "Lot 이력", "도구로 조회", "tl")
    o += _b(60, 430, 260, 80, "정비 기록", "도구로 조회", "tl")
    o += _l(p, [(466, 360), (324, 370)], "g", head="both")
    o += _l(p, [(466, 400), (324, 465)], "g", head="both")
    o += _l(p, [(730, 377), (836, 377)])
    o += _b(840, 330, 300, 95, "이벤트 행 아래", "조사 결과 표시", "ag")
    return _svg(o, "1170 540")


def cost():
    """N회 판정 + M회 조사."""
    hit = {2, 6, 9}
    ev = "".join(f'<i class="{"on" if i in hit else ""}"></i>' for i in range(12))
    dec = "".join(f'<i class="{"on" if i in hit else ""}">{ic("check") if i not in hit else ic("search")}</i>' for i in range(12))
    inv = "".join(f'<i class="on">{ic("tool")}</i>' for _ in hit)
    return ('<div class="cost">'
            f'<div class="cr"><div class="cl"><b>이벤트</b><span>전체 N개</span></div><div class="cc">{ev}</div></div>'
            f'<div class="cr"><div class="cl"><b>Decisions 판정</b><span>N회 · 이벤트마다</span></div><div class="cc dec">{dec}</div></div>'
            f'<div class="cr"><div class="cl r"><b>조사 Agent</b><span>M회 · 기준값 이상만</span></div><div class="cc inv">{inv}</div></div>'
            '<div class="cf">비용 구조 = <b>N회 판정</b> + <b class="r">M회 조사</b></div></div>')


def lanes():
    """이벤트 조회와 Decisions 처리는 따로 동작."""
    def lane(icon, t, items, cls=""):
        li = "".join(f"<span>{x}</span>" for x in items)
        return f'<div class="ln {cls}"><div class="lh">{ic(icon)}<b>{t}</b></div><div class="lb">{li}</div></div>'
    return ('<div class="lns">'
            + lane("search", "이벤트 조회 · 브라우저", ["2초마다 /api/events", "since · run_id로 새 이벤트만", "같은 seq 중복 판정 없음", "순서대로 대기열에"])
            + '<div class="lq">대기열<br><small>seq 순서</small></div>'
            + lane("model", "Decisions 처리 · 서버", ["동시에 1건만", "호출 시작 간격 최소 3초", "자동 · 수동 호출 합산", "실패는 실패 상태로 표시"], "r")
            + "</div>")


def wire():
    """[decisions] 탭 최소 화면 (요청문 5 · 6 의 구성)."""
    rows = "".join(f'<tr><td>{s}</td><td>{e}</td><td class="m">이벤트 내용</td><td class="m">probability</td><td class="m">판정 상태</td></tr>'
                   for s, e in [("1", "EQ-A"), ("2", "EQ-A"), ("3", "EQ-B")])
    body = ('<div class="wf">'
            '<div class="wt"><span class="btn">감시 시작</span><span class="m">경과 시간 · 감시 상태</span></div>'
            '<table class="wtab"><thead><tr><th>seq</th><th>장비</th><th>이벤트 내용</th><th>조사 필요 확률</th><th>판정 상태</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>'
            '<div class="wd"><div><b>생산라인 API</b><span>Request · Response</span></div>'
            '<div><b>Decisions API</b><span>Request · Response · 복사</span></div>'
            '<div class="r"><b>Decisions 테스트</b><span>input 편집 · 1회 호출</span></div></div></div>')
    return window("agent-sim · [decisions] 탭 구성", body, "wfw")
