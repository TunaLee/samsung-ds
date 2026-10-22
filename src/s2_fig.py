"""2교시 도식 (원본 교안 그림을 이 덱 스타일로 다시 그림)."""
from fig import ic

R, K, G, M, L = "#E8002D", "#26262B", "#DCDCE1", "#6B6B73", "#F1F1F4"


def score_read():
    """Chroma 코사인 거리 → 1 − 거리 → 화면 점수."""
    st = [("doc", "lab/store.py", "Chroma 거리 설정"), ("search", "코사인 거리", "Chroma가 반환"),
          ("pen", "1 − 거리", "앱이 계산"), ("chart", "화면 점수", "클수록 방향이 비슷")]
    cells = '<div class="tc-arr">→</div>'.join(
        f'<div class="tc{" p2-on" if i == 3 else ""}"><div class="fi">{ic(a)}</div><div class="ft">{t}</div><div class="fd">{d}</div></div>'
        for i, (a, t, d) in enumerate(st))
    return f'<div class="tcall">{cells}</div>'


def highlight_chunk():
    """근거 청크 안에서 질문과 가장 가까운 문장 하나를 노란색으로."""
    rows = [(92, False), (78, False), (96, True), (70, False), (84, False)]
    li = "".join(
        f'<div class="p2-sl{" on" if h else ""}"><span class="p2-sn">문장 {i + 1}</span>'
        f'<i style="width:{w}%"></i>{"<em>점수</em>" if h else ""}</div>' for i, (w, h) in enumerate(rows))
    return (f'<div class="p2-hc"><div class="p2-q"><b>질문</b>1 FIT 는 무엇을 뜻하나요?</div>'
            f'<div class="p2-card"><div class="p2-ch">근거 청크 #1 · 출처 · 검색 점수</div>{li}</div>'
            f'<div class="p2-leg"><span class="y"></span>질문 벡터와 유사도가 가장 높은 문장 하나 · 점수 함께 표시</div></div>')


def semantic_cut():
    """원본 01.png: 이웃 문장 유사도가 크게 떨어지는 곳에서 자르기."""
    def s(n):
        return f'<div class="p2-s">문장 {n}</div>'

    def p(v, cut=False):
        return f'<div class="p2-p{" cut" if cut else ""}">{v}</div>'
    c1 = f'<div class="p2-chunk"><div class="p2-cl">청크 1</div><div class="p2-row">{s(1)}{p("0.82")}{s(2)}{p("0.79")}{s(3)}</div></div>'
    c2 = f'<div class="p2-chunk"><div class="p2-cl">청크 2</div><div class="p2-row">{s(4)}{p("0.85")}{s(5)}</div></div>'
    mid = f'<div class="p2-cutc"><div class="p2-scis">자르는 지점</div>{p("0.31", True)}<div class="p2-vl"></div></div>'
    return (f'<div class="p2-sem"><div class="p2-semr">{c1}{mid}{c2}</div>'
            '<div class="p2-semb"><div class="p2-semk">숫자 = 이웃한 두 문장의 유사도<br>(임베딩 벡터의 코사인 유사도)</div>'
            '<div class="p2-semx"><b>유사도가 크게 떨어짐 → 여기서 자름</b><span>이웃 문장 사이의 주제가 바뀐 지점</span></div></div></div>')


def _chart(vals, title, sub, thr, cuts=()):
    w, h, x0, y0 = 460, 250, 50, 20
    n = len(vals)
    pts = " ".join(f"{x0 + i * (w - x0 - 10) / (n - 1):.1f},{y0 + (1 - v) * (h - 60):.1f}" for i, v in enumerate(vals))
    ty = y0 + (1 - thr) * (h - 60)
    out = [f'<svg viewBox="0 0 {w} {h}" class="p2-chart">',
           f'<line x1="{x0}" y1="{y0 - 6}" x2="{x0}" y2="{h - 40}" stroke="{K}" stroke-width="2"/>',
           f'<line x1="{x0}" y1="{h - 40}" x2="{w - 4}" y2="{h - 40}" stroke="{K}" stroke-width="2"/>',
           f'<line x1="{x0}" y1="{ty:.1f}" x2="{w - 4}" y2="{ty:.1f}" stroke="{M}" stroke-width="2" stroke-dasharray="7 6"/>',
           f'<text x="{w - 6}" y="{ty - 8:.1f}" text-anchor="end" class="p2-ct">기준값</text>',
           f'<polyline points="{pts}" fill="none" stroke="{K}" stroke-width="2.4" stroke-linejoin="round"/>']
    for i in cuts:
        x = x0 + i * (w - x0 - 10) / (n - 1)
        y = y0 + (1 - vals[i]) * (h - 60)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{R}"/><text x="{x:.1f}" y="{y - 14:.1f}" text-anchor="middle" class="p2-ct r">절단점</text>')
    out.append(f'<text x="{(w + x0) / 2}" y="{h - 14}" text-anchor="middle" class="p2-cx">문장 순서</text>'
               f'<text x="18" y="{(h - 40) / 2 + 10}" text-anchor="middle" class="p2-cx" transform="rotate(-90 18 {(h - 40) / 2 + 10})">문장 간 거리</text></svg>')
    return f'<div class="p2-chw"><div class="p2-cht">{title}</div><div class="p2-chs">{sub}</div>{"".join(out)}</div>'


