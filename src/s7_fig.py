"""7교시 도해 (원본 교안의 흐름 · 그림을 이 덱 스타일로 다시 그림). 클래스는 s7- 로 시작."""
from fig import ic


def chain(items, hl=(), cls=""):
    """짧은 단계 줄. items: 문자열 또는 (제목, 설명)."""
    out = []
    for i, it in enumerate(items):
        t, d = (it, "") if isinstance(it, str) else it
        on = " on" if i in hl else ""
        sub = f"<em>{d}</em>" if d else ""
        out.append(f'<span class="s7-c{on}"><b>{t}</b>{sub}</span>')
    return f'<div class="s7-chain {cls}">' + '<i class="s7-a">→</i>'.join(out) + "</div>"


def vchain(items, hl=()):
    """세로 단계 줄."""
    out = []
    for i, it in enumerate(items):
        t, d = (it, "") if isinstance(it, str) else it
        on = " on" if i in hl else ""
        sub = f"<em>{d}</em>" if d else ""
        out.append(f'<div class="s7-v{on}"><b>{t}</b>{sub}</div>')
    return '<div class="s7-vchain">' + '<i class="s7-va">↓</i>'.join(out) + "</div>"


def agent_io():
    """시험 결과 검토 Agent: 입력 → 할 일 → 결과."""
    cols = [("folder", "입력", ["시험 결과 CSV가 들어 있는 폴더"]),
            ("tool", "Agent가 해야 할 일", ["파일 찾기", "CSV 읽기", "조건별 결과 계산", "누락 항목 확인"]),
            ("report", "결과", ["시험 결과 집계표", "누락 목록"])]
    cells = []
    for i, (icon, h, li) in enumerate(cols):
        hl = " on" if i == 2 else ""
        items = "".join(f"<li>{x}</li>" for x in li)
        cells.append(f'<div class="s7-io{hl}"><div class="s7-ioh">{ic(icon)}<b>{h}</b></div><ul>{items}</ul></div>')
    return '<div class="s7-ios">' + '<i class="s7-a">→</i>'.join(cells) + "</div>"


def decide():
    """도구 결과를 보고 다음 행동을 고른다."""
    opts = [("ok", "충분", "종료", "검토표 완성"),
            ("", "부족", "추가 조회", "다른 자료 찾기"),
            ("", "부족", "조건 변경", "범위 · 조건 바꿔 다시"),
            ("", "부족", "사용자 확인", "필요한 정보 묻기"),
            ("stop", "호출 한도", "중단", "미해결 내용 남기기")]
    li = "".join(f'<div class="s7-opt {k}"><span>{w}</span><b>{t}</b><em>{d}</em></div>' for k, w, t, d in opts)
    return ('<div class="s7-dec">'
            f'<div class="s7-dbox">{ic("tool")}<b>도구 결과</b><em>실제 반환값</em></div><i class="s7-a">→</i>'
            f'<div class="s7-dbox core">{ic("model")}<b>판단</b><em>충분한가</em></div><i class="s7-a">→</i>'
            f'<div class="s7-opts">{li}</div></div>')


def drift():
    """대화가 깊어질수록 구체적인 정보가 섞인다."""
    lines = ["「이 기능을 만들어 줘.」", "「우리 업무에서는 이런 절차를 사용해.」",
             "「실제로는 이 조건에서 이런 문제가 생겨.」", "「내부 문서에는 이렇게 적혀 있는데...」"]
    out = "".join(f'<div class="s7-dr l{i}"><span>{i + 1}</span>{t}</div>' for i, t in enumerate(lines))
    return (f'<div class="s7-drift"><div class="s7-drs">{out}</div>'
            '<div class="s7-drbar"><b>대화가 깊어질수록</b><em>처음에는 입력할 생각이 없던 정보가 섞임</em></div></div>')


def mmrag():
    """멀티모달 RAG 구조: 문서 준비 · 질문 (원본 03.svg 다시 그림)."""
    def node(t, d="", tag="", cls=""):
        tg = f'<i class="tag {cls}">{tag}</i>' if tag else ""
        return f'<div class="s7-n {cls}">{tg}<b>{t}</b><em>{d}</em></div>'
    A = '<div class="s7-ar">→</div>'
    E = '<div></div>'
    r1 = (node("PDF") + A + node("페이지 이미지", "페이지마다 1장") + A + node("EmbeddingGemma 2", "페이지 임베딩", "내 PC", "pc")
          + A + node("벡터 DB", "벡터 + 문서명 · 페이지", "", "db") + E + E + E + E)
    r2 = (node("질문") + '<div class="s7-ar long">→</div>' + node("EmbeddingGemma 2", "질문 임베딩", "내 PC", "pc")
          + A + node("검색", "가까운 페이지 3장", "", "db") + A + node("gpt-5.6-luna", "페이지 이미지 + 질문", "OpenAI API", "api")
          + A + node("보고서형 답변", "", "", "out"))
    mid = (E * 4 + '<div class="s7-mid">같은 모델 · 같은 768차원 공간</div>' + E
           + '<div class="s7-mid dn">↓ 가까운 순서로</div>' + E * 4)
    return ('<div class="s7-mm">'
            '<div class="s7-lane"><div class="s7-lh">문서 준비<em>문서를 올릴 때 한 번</em></div>'
            f'<div class="s7-grid">{r1}</div></div>'
            f'<div class="s7-grid s7-midrow">{mid}</div>'
            '<div class="s7-lane"><div class="s7-lh">질문<em>질문할 때마다</em></div>'
            f'<div class="s7-grid">{r2}</div></div></div>')


