"""4교시 도해 (원본 교안 그림 04.svg · 05.svg 등을 이 덱 스타일로 다시 그림)."""
from fig import ICONS, ic

R, K, G, M, W = "#E8002D", "#26262B", "#DCDCE1", "#6B6B73", "#FFFFFF"


def _sic(name, x, y, s=1.0, color=K):
    """SVG 안에 선 아이콘 넣기 (24×24 기준)."""
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{color}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def seq(pid, actors, msgs, h=None, w=1160, top=96, gap=62):
    """순서도: actors = [(아이콘, 이름, 보조, 강조)], msgs = [(번호, 시작, 끝, 제목, 보조, 종류)].
    종류: 'go'(검정 실선) · 'back'(빨강 실선) · 'self'(같은 칸 안의 실행)."""
    n = len(actors)
    xs = [w * (i + .5) / n for i in range(n)]
    H = h or top + 40 + gap * len(msgs) + 10
    s = [f'<svg viewBox="0 0 {w} {H}" class="s4seq">',
         f'<defs><marker id="{pid}k" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 Z" fill="{K}"/></marker>'
         f'<marker id="{pid}r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 Z" fill="{R}"/></marker></defs>']
    for (icon, name, sub, hl), x in zip(actors, xs):
        fill, tc = (K, W) if hl else (W, K)
        s.append(f'<line x1="{x}" y1="{top - 10}" x2="{x}" y2="{H - 6}" stroke="{G}" stroke-width="3" stroke-dasharray="6 6"/>')
        s.append(f'<rect x="{x - 105}" y="6" width="210" height="{top - 22}" rx="14" fill="{fill}" stroke="{K}" stroke-width="2.5"/>')
        s.append(_sic(icon, x - 92, 22, 1.5, W if hl else R))
        s.append(f'<text x="{x - 48}" y="{38 if sub else 47}" class="sa" fill="{tc}">{name}</text>')
        if sub:
            s.append(f'<text x="{x - 48}" y="62" class="sb" fill="{"#C9C9CF" if hl else M}">{sub}</text>')
    for i, (no, a, b, t, sub, kind) in enumerate(msgs):
        y = top + 34 + gap * i
        xa, xb = xs[a], xs[b]
        col, mk = (R, f"{pid}r") if kind == "back" else (K, f"{pid}k")
        if kind == "self":
            s.append(f'<rect x="{xa - 95}" y="{y - 20}" width="190" height="40" rx="10" fill="#FFF0F3" stroke="{R}" stroke-width="2.5"/>'
                     f'<text x="{xa}" y="{y + 6}" text-anchor="middle" class="sm" fill="{R}">{t}</text>')
            if sub:
                s.append(f'<text x="{xa + 108}" y="{y + 6}" class="sb" fill="{M}">{sub}</text>')
            lx = xa - 118
        else:
            d = 1 if xb > xa else -1
            s.append(f'<line x1="{xa + 8 * d}" y1="{y}" x2="{xb - 10 * d}" y2="{y}" stroke="{col}" stroke-width="3" marker-end="url(#{mk})"/>')
            mid = (xa + xb) / 2
            s.append(f'<rect x="{mid - len(t) * 9.6 - 10}" y="{y - 30}" width="{len(t) * 19.2 + 20}" height="26" fill="{W}"/>'
                     f'<text x="{mid}" y="{y - 10}" text-anchor="middle" class="sm" fill="{col}">{t}</text>')
            if sub:
                s.append(f'<text x="{mid}" y="{y + 22}" text-anchor="middle" class="sb" fill="{M}">{sub}</text>')
            lx = min(xa, xb) - 30
        if no:
            s.append(f'<circle cx="{lx}" cy="{y}" r="15" fill="{R if kind == "back" else K}"/>'
                     f'<text x="{lx}" y="{y + 6}" text-anchor="middle" class="sn">{no}</text>')
    s.append("</svg>")
    return "".join(s)


def search_flow():
    """LLM은 검색어를 정하고, 앱이 검색 엔진에 요청."""
    return seq("sf", [("chat", "사용자", "질문", False), ("model", "LLM", "판단 · 작성", True),
                      ("plug", "앱", "LLM을 감싼 프로그램", False), ("search", "검색 엔진", "검색 도구", False)],
               [("1", 0, 1, "오늘 아침 뉴스", "", "go"),
                ("2", 1, 2, "검색 요청 · 검색어", "「검색이 필요하다」 판단", "go"),
                ("3", 2, 3, "검색 실행", "", "go"),
                ("4", 3, 2, "검색 결과", "", "back"),
                ("5", 2, 1, "검색 결과 전달", "", "back"),
                ("6", 1, 0, "결과를 읽고 쓴 답변", "", "back")], gap=56)


