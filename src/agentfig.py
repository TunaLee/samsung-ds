"""AI Agent 과정용 도식 (원본 교안 그림을 이 덱 스타일로 다시 그림)."""
from fig import ic

R, K, G, M = "#E8002D", "#26262B", "#DCDCE1", "#6B6B73"


def context_stack():
    """지침 · 도구 · 참고 정보 → LLM, 전체가 Context Window 안."""
    rows = [("book", "Instructions · 지침", "역할 · 업무 규칙 · 답변 형식", "어떻게 처리하고 답할까"),
            ("tool", "Tools · 도구 정의", "도구 이름 · 설명 · 입력 규격", "어떤 기능을 쓸 수 있을까"),
            ("folder", "Context Information · 참고 정보", "질문 · 선택한 이력 · 문서 · 도구 결과", "무엇을 근거로 답할까")]
    li = "".join(f'<div class="cs-row"><div class="cs-ic">{ic(i)}</div><div><b>{t}</b><span>{d}</span></div><em>{q}</em></div>'
                 for i, t, d, q in rows)
    return (f'<div class="cs"><div class="cs-in"><div class="cs-h">모델에 전달하는 전체 입력</div>{li}</div>'
            f'<div class="cs-arr">→</div><div class="cs-llm">{ic("model")}<b>LLM</b><span>해석 · 판단</span><span>답변 또는 도구 호출 요청</span></div></div>'
            f'<div class="cs-win"><b>Context Window</b> 한 번의 요청에서 쓸 수 있는 토큰 한도 · 입력 + 출력(+ 추론) 공간을 함께 계산</div>')


def budget(total=12000, parts=(("지침 · 도구 정의", 2000, K), ("질문 · 선택한 이력", 2000, M), ("문서 · 도구 결과", 8000, R))):
    seg = "".join(f'<div class="bg-s" style="flex:{v};background:{c}"><b>{v:,}</b><span>{n}</span></div>' for n, v, c in parts)
    return (f'<div class="bg"><div class="bg-h">입력 예산 {total:,} 토큰 (설명용 가정)</div><div class="bg-bar">{seg}</div>'
            f'<div class="bg-out">+ 출력 · 추론 공간은 별도로 남겨 둠</div></div>')


def three_ways():
    rows = [("사람이 선택", ["사람이 필요한 문단 고르기", "질문과 함께 전달", "LLM이 읽고 답변"]),
            ("문서 전체 전달", ["짧은 자료 전체", "질문과 함께 전달", "LLM이 읽고 답변"]),
            ("RAG", ["질문으로 관련 자료 검색", "질문 + 검색된 자료", "LLM이 읽고 답변"])]
    out = ""
    for i, (h, st) in enumerate(rows):
        hl = " hl" if i == 2 else ""
        cells = '<i>→</i>'.join(f"<span>{x}</span>" for x in st)
        out += f'<div class="tw{hl}"><b>{h}</b><div class="tw-f">{cells}</div></div>'
    return f'<div class="tws">{out}</div>'


def embed():
    sent = [("S1", "웨이퍼 식각 공정의 가스 유량 · 압력 레시피", "[0.082, −0.145, 0.231, …]"),
            ("S2", "박막 증착 설비의 온도 · 진공 레시피", "[0.079, −0.138, 0.228, …]"),
            ("S3", "돼지고기 김치찌개 레시피와 조리 순서", "[−0.312, 0.451, −0.089, …]")]
    left = "".join(f'<div class="em-s"><b>{k}</b>{t}</div>' for k, t, _ in sent)
    right = "".join(f'<div class="em-v{" far" if k == "S3" else ""}"><b>{k}</b><code>{v}</code></div>' for k, _, v in sent)
    return (f'<div class="em"><div class="em-col"><div class="em-h">문장</div>{left}</div><div class="em-arr">→</div>'
            f'<div class="em-m">{ic("model")}<b>임베딩 모델</b><span>문장 → 숫자 배열</span></div><div class="em-arr">→</div>'
            f'<div class="em-col"><div class="em-h">벡터 (숫자 배열)</div>{right}</div></div>')


