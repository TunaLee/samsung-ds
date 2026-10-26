"""1교시 도입 · AI 에이전트란 — 나오게 된 계기 · 작업 길이 · 구성 (koreanre-ai trend.py 를 이 과정 예시로)."""
import fig
from kit import cards, note, page, pane, section, two, ul

TREND = [  # (시기, 제목, 설명, 강조)
    ("2022.11", "채팅", "ChatGPT 공개 · 묻고 답하기", False),
    ("2023.06", "도구 호출", "모델이 함수를 골라 호출 · Function Calling", True),
    ("2024.11", "연결 표준 MCP", "AI와 외부 시스템을 잇는 공통 규격", False),
    ("2025.02", "코딩 에이전트", "Claude Code · 5월 Codex · 터미널에서 직접 작업", True),
    ("2025.07", "범용 에이전트", "ChatGPT agent · 웹 · 파일 · 코드를 이어서 실행", False),
    ("2025.10", "스킬", "업무 지침을 저장해 꺼내 쓰는 Agent Skills", False),
]

# METR Time Horizon 1.1 — 당시 최고 성능 모델 · (출시일, 50% 길이 분, 80% 길이 분, 이름표) · posco-dx hx.py 와 같은 값
METR_SOTA = [
    ("2023-03-14", 4.0, 0.9, "GPT-4"), ("2024-05-13", 7.0, 1.3, ""), ("2024-06-20", 11.4, 1.7, ""),
    ("2024-09-12", 20.3, 4.4, ""), ("2024-12-05", 38.8, 7.1, "o1"), ("2025-02-24", 60.4, 12.1, ""),
    ("2025-04-16", 119.7, 30.0, "o3"), ("2025-08-07", 203.0, 38.3, "GPT-5"), ("2025-11-18", 224.3, 54.1, ""),
    ("2025-11-24", 293.0, 49.4, ""), ("2025-12-11", 352.2, 66.0, ""), ("2026-02-05", 718.8, 69.9, "Claude Opus 4.6"),
    ("2026-04-07", 1044.8, 185.9, "Mythos Preview"),
]


def metr_chart():
    import math
    from datetime import date
    R, K, M = "#E8002D", "#26262B", "#8A8A92"
    W, H, X0, X1, Y0, Y1 = 760, 380, 70, 740, 340, 20
    t0, t1 = date(2023, 1, 1).toordinal(), date(2026, 7, 1).toordinal()
    lo, hi = math.log2(0.5), math.log2(32 * 60)
    X = lambda d: X0 + (X1 - X0) * (date.fromisoformat(d).toordinal() - t0) / (t1 - t0)
    Y = lambda m: Y0 - (Y0 - Y1) * (math.log2(m) - lo) / (hi - lo)
    g = ""
    for m, lab in ((1, "1분"), (4, "4분"), (15, "15분"), (60, "1시간"), (240, "4시간"), (960, "16시간")):
        g += (f'<line x1="{X0}" x2="{X1}" y1="{Y(m):.1f}" y2="{Y(m):.1f}" stroke="#EFEFF2" stroke-width="1.5"/>'
              f'<text x="{X0 - 8}" y="{Y(m) + 4:.1f}" text-anchor="end" font-size="13" fill="{M}">{lab}</text>')
    for yr in (2023, 2024, 2025, 2026):
        g += f'<text x="{X(f"{yr}-01-01"):.1f}" y="{Y0 + 22}" text-anchor="middle" font-size="13" fill="{M}">{yr}</text>'
    band = " ".join(f"{X(d):.1f},{Y(a):.1f}" for d, a, b, _ in METR_SOTA) + " " + \
        " ".join(f"{X(d):.1f},{Y(b):.1f}" for d, a, b, _ in reversed(METR_SOTA))
    g += f'<polygon points="{band}" fill="{R}" fill-opacity=".08"/>'
    for idx, col in ((1, R), (2, K)):
        pts = " L".join(f"{X(r[0]):.1f} {Y(r[idx]):.1f}" for r in METR_SOTA)
        g += f'<path d="M{pts}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" class="mtline"/>'
        for r in METR_SOTA:
            g += f'<circle cx="{X(r[0]):.1f}" cy="{Y(r[idx]):.1f}" r="4.5" fill="{col}"/>'
    for d, a, b, lab in METR_SOTA:
        if lab:
            ty = Y(b) - 16 if lab == "Claude Opus 4.6" else Y(a) - 10
            g += f'<text x="{X(d) - 8:.1f}" y="{ty:.1f}" text-anchor="end" font-size="12.5" font-weight="700" fill="{K}">{lab}</text>'
    g += (f'<line x1="{X0}" x2="{X1}" y1="{Y(960):.1f}" y2="{Y(960):.1f}" stroke="{R}" stroke-dasharray="5 5" stroke-width="1.5"/>'
          f'<text x="{X0 + 6}" y="{Y(960) - 6:.1f}" font-size="12" fill="{R}">16시간 넘는 측정은 신뢰 낮음</text>')
    lx, ly = X0 + 420, Y0 - 56
    g += (f'<rect x="{lx}" y="{ly - 10}" width="14" height="4" fill="{R}"/><text x="{lx + 20}" y="{ly - 4}" font-size="13" fill="{K}" font-weight="700">절반(50%) 성공하는 작업 길이</text>'
          f'<rect x="{lx}" y="{ly + 10}" width="14" height="4" fill="{K}"/><text x="{lx + 20}" y="{ly + 16}" font-size="13" fill="{K}" font-weight="700">80% 성공하는 작업 길이</text>'
          f'<text x="{lx + 20}" y="{ly + 36}" font-size="12.5" fill="{R}">가운데 띠 = 믿고 맡기기까지의 차이</text>')
    return f'<svg class="mtchart" viewBox="0 0 {W} {H}">{g}</svg>'


