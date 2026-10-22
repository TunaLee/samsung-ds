"""8교시 도식 · 화면 모형. 흰 바탕 · 검정 글자 · 빨강 강조 · 선 아이콘."""
from fig import ic


def tags(items, hl=()):
    return '<div class="s8-tags">' + "".join(
        f'<span class="{"on" if x in hl else ""}">{x}</span>' for x in items) + "</div>"


def prompt_map():
    """요청문의 네 묶음."""
    cols = [("chat", "먼저 확인", ["STEP 1 작성자 성명", "STEP 2 발표 목차", "STEP 3 촬영할 화면"]),
            ("window", "자료 확보", ["작업 원칙", "웹: 앱 실행 · 화면 캡처", "터미널: 실행 결과"]),
            ("form", "페이지 구성", ["정보 구성 · 권장 내용", "레이아웃 · 좁은 영역", "실제 결과 우선 · 디자인"]),
            ("html", "마무리", ["이미지 base64 내장", "구현 조건", "최종 확인 · 완성 기준"])]
    out = []
    for i, (icon, t, li) in enumerate(cols):
        rows = "".join(f"<li>{x}</li>" for x in li)
        out.append(f'<div class="s8-pm{" on" if i == 0 else ""}"><div class="pn">{i + 1:02d}</div>{ic(icon)}<b>{t}</b><ul>{rows}</ul></div>')
    return '<div class="s8-pmap">' + '<i class="pa">→</i>'.join(out) + "</div>"


def step3():
    st = [("STEP 1", "작성자 성명", "페이지 작성자 · 파일명에 사용"),
          ("STEP 2", "발표 목차", "프로젝트를 빠르게 확인 → 목차 제안"),
          ("STEP 3", "촬영할 화면", "웹: 스크린샷 목록 · 터미널: 실행 결과 목록")]
    cells = '<i class="pa">→</i>'.join(
        f'<div class="s8-st"><em>{a}</em><b>{t}</b><span>{d}</span><small>답변을 받은 뒤 다음 단계</small></div>' for a, t, d in st)
    stop = "".join(f"<span>{x}</span>" for x in ["앱 실행", "스크린샷 촬영", "HTML 작성", "base64 변환"])
    return (f'<div class="s8-step3">{cells}</div>'
            f'<div class="s8-stop"><b>확인이 끝나기 전에는 시작하지 않음</b>{stop}</div>')


def ask(text, who="AI의 질문"):
    return f'<div class="s8-ask"><div class="aw">{ic("chat")}<span>{who}</span></div><div class="aq">{text}</div></div>'


def term(lines, badge="실제 실행 결과"):
    li = "".join(f'<div class="tl"><span class="tp">{p}</span>{t}</div>' for p, t in lines)
    return (f'<div class="s8-term"><div class="tb"><i></i><i></i><i></i><em>{badge}</em></div>'
            f'<div class="tbody">{li}</div></div>')


def secflow(items, hl=None):
    """items: [(제목, 설명)] 세로로 읽는 발표 흐름 (가로 배치)."""
    out = "".join(f'<div class="s8-sf{" on" if hl is not None and i == hl else ""}"><em>{i + 1}</em><b>{t}</b><span>{d}</span></div>'
                  for i, (t, d) in enumerate(items))
    return f'<div class="s8-secflow">{out}</div>'


def chains(rows):
    out = ""
    for r in rows:
        out += '<div class="s8-ch">' + '<i>→</i>'.join(f"<span>{x}</span>" for x in r) + "</div>"
    return f'<div class="s8-chains">{out}</div>'


def exhibit():
    """전시관 · 확인 사이트 안의 좁은 영역에 발표 페이지가 들어간 모습."""
    stack = [("제목", "h"), ("짧은 설명", "t"), ("큰 실제 화면", "img"), ("핵심 포인트", "t"), ("다음 구간 제목", "h"), ("큰 실제 화면", "img")]
    blocks = "".join(f'<div class="xb {k}">{t}</div>' for t, k in stack)
    return ('<div class="s8-ex"><div class="exbar">' + ic("window") + '<span>전시관 · 확인 사이트</span></div>'
            '<div class="exbody"><div class="exside">목록<br>필터<br>작품 정보</div>'
            f'<div class="excol"><div class="exw">약 900 ~ 1050px</div>{blocks}</div>'
            '<div class="exside">댓글<br>평가<br>메뉴</div></div></div>')