def decide_run():
    """[그림 1] 다시 그림 — 무엇을 부를지는 LLM, 실제 실행은 앱."""
    return seq("dr", [("chat", "질문", "회의 메모 좀 찾아줘", False), ("model", "LLM", "설명문을 읽고 판단", True),
                      ("plug", "앱", "도구를 실제로 실행", False)],
               [("1", 0, 1, "질문", "", "go"),
                ("2", 1, 2, "도구 이름 · 인자", "결정 · 아직 실행 전", "go"),
                ("", 2, 2, "도구 실행", "실행 · 파일 읽기 · 쓰기", "self"),
                ("3", 2, 1, "반환값", "", "back"),
                ("4", 1, 0, "돌아온 값으로 답변", "결정", "back")], gap=62)


def save_trip():
    """[그림 2] 다시 그림 — 메모 저장 요청 한 번의 왕복 (①~⑤)."""
    rows = [("1", "앱 → LLM", "사용자 요청 · 역할 지시문 · 도구 선언을 OpenAI API로", "메모 저장 함수의 코드는 보내지 않음", False),
            ("2", "LLM → 앱", "<code>memo_tool_2</code>를 어떤 <code>text</code>로 부를지 구조화된 응답", "사람이 읽는 답변과 다른 실행 요청 · 아직 저장 전", True),
            ("3", "앱 → 함수", "이름에 연결된 <code>note_save</code>를 찾아 인자 전달 · 실행", "파일을 수정하는 주체는 앱의 Python 코드", False),
            ("4", "앱 → LLM", "실행 결과를 <code>function_call_output</code>으로 다음 입력에", "<code>call_id</code>로 어느 호출의 결과인지 연결", False),
            ("5", "LLM → 앱 → 화면", "결과를 읽고 최종 답변 또는 다음 호출", "앱이 최종 답변을 화면에 표시", True)]
    out = "".join(f'<div class="tp-r{" llm" if l else ""}{" rep" if n in "234" else ""}"><span class="tp-n">{n}</span><span class="tp-d">{d}</span>'
                  f'<b>{t}</b><em>{e}</em></div>' for n, d, t, e, l in rows)
    return f'<div class="tp">{out}<div class="tp-loop">도구를 여러 번 쓰면<br><b>②~④ 반복</b></div></div>'


def autonomy():
    """고정 코드 → 에이전트: 다음 단계를 누가 정하는가."""
    rows = [("고정 코드", "코드", "환율을 받아 금액을 곱하는 계산기"),
            ("LLM 한 번 호출", "코드 · LLM은 한 번 응답", "문서 한 편 요약"),
            ("워크플로우", "코드가 정한 순서 안에서 LLM", "rag-sim · 검색 → 생성"),
            ("에이전트", "LLM이 도구와 다음 행동 선택", "Claude Code · agent-sim")]
    cells = "".join(f'<div class="au{" on" if i == 3 else ""}"><div class="au-dot"></div><b>{t}</b>'
                    f'<span class="au-k">다음 단계</span><em>{w}</em><span class="au-ex">{e}</span></div>'
                    for i, (t, w, e) in enumerate(rows))
    return (f'<div class="aus"><div class="au-axis"><span>코드가 정함</span><i></i><span class="r">LLM이 정함 · 자율성</span></div>'
            f'<div class="au-row">{cells}</div></div>')


def decl_split():
    """도구 선언은 LLM에, 실행 함수는 앱에 — 등록 정보가 둘을 연결."""
    return ('<div class="ds">'
            f'<div class="ds-c llm"><div class="ds-h">{ic("model")}<b>도구 선언</b><span>LLM에 전달</span></div>'
            '<div class="ds-kv"><i>name</i><code>memo_tool_2</code></div>'
            '<div class="ds-kv"><i>description</i><code>새 메모를 저장한다.</code></div>'
            '<div class="ds-kv"><i>parameters</i><code>text · 문자열</code></div>'
            '<div class="ds-f">호출 여부 · 입력값 판단</div></div>'
            '<div class="ds-a">→</div>'
            f'<div class="ds-c mid"><div class="ds-h">{ic("link")}<b>이름과 함수의 연결</b><span>앱의 등록 정보</span></div>'
            '<div class="ds-map"><code>memo_tool_2</code><i>↓</i><code>note_save</code></div>'
            '<div class="ds-f">반환된 이름으로 실행 함수 조회</div></div>'
            '<div class="ds-a">→</div>'
            f'<div class="ds-c app"><div class="ds-h">{ic("folder")}<b>실행 함수</b><span>내 PC의 앱</span></div>'
            '<div class="ds-code"><code>def note_save(text=""):<br>&nbsp;&nbsp;…메모 파일에 덧붙여 저장</code></div>'
            '<div class="ds-f">LLM에 보내지 않음</div></div>'
            '</div>')