def space():
    """2D 의미 공간: 공정 레시피 둘은 가깝고, 요리 레시피는 멀다."""
    return f'''<svg viewBox="0 0 640 380" class="vsp">
<defs><marker id="va" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{K}"/></marker>
<marker id="vr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{R}"/></marker></defs>
<line x1="60" y1="330" x2="610" y2="330" stroke="{G}" stroke-width="2"/><line x1="320" y1="20" x2="320" y2="350" stroke="{G}" stroke-width="2"/>
<line x1="320" y1="330" x2="560" y2="140" stroke="{R}" stroke-width="4" marker-end="url(#vr)"/>
<line x1="320" y1="330" x2="575" y2="200" stroke="{R}" stroke-width="4" marker-end="url(#vr)"/>
<line x1="320" y1="330" x2="110" y2="110" stroke="{K}" stroke-width="4" marker-end="url(#va)"/>
<path d="M545 150 Q600 160 565 205" fill="none" stroke="{R}" stroke-width="2" stroke-dasharray="5 5"/>
<text x="560" y="128" class="vt r">S1 식각 공정</text><text x="582" y="222" class="vt r">S2 증착 공정</text>
<text x="70" y="98" class="vt">S3 김치찌개</text>
<text x="420" y="300" class="vs">가까움 → 유사도 높음</text><text x="120" y="250" class="vs">멀리 → 유사도 낮음</text></svg>'''


def cosine():
    return f'''<svg viewBox="0 0 420 320" class="vsp">
<defs><marker id="ca" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{K}"/></marker>
<marker id="cr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{R}"/></marker></defs>
<line x1="60" y1="260" x2="400" y2="260" stroke="{G}" stroke-width="2"/><line x1="60" y1="20" x2="60" y2="280" stroke="{G}" stroke-width="2"/>
<line x1="60" y1="260" x2="320" y2="260" stroke="{K}" stroke-width="5" marker-end="url(#ca)"/>
<line x1="60" y1="260" x2="190" y2="260" stroke="{R}" stroke-width="7" marker-end="url(#cr)"/>
<line x1="60" y1="260" x2="60" y2="130" stroke="{K}" stroke-width="5" marker-end="url(#ca)"/>
<line x1="190" y1="250" x2="70" y2="140" stroke="{M}" stroke-width="2" stroke-dasharray="6 5"/>
<text x="180" y="292" class="vt r">A (1, 0)</text><text x="300" y="292" class="vt">B (2, 0)</text><text x="72" y="122" class="vt">C (0, 1)</text>
<text x="140" y="185" class="vs">거리 √2</text><path d="M60 230 L90 230 L90 260" fill="none" stroke="{M}" stroke-width="2"/></svg>'''


def naive_rag():
    def lane(label, steps, hl):
        cells = '<i>→</i>'.join(f'<span class="{"on" if j == hl else ""}"><b>{t}</b><em>{d}</em></span>' for j, (t, d) in enumerate(steps))
        return f'<div class="nr"><div class="nr-l">{label}</div><div class="nr-f">{cells}</div></div>'
    return ('<div class="nrs">'
            + lane("저장할 때 · 문서 1회", [("PDF", "원본"), ("파싱", "글자 꺼내기"), ("청킹", "조각 나누기"), ("임베딩", "숫자 배열"), ("저장소", "조각 + 벡터 + 출처")], 3)
            + '<div class="nr-mid">↓ 가까운 조각 몇 개만 꺼냄</div>'
            + lane("물어볼 때 · 질문마다", [("질문", ""), ("질문 임베딩", "같은 모델"), ("검색", "가까운 순"), ("생성", "근거로 답변"), ("답", "")], 2)
            + "</div>")