def report():
    """결론 → 근거 → 과정 순서의 답변 화면 예."""
    cards = "".join(f'<div class="s7-ev"><div class="th"></div><div><b>[{i}] 문서명 · 페이지</b><em>거리</em></div></div>' for i in (1, 2, 3))
    return ('<div class="s7-rep">'
            '<div class="s7-rk">결론</div><div class="s7-rc">답변을 눈에 띄는 상자에 먼저 <sup>[1]</sup> <sup>[2]</sup></div>'
            f'<div class="s7-rk">근거</div><div class="s7-evs">{cards}</div>'
            '<div class="s7-rk">과정</div><div class="s7-rp"><span>질문 임베딩 시간</span><span>검색 순위 · 거리</span>'
            '<span>답변 모델 응답 시간</span><span>토큰 수</span></div></div>')


def triples(rows=(("RAM", "has_error", "Soft Error"), ("Soft Error", "detected_by", "Parity"),
                  ("Parity", "has_limitation", "단일 비트만 검출"))):
    li = "".join(f'<div class="s7-tr"><span class="nd">{a}</span><span class="rl">{r}<i>→</i></span><span class="nd">{b}</span>'
                 f'<span class="src">문서명 · 페이지 · Chunk ID · 원문 문장</span></div>' for a, r, b in rows)
    return f'<div class="s7-trs">{li}</div>'


def track(icon, tag, title, desc, out):
    return (f'<div class="s7-tk"><div class="s7-tkh">{ic(icon)}<span>{tag}</span></div><h3>{title}</h3>'
            f'<p>{desc}</p><div class="s7-tko"><em>결과물</em>{out}</div></div>')


def keywords(words):
    return '<div class="s7-kw">' + "".join(f"<span>{w}</span>" for w in words) + "</div>"


def checks(items):
    return '<div class="chk">' + "".join(f"<div>{x}</div>" for x in items) + "</div>"


def text_loss():
    """같은 페이지 · 원본(본문 + 표 + 그래프) vs 텍스트 추출 결과. 설명용."""
    R, K, G = "#E8002D", "#26262B", "#DCDCE1"
    bars = "".join(f'<rect x="{40 + i * 34}" y="{150 - h}" width="22" height="{h}" fill="{K if i != 3 else R}"/>' for i, h in enumerate((58, 74, 66, 30, 52)))
    page = (f'<svg viewBox="0 0 260 330" class="tl-pg"><rect x="1" y="1" width="258" height="328" rx="8" fill="#fff" stroke="{K}" stroke-width="2"/>'
            f'<rect x="20" y="18" width="150" height="10" rx="3" fill="{K}"/>'
            + "".join(f'<rect x="20" y="{40 + i * 12}" width="{220 - (i % 2) * 40}" height="6" rx="3" fill="{G}"/>' for i in range(3))
            + f'<line x1="30" y1="150" x2="230" y2="150" stroke="{K}"/>{bars}'
            + '<text x="130" y="168" text-anchor="middle" font-size="11" fill="#666">리플로 조건별 보이드율 그래프</text>'
            + "".join(f'<rect x="20" y="{185 + r * 22}" width="220" height="22" fill="none" stroke="{K}" stroke-width="1"/>' for r in range(4))
            + "".join(f'<line x1="{20 + c * 73}" y1="185" x2="{20 + c * 73}" y2="273" stroke="{K}" stroke-width="1"/>' for c in (1, 2))
            + '<text x="130" y="292" text-anchor="middle" font-size="11" fill="#666">공정 조건 표</text>'
            + "".join(f'<rect x="20" y="{302 + i * 10}" width="{200 - i * 50}" height="6" rx="3" fill="{G}"/>' for i in range(2)) + "</svg>")
    txt = ('<div class="tl-tx"><div class="tl-h">텍스트 추출 결과</div>'
           '<p>Maintaining Low Voiding Solder Die Attach …</p><p>The reflow profile was adjusted to …</p>'
           '<p class="lost">[그래프 → 사라짐 · 막대 높이 · 빨간 막대의 의미 없음]</p>'
           '<p class="mix">Peak 245 30 60 Profile A 1.2 B …</p><p class="lost">[표 → 숫자만 한 줄로 · 어느 칸의 값인지 모름]</p>'
           '<p>Results show that …</p></div>')
    return f'<div class="tl-w"><div><div class="tl-h">원본 페이지</div>{page}</div><div class="tl-arr">→</div>{txt}</div>'