def chains():
    """도구 뒤의 함수가 하는 일은 다양 — 파일 · 외부 API."""
    rows = [(("tool", "메모 저장 도구"), ("plug", "앱의 note_save 함수"), ("folder", "내 PC의 메모 파일")),
            (("tool", "환율 조회 도구"), ("plug", "앱의 환율 조회 함수"), ("globe", "Frankfurter API"))]
    out = ""
    for r in rows:
        cells = '<i>→</i>'.join(f'<span>{ic(a)}<b>{t}</b></span>' for a, t in r)
        out += f'<div class="ch-r">{cells}</div>'
    return (f'<div class="chs"><div class="ch-h"><span>LLM이 고름</span><span>앱이 실행</span><span>실제 작업 대상</span></div>{out}</div>')


def inout():
    ok = [("질문 · 역할 지시문", "전달"), ("도구 이름 · 설명문 · 인자 형식", "전달"),
          ("도구가 반환한 결과 · 오류", "실행 후 다음 요청의 입력에")]
    no = [("note_save의 Python 구현 코드", "도구 등록 과정에서 전달하지 않음"),
          ("메모 파일 전체 · 프로젝트 폴더 전체", "자동 전달 없음 · 도구 결과에 담긴 내용만")]
    a = "".join(f'<div class="io-r"><span class="io-m">✓</span><b>{t}</b><em>{d}</em></div>' for t, d in ok)
    b = "".join(f'<div class="io-r"><span class="io-m x">×</span><b>{t}</b><em>{d}</em></div>' for t, d in no)
    return (f'<div class="io"><div class="io-c on"><div class="io-h">입력 컨텍스트에 올라가는 것</div>{a}</div>'
            f'<div class="io-c"><div class="io-h">올라가지 않는 것</div>{b}</div></div>')


def api_map():
    """OpenAI API 요청의 세 항목."""
    rows = [("instructions", "역할 지시문", "book"), ("input", "사용자 질문 · 도구 실행 결과", "chat"), ("tools", "도구 선언", "tool")]
    li = "".join(f'<div class="am-r">{ic(i)}<code>{k}</code><span>{v}</span></div>' for k, v, i in rows)
    return (f'<div class="am"><div class="am-l">{li}</div><div class="am-arr">→</div>'
            f'<div class="am-m">{ic("model")}<b>LLM</b><span>모두 판단에 쓰는 입력</span><span>모두 입력 토큰 · 컨텍스트 한도에 포함</span></div></div>')


def gauge():
    """[도구] 탭 최상단 Context Window 표시를 단순화한 모형 (수치 없음)."""
    return ('<div class="gw"><div class="gw-h"><b>Context Window</b><span>[도구] 탭 최상단</span></div>'
            '<div class="gw-l">전체 현황 <em>최대 용량 대비 사용량</em></div>'
            '<div class="gw-bar"><i style="width:34%"></i></div>'
            '<div class="gw-l">사용 중 상세 현황 <em>항목별 비중</em></div>'
            '<div class="gw-bar seg"><i class="a" style="width:22%"></i><i class="b" style="width:30%"></i><i class="c" style="width:48%"></i></div>'
            '<div class="gw-lg"><span><i class="a"></i>Instructions</span><span><i class="b"></i>Tools</span><span><i class="c"></i>Context</span>'
            '<span class="tip">마우스를 올리면 수치 · 계산 기준</span></div></div>')


def growth():
    """한 질문 안에서 호출이 이어질수록 다시 보내는 입력이 쌓임 (길이는 설명용)."""
    calls = [("1회차", [("지침", "a", 18), ("도구 정의", "b", 22), ("질문", "q", 8)]),
             ("2회차", [("지침", "a", 18), ("도구 정의", "b", 22), ("질문", "q", 8), ("호출 요청", "f", 8), ("도구 결과", "c", 20)]),
             ("3회차", [("지침", "a", 18), ("도구 정의", "b", 22), ("질문", "q", 8), ("호출 요청", "f", 8), ("도구 결과", "c", 20),
                        ("호출 요청", "f", 8), ("도구 결과", "c", 16)])]
    out = ""
    for name, segs in calls:
        bar = "".join(f'<i class="{c}" style="flex:{v}"><span>{n}</span></i>' for n, c, v in segs)
        tot = sum(v for _, _, v in segs)
        out += f'<div class="gr-r"><b>{name}</b><div class="gr-b" style="width:{tot / 120 * 100:.0f}%">{bar}</div></div>'
    return f'<div class="gr">{out}<div class="gr-n">같은 질문 안 · 호출할 때마다 앞의 항목을 다시 보냄 · 막대 길이는 설명용</div></div>'