def two_modes():
    def col(cls, title, when, ask, steps, me, res):
        li = "".join(f"<li>{x}</li>" for x in steps)
        return (f'<div class="md {cls}"><div class="md-h"><b>{title}</b><span>{when}</span></div><div class="md-q">{ask}</div>'
                f'<div class="md-k">AI</div><ul>{li}</ul><div class="md-k">사람</div><p>{me}</p><div class="md-r">{res}</div></div>')
    a = col("", "대화형", "묻고 답하기", "「박리 시험 조건 알려 줘」",
            ["학습한 범위에서 글로 답함", "사내 규격 문서는 본 적 없음 · 출처 없음"], "문서 찾기 · 대조 · 표 정리를 직접", "그럴듯한 답 한 덩어리")
    b = col("on", "위임형 · 에이전트", "목표를 맡기기", "「사내 규격 문서에서 박리 시험 조건을 찾아 출처 달린 표로」",
            ["문서 검색을 여러 번 · 원문 확인", "조건 · 수치를 표로 정리", "부족하면 다른 말로 다시 검색"], "목표를 정하고 결과를 확인", "출처 달린 결과물")
    return page("대화형과 위임형", f'<div class="mds">{a}<div class="md-a">→</div>{b}</div>'
                + note("바뀐 것", "AI가 <b>답</b>을 주는 데서 → <b>일을 맡아 끝까지</b> 하는 데로 · 사람 역할은 목표 · 확인", "red"), kick="AI 에이전트란")


def why_now():
    return page("에이전트 등장 배경", cards([
        ("도구 호출", "2023.06 Function Calling · 모델이 <b>어떤 함수를 어떤 값으로</b> 부를지 고름 → 검색 · 계산 · 실행을 앱이 대신", "01"),
        ("긴 작업", "맡길 수 있는 작업 길이가 <b>약 105일마다 2배</b> · 몇 분 → 몇 시간짜리 일", "02"),
        ("연결 표준", "2024.11 MCP · 사내 시스템 · 문서 저장소를 <b>같은 방식</b>으로 연결", "03"),
    ]) + note("정리", "고를 수 있게 됨(도구 호출) + 오래 이어 갈 수 있게 됨(작업 길이) + 붙이기 쉬워짐(MCP) → 에이전트", "red"), kick="AI 에이전트란")