def breakpoints():
    """원본 02.png: 소설 vs 산업 백서의 문장 간 거리."""
    novel = [.35, .72, .28, .66, .4, .8, .3, .58, .25, .75, .45, .82, .33, .62, .27, .7, .5, .38, .77, .3, .64, .42, .85, .36, .6, .29, .73, .47, .68, .34]
    paper = [.12, .15, .11, .14, .17, .13, .16, .12, .9, .14, .13, .17, .15, .12, .16, .14, .13, .93, .15, .12, .16, .14, .13, .17, .15, .14, .16, .13, .15, .14]
    return ('<div class="p2-bp">'
            + _chart(novel, "소설", "화자 전환 · 묘사 · 대화 → 문장 간 거리가 크게 출렁임", .55)
            + _chart(paper, "산업 백서", "전문 용어 반복 → 평소엔 가깝다가 소제목 · 주제 전환에서 급상승", .55, cuts=(8, 17))
            + '</div>')


def size_compare():
    """큰 청크와 작은 청크가 담는 범위."""
    big = ('<div class="p2-sz"><div class="p2-szh">큰 청크</div>'
           '<div class="p2-blk big"><span class="t a">정의</span><span class="t b">시험 조건</span><span class="t c">적용 대상</span><span class="t d">다른 주제</span></div>'
           '<ul class="ul"><li>앞뒤 맥락 · 조건이 함께 → <b>정보량</b></li><li>주제가 섞여 벡터가 흐려짐 · 관계없는 내용까지 전달</li></ul></div>')
    small = ('<div class="p2-sz"><div class="p2-szh">작은 청크</div>'
             '<div class="p2-blk sm"><span class="t a">정의</span><span class="gap"></span><span class="t b">시험 조건</span><span class="gap"></span><span class="t c">적용 대상</span></div>'
             '<ul class="ul"><li>한 가지 내용 → 질문과 맞는 조각을 <b>찾기 쉬움</b></li><li>설명이 끊겨 답변에 필요한 맥락 부족</li></ul></div>')
    return f'<div class="p2-szs">{big}{small}</div>'


def parent_child():
    """부모 청크(절 단위) 안의 자식 청크로 찾고, 부모를 전달."""
    def parent(n, hit):
        kids = "".join(f'<span class="k{" hit" if hit and j == 1 else ""}">자식 {n}-{j + 1}</span>' for j in range(3))
        return f'<div class="p2-par{" on" if hit else ""}"><div class="p2-parh">부모 {n} · 절 단위</div><div class="p2-kids">{kids}</div></div>'
    return ('<div class="p2-pc">'
            '<div class="p2-pcl"><div class="p2-pch">문서</div>' + parent(1, False) + parent(2, True) + parent(3, False) + '</div>'
            '<div class="p2-pcr">'
            f'<div class="p2-pcs"><b>1</b><div>{ic("chat")}<span>질문</span></div></div>'
            f'<div class="p2-pcs"><b>2</b><div>{ic("search")}<span><em>자식 청크</em>에서 검색 · 문장 몇 개 단위</span></div></div>'
            f'<div class="p2-pcs on"><b>3</b><div>{ic("folder")}<span>찾은 자식의 <em>부모 청크</em>를 LLM에 전달</span></div></div>'
            f'<div class="p2-pcs"><b>4</b><div>{ic("model")}<span>답변</span></div></div>'
            '</div></div>')


def id_vectors():
    """EQ-1023과 EQ-1032: 글자 하나 차이, 다른 장비, 가까운 벡터."""
    return f'''<div class="p2-idv"><svg viewBox="0 0 560 300" class="p2-ids">
<line x1="40" y1="260" x2="540" y2="260" stroke="{G}" stroke-width="2"/><line x1="60" y1="20" x2="60" y2="280" stroke="{G}" stroke-width="2"/>
<circle cx="390" cy="110" r="64" fill="#FFF5F7" stroke="{R}" stroke-width="2" stroke-dasharray="6 6"/>
<circle cx="372" cy="98" r="11" fill="{K}"/><circle cx="406" cy="122" r="11" fill="{R}"/>
<text x="300" y="70" class="p2-it">EQ-1023</text><text x="420" y="160" class="p2-it r">EQ-1032</text>
<text x="390" y="206" text-anchor="middle" class="p2-is">매우 가까운 벡터로 표현될 수 있음</text></svg>
<div class="p2-idr"><div class="p2-idc"><code>EQ-1023</code><code class="r">EQ-1032</code></div>
<div class="p2-idt">글자 하나 차이 · <b>전혀 다른 장비</b></div>
<ul class="ul"><li>임베딩 모델에게 식별자는 뜻이 거의 없는 문자열</li><li>필요한 것: <b>글자가 정확히 일치하는지</b> 보는 검색</li></ul></div></div>'''