def rounds():
    """1회차와 2회차 요청 비교 — 달라지는 것은 input."""
    def col(title, items):
        li = "".join(f'<div class="rd-i{" new" if new else ""}"><code>{k}</code><span>{v}</span></div>' for k, v, new in items)
        return f'<div class="rd-c"><div class="rd-h">{title}</div>{li}</div>'
    a = col("1회차 요청", [("instructions", "역할 지시문", False), ("tools", "도구 3개 선언", False),
                         ("input[0]", "user · 회의 메모 좀 찾아줘", False)])
    b = col("2회차 요청", [("instructions", "같은 값 다시", False), ("tools", "같은 값 다시", False),
                         ("input[0]", "user · 회의 메모 좀 찾아줘", False),
                         ("input[1]", "function_call · memo_tool_1 · call_ab12…", True),
                         ("input[2]", "function_call_output · call_ab12…", True)])
    return (f'<div class="rd">{a}<div class="rd-m"><span>앱이 도구 실행</span><b>→</b><span>결과를 붙여<br>한 번 더</span></div>{b}</div>')


def guard():
    """어디서 막는가 — LLM의 판단 단계와 앱의 실행 단계."""
    return ('<div class="gd">'
            '<div class="gd-z llm"><div class="gd-zh">LLM의 판단</div>'
            '<div class="gd-b">지침의 금지 문구<em>판단에 영향 · 실행은 막지 않음</em></div></div>'
            '<div class="gd-a">호출 요청 →</div>'
            '<div class="gd-z app"><div class="gd-zh">앱의 실행</div>'
            '<div class="gd-b">실행 전 사람 확인<em>확실 · 매번 확인</em></div>'
            '<div class="gd-b">앱 코드의 권한 검사<em>조건이 안 맞으면 실행 안 함</em></div>'
            '<div class="gd-b">도구 미등록<em>호출 경로 자체가 없음</em></div></div>'
            '<div class="gd-a">→ 실행</div>'
            '</div>')


def guide(title, lines, keys, conds):
    """Claude Code 요청문 작성 가이드: 가이드라인 · 키워드 · 실습 조건."""
    li = "".join(f"<li>{x}</li>" for x in lines)
    kw = "".join(f"<span>{k}</span>" for k in keys)
    cd = "".join(f'<div class="pg-cd"><b>{k}</b><span>{v}</span></div>' for k, v in conds)
    return (f'<div class="pg"><div class="pg-l"><div class="pg-tag">Claude Code · Prompt 직접 작성</div>'
            f'<div class="pg-t">{title}</div><ul>{li}</ul><div class="pg-kh">키워드</div><div class="pg-kw">{kw}</div></div>'
            f'<div class="pg-r"><div class="pg-rh">실습 조건 확인</div>{cd}</div></div>')


def blanks(items):
    """기록 칸."""
    out = "".join(f'<div class="bl-r"><span>{q}</span><i></i></div>' for q in items)
    return f'<div class="bl"><div class="bl-h">기록</div>{out}</div>'


def tool_vs_none():
    """도구 없이 vs 계산기 도구가 있을 때."""
    def box(title, rows, cls):
        li = "".join(f'<div class="tv-r"><b>{a}</b><span>{b}</span></div>' for a, b in rows)
        return f'<div class="tv-c {cls}"><div class="tv-h">{title}</div>{li}</div>'
    a = box("도구 없이", [("LLM", "4,817 × 293 = 다음 토큰을 확률로 고름"), ("답", "「1,411,281입니다.」 · 그럴듯하지만 틀릴 수 있음")], "no")
    b = box("계산기 도구가 있으면", [("LLM", "calculator 도구를 (4817 × 293)로 부르기로 결정"), ("앱", "실제로 계산 → 1,411,381"),
                                  ("LLM", "결과를 받아 「1,411,381입니다.」")], "yes")
    return f'<div class="tv">{a}<div class="tv-arr">→</div>{b}</div>'