def layouts():
    """피할 배치 4가지와 기본 배치."""
    bad = [("카드 2개 좌우", '<div class="g2"><i></i><i></i></div>'),
           ("카드 3개 한 줄", '<div class="g3"><i></i><i></i><i></i></div>'),
           ("설명 + 스크린샷 좌우", '<div class="g2"><i class="tx"></i><i class="im"></i></div>'),
           ("스크린샷 갤러리", '<div class="g4"><i class="im"></i><i class="im"></i><i class="im"></i><i class="im"></i></div>')]
    b = "".join(f'<div class="lb"><div class="wf">{w}</div><span>{t}</span></div>' for t, w in bad)
    good = ('<div class="wf v"><i class="h"></i><i class="tx"></i><i class="im big"></i><i class="tx"></i></div>')
    return (f'<div class="s8-lay"><div class="lbad"><div class="lh">기본으로 쓰지 않는 배치</div><div class="lgrid">{b}</div></div>'
            f'<div class="lgood"><div class="lh">기본 배치 · 세로 1단</div>{good}'
            '<div class="lcap">제목 → 짧은 설명 → 큰 실제 화면 → 핵심 포인트</div></div></div>')


def embed_flow():
    st = [("folder", "캡처 파일", "<code>captures/main.png</code>"),
          ("html", "작성 중 HTML", "<code>&lt;!--IMG:captures/main.png--&gt;</code>"),
          ("tool", "Python 스크립트", "찾기 · 확인 · 인코딩 · 치환"),
          ("check", "최종 HTML", "<code>data:image/...;base64,...</code>")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc"><div class="fi">{ic(i)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>' for i, t, d in st)
    return f'<div class="tcall s8-emb">{cells}</div>'


def checks(items, cols=2, start=1):
    li = "".join(f'<div class="ck"><em>{start + i}</em><span>{x}</span></div>' for i, x in enumerate(items))
    return f'<div class="s8-checks c{cols}">{li}</div>'


def recap_map():
    cols = [("model", "판단 · 행동 구조", ["AI Agent", "LLM", "Instructions · Guardrails", "Tools", "MCP Server"]),
            ("search", "정보 준비 · RAG", ["Context Window", "문서 준비 · 청킹 · 검색", "Metadata · GraphRAG · Text-to-SQL", "Advanced RAG", "Parent–Child RAG"]),
            ("nodes", "역할 분리 · 호출", ["Multi-Agent", "Decisions + 조사 Agent"]),
            ("link", "확장", ["Multi-modal RAG", "문서 계층화"])]
    out = []
    for i, (icon, t, li) in enumerate(cols):
        rows = "".join(f"<li>{x}</li>" for x in li)
        out.append(f'<div class="s8-rc"><div class="rh">{ic(icon)}<b>{t}</b></div><ul>{rows}</ul></div>')
    return '<div class="s8-recap">' + '<i class="pa">→</i>'.join(out) + "</div>"


def lanes(rows):
    """rows: [(라벨, [(제목, 설명)], 강조 인덱스)] 가로 흐름 여러 줄."""
    out = ""
    for label, st, hl in rows:
        cells = '<i>→</i>'.join(f'<span class="{"on" if j == hl else ""}"><b>{t}</b><em>{d}</em></span>' for j, (t, d) in enumerate(st))
        out += f'<div class="nr"><div class="nr-l">{label}</div><div class="nr-f">{cells}</div></div>'
    return f'<div class="nrs s8-lanes">{out}</div>'


def decisions():
    """6교시 구조: 판정기와 조사 Agent의 역할 분담."""
    st = [("rule", "Decisions", "반복 판정"), ("window", "앱", "기준값 이상 이벤트만 넘김"),
          ("model", "조사 Agent", "근거가 필요한 건만 조사"), ("tool", "조회 Tool", "근거 확인")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc{" s8-core" if i == 2 else ""}"><div class="fi">{ic(a)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>'
        for i, (a, t, d) in enumerate(st))
    return f'<div class="tcall">{cells}</div>'


def hier():
    st = [("rule", "목차", "읽을 범위 고르기"), ("doc", "장별 요약 MD", "원본 파일 · 장 · 페이지 연결"), ("book", "챕터별 PDF", "원문 확인 · 수치 · 예외 조건")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc"><div class="fi">{ic(a)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>' for a, t, d in st)
    return f'<div class="tcall">{cells}</div>'