def tool_use():
    tools = [("search", "문서 검색 · RAG"), ("folder", "파일 읽기 · 쓰기"), ("chart", "코드 실행 · 계산"), ("mail", "메일 · 메모"), ("plug", "사내 시스템 · MCP")]
    chips = "".join(f'<div class="tu-t">{fig.ic(i)}<span>{t}</span></div>' for i, t in tools)
    loop = ('<div class="tu-l">'
            '<div class="tu-s"><b>① 판단</b><span>지금 무엇이 필요한가</span></div><i>→</i>'
            '<div class="tu-s on"><b>② 도구 호출</b><span>검색 · 파일 · 계산 · 연결된 시스템</span></div><i>→</i>'
            '<div class="tu-s"><b>③ 결과 확인</b><span>충분한가 · 맞는가</span></div><i>→</i>'
            '<div class="tu-s"><b>④ 다음 행동</b><span>다시 호출 또는 끝내기</span></div></div>')
    return page("도구 사용", two(
        pane("도구 없는 AI", ul(["다음 글자를 확률로 이어 쓰기만", "계산 · 최신 정보 · 사내 문서 · 실행 불가", "결과를 사람이 옮겨서 실행"]), "bad"),
        pane("도구를 쓰는 AI", ul(["필요할 때 도구를 <b>스스로</b> 골라 호출", "도구 결과를 읽고 다음 행동 결정", "여러 단계를 이어서 끝까지"]), "good"))
        + f'<div class="tu-ts">{chips}</div>', kick="AI 에이전트란")


def horizon():
    cards_ = ('<div class="mtcards">'
              '<div class="mtc hl"><b>105<small>일</small></b><span>작업 길이가 2배 되는 기간 (2024년 이후)</span></div>'
              '<div class="mtc"><b>약 2<small>년</small></b><span>무어의 법칙 · 칩 성능 2배 주기</span></div>'
              '<div class="mtc"><b>5.7<small>시간</small> → 54<small>분</small></b><span>GPT-5.4 · 50% 기준 vs 80% 기준</span></div></div>')
    return page("AI 작업 길이 · 105일마다 2배", f'<div class="mtwrap">{metr_chart()}{cards_}</div>'
                + note("읽는 법", "작업 길이 = 사람이 하면 걸리는 시간 · 출처 METR Time Horizons (2026.5)"),
                kick="AI 에이전트란")


def course_map():
    rows = [("모델 · Context", "1교시 · 무엇을 얼마나 넣을지"), ("자료 · RAG", "2~3교시 · 근거를 찾아 넣기"),
            ("도구 · MCP", "4~5교시 · 고르고 실행하기"), ("여러 에이전트", "6교시 · 판정과 조사 나누기")]
    out = "".join(f'<div class="bgp on"><b>{n}</b><span>{d}</span></div>' for n, d in rows)
    return page("과정 구성", f'<div class="bgps">{out}</div>'
                + note("이어서", "에이전트를 이루는 네 가지를 한 교시씩 · 7~8교시 캡스톤에서 하나로", "red"), kick="AI 에이전트란")


def intro():
    return [
        section("01", "AI 에이전트란", "왜 나왔고 · 무엇으로 이루어지고 · 얼마나 맡길 수 있나"),
        two_modes(),
        why_now(),
        tool_use(),
        horizon(),
        page("에이전트 구성 요소", fig.agent_parts()
             + note("핵심", "모델은 엔진 · 나머지 셋은 장비 · <b>같은 모델도 장비에 따라 결과가 달라짐</b>", "red"), kick="AI 에이전트란"),
        page("채팅 → 에이전트 연표", fig.timeline(TREND)
             + note("출처", "OpenAI (2023.06 · 2025.05 · 2025.07) · Anthropic (2024.11 · 2025.02 · 2025.10)"), kick="AI 에이전트란"),
        course_map(),
    ]