def two_search():
    """의미 검색과 BM25가 잘하는 것 (원본 04.png 01)."""
    def col(h, sub, good, bad, rng, cls):
        g = "".join(f'<li class="g">{x}</li>' for x in good)
        b = "".join(f'<li class="b">{x}</li>' for x in bad)
        return f'<div class="p2-ts {cls}"><div class="p2-tsh">{h}</div><div class="p2-tss">{sub}</div><ul>{g}{b}</ul><div class="p2-tsr">점수 범위 {rng}</div></div>'
    return ('<div class="p2-tsw">'
            + col("의미 검색", "임베딩 + 코사인", ["표현이 달라도 찾음", "오타 · 유의어 · 문맥에 강함"], ["정확한 용어 · 고유명사 · 숫자를 놓치기 쉬움"], "<b>0 ~ 1</b> · 코사인 유사도", "a")
            + col("BM25", "키워드 일치 빈도", ["정확히 그 단어가 든 문서를 잡음", "제품 코드 · 조항 · 드문 용어에 강함"], ["표현이 다르면 찾지 못함"], "<b>0 ~ 수십</b> · 상한 없음", "b")
            + '</div>')


def scale_gap():
    """원본 04.png 02: 점수를 그대로 더하면 BM25가 결과를 정함."""
    return ('<div class="p2-sg">'
            '<div class="p2-sgr"><span>코사인</span><div class="p2-sgt"><i style="width:4.2%"></i></div><b>0.87</b></div>'
            '<div class="p2-sgr on"><span>BM25</span><div class="p2-sgt"><i style="width:88%"></i></div><b>18.4</b></div>'
            '<div class="p2-sgx">같은 축에 놓으면 <b>20배 이상</b> 차이 · <code>0.76 + 18.4 = 19.16</code> → <b>96%가 BM25 몫</b></div>'
            '</div>')


def rrf_formula():
    vals = [("1위", "1/61", "0.01639"), ("2위", "1/62", "0.01613"), ("3위", "1/63", "0.01587"), ("4위", "1/64", "0.01562"), ("5위", "1/65", "0.01538")]
    rows = "".join(f'<div class="p2-rv"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in vals)
    return ('<div class="p2-rf"><div class="p2-rfl"><div class="p2-rfe">RRF(d) = Σ 1 / (k + rank<sub>i</sub>(d))</div>'
            '<ul class="ul"><li>각 검색기의 <b>등수만</b> 가져와 역수를 더함</li><li>점수의 단위 · 분포가 사라짐 → 정규화 · 가중치 조정 불필요</li>'
            '<li><b>k = 60</b> · 1등과 2등의 격차를 완만하게 · 한 검색기가 결과를 독점하지 못하게</li></ul></div>'
            f'<div class="p2-rfr"><div class="p2-rfh">k = 60일 때 등수별 값</div>{rows}</div></div>')


def three_cols():
    """세 열 비교 화면 (원본 04.png 04, 축약)."""
    cols = [("의미 검색", "코사인 0~1", ["휴가 이월 및 소멸 규정", "미사용 연차는 다음 해로 이월 가능", "연차 촉진 제도 안내"],
             "이월 한도(5일) · 신청 절차 빠짐", False),
            ("BM25", "점수 0~∞", ["연차 이월 한도는 최대 5일", "휴가 이월 및 소멸 규정", "이월 신청 절차 — 인사팀 승인"],
             "이월 가능 여부의 기본 설명 빠짐", False),
            ("하이브리드 (RRF)", "순위 결합", ["휴가 이월 및 소멸 규정", "연차 이월 한도는 최대 5일", "미사용 연차는 다음 해로 이월 가능"],
             "양쪽에서만 나오던 조각이 한 답변에", True)]
    out = ""
    for h, s, items, res, ok in cols:
        li = "".join(f'<div class="p2-3i"><b>{i + 1}</b>{x}</div>' for i, x in enumerate(items))
        out += (f'<div class="p2-3c{" on" if ok else ""}"><div class="p2-3h"><b>{h}</b><span>{s}</span></div>{li}'
                f'<div class="p2-3a">… 상위 5개 · 생성된 답변</div><div class="p2-3r{" ok" if ok else ""}">{"✓" if ok else "×"} {res}</div></div>')
    return f'<div class="p2-3q"><span>질의</span>연차 휴가 이월 규정</div><div class="p2-3w">{out}</div>'
