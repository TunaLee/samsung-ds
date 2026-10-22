"""임베딩 시각화: 축 하나 = 특징 하나 → 특징이 늘수록 세밀하게 구분."""
import random

R, K, G, M, B = "#E8002D", "#26262B", "#DCDCE1", "#6B6B73", "#2F6BD8"
# 세 문장 · 설명용 특징 값 (0~1)
S = [("S1", "웨이퍼 식각 레시피", R, dict(semi=.92, cook=.06, etch=.88)),
     ("S2", "박막 증착 레시피", "#FF7A93", dict(semi=.86, cook=.08, etch=.14)),
     ("S3", "김치찌개 레시피", K, dict(semi=.07, cook=.94, etch=.5))]


def _defs(pid):
    return (f'<defs><marker id="{pid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{M}"/></marker></defs>')


def _dot(x, y, key, color, label=True, r=11):
    t = f'<text x="{x}" y="{y - 18}" text-anchor="middle" class="ef-l" fill="{color}">{key}</text>' if label else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#fff" stroke-width="3"/>{t}'


def line1d():
    """특징 하나: 반도체 관련도 한 줄."""
    x0, x1, y = 60, 600, 120
    s = f'<svg viewBox="0 0 660 200" class="ef">{_defs("e1")}'
    s += f'<line x1="{x0}" y1="{y}" x2="{x1 + 20}" y2="{y}" stroke="{M}" stroke-width="3" marker-end="url(#e1)"/>'
    s += f'<text x="{x0}" y="{y + 40}" class="ef-a">0</text><text x="{x1}" y="{y + 40}" class="ef-a" text-anchor="end">1</text>'
    s += f'<text x="{(x0 + x1) / 2}" y="{y + 70}" text-anchor="middle" class="ef-ax">특징 ① 반도체 관련도</text>'
    for k, _, c, v in S:
        s += _dot(x0 + v["semi"] * (x1 - x0), y, k, c)
    s += f'<rect x="{x0 + .84 * (x1 - x0) - 30}" y="{y - 60}" width="{.1 * (x1 - x0) + 60}" height="84" rx="14" fill="none" stroke="{R}" stroke-width="2" stroke-dasharray="6 5"/>'
    return s + "</svg>"


def plane2d():
    """특징 둘: 반도체 관련도 × 요리 관련도."""
    ox, oy, W, H = 80, 330, 470, 280
    s = f'<svg viewBox="0 0 620 400" class="ef">{_defs("e2")}'
    for i in range(1, 5):
        s += f'<line x1="{ox + W * i / 4}" y1="{oy}" x2="{ox + W * i / 4}" y2="{oy - H}" stroke="#F1F1F4" stroke-width="2"/>'
        s += f'<line x1="{ox}" y1="{oy - H * i / 4}" x2="{ox + W}" y2="{oy - H * i / 4}" stroke="#F1F1F4" stroke-width="2"/>'
    s += f'<line x1="{ox}" y1="{oy}" x2="{ox + W + 20}" y2="{oy}" stroke="{M}" stroke-width="3" marker-end="url(#e2)"/>'
    s += f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - H - 20}" stroke="{M}" stroke-width="3" marker-end="url(#e2)"/>'
    s += f'<text x="{ox + W}" y="{oy + 34}" text-anchor="end" class="ef-ax">특징 ① 반도체 관련도 →</text>'
    s += f'<text x="{ox - 16}" y="{oy - H - 26}" class="ef-ax">↑ 특징 ② 요리 관련도</text>'
    for k, _, c, v in S:
        s += _dot(ox + v["semi"] * W, oy - v["cook"] * H, k, c)
    s += f'<ellipse cx="{ox + .89 * W}" cy="{oy - .07 * H}" rx="62" ry="36" fill="none" stroke="{R}" stroke-width="2" stroke-dasharray="6 5"/>'
    return s + "</svg>"


def _p3(x, y, z, ox=330, oy=330, L=230):
    """간단한 등각 투영: x 오른쪽 아래, z 왼쪽 아래, y 위."""
    return ox + (x - z) * L * .87, oy + (x + z) * L * .5 - y * L


def space3d():
    """특징 셋: 반도체 · 요리 · 식각↔증착."""
    s = f'<svg viewBox="0 0 660 470" class="ef">{_defs("e3")}'
    o = _p3(0, 0, 0)
    for (x, y, z), name, anchor, dx, dy in [((1.08, 0, 0), "특징 ① 반도체", "start", 8, 6), ((0, 1.15, 0), "특징 ③ 식각 ↔ 증착", "middle", 0, -12),
                                           ((0, 0, 1.08), "특징 ② 요리", "end", -8, 6)]:
        p = _p3(x, y, z)
        s += f'<line x1="{o[0]}" y1="{o[1]}" x2="{p[0]}" y2="{p[1]}" stroke="{M}" stroke-width="3" marker-end="url(#e3)"/>'
        s += f'<text x="{p[0] + dx}" y="{p[1] + dy}" text-anchor="{anchor}" class="ef-ax">{name}</text>'
    for k, _, c, v in S:
        p = _p3(v["semi"], v["etch"], v["cook"])
        f = _p3(v["semi"], 0, v["cook"])
        s += f'<line x1="{p[0]}" y1="{p[1]}" x2="{f[0]}" y2="{f[1]}" stroke="{c}" stroke-width="2" stroke-dasharray="4 4"/>'
        s += f'<ellipse cx="{f[0]}" cy="{f[1]}" rx="9" ry="4" fill="{G}"/>'
        s += _dot(p[0], p[1], k, c)
    return s + "</svg>"


def dims():
    """특징 수가 늘수록 더 세밀하게."""
    steps = [("1", "반도체인가", "S1 · S2 구분 불가"), ("2", "+ 요리인가", "S3 분리"), ("3", "+ 식각인가 증착인가", "S1 · S2 분리"),
             ("1,536", "+ 문체 · 주제 · 맥락 …", "아주 미묘한 차이까지")]
    out = ""
    for i, (n, t, d) in enumerate(steps):
        hl = " on" if i == 3 else ""
        bars = "".join(f'<i style="height:{12 + (j * 37 % 40)}px"></i>' for j in range(min(int(n.replace(",", "")) if n != "1,536" else 24, 24)))
        out += (f'<div class="ef-d{hl}"><div class="ef-bars">{bars}</div><b>{n}<small>개 특징</small></b>'
                f'<span>{t}</span><em>{d}</em></div>')
    return f'<div class="ef-ds">{out}</div>'


def strip(seed, like=None, n=24):
    """벡터를 색 띠로: 칸 하나 = 숫자 하나 (빨강 +, 회색 −, 진할수록 큼)."""
    rnd = random.Random(seed)
    vals = [rnd.uniform(-1, 1) for _ in range(n)]
    if like is not None:
        base = random.Random(like)
        b = [base.uniform(-1, 1) for _ in range(n)]
        vals = [x * .85 + rnd.uniform(-.15, .15) for x in b]
    cells = "".join(
        f'<i style="background:{"rgba(232,0,45," if v > 0 else "rgba(38,38,43,"}{.15 + .85 * abs(v):.2f})"></i>' for v in vals)
    return f'<div class="ef-strip">{cells}<span>… 1,536칸</span></div>'


def embed2():
    rows = [("S1", "웨이퍼 식각 공정의 가스 유량 · 압력 레시피", strip(1)), ("S2", "박막 증착 설비의 온도 · 진공 레시피", strip(2, like=1)),
            ("S3", "돼지고기 김치찌개 레시피와 조리 순서", strip(3))]
    out = "".join(f'<div class="ef-row"><b class="{"far" if k == "S3" else ""}">{k}</b><span>{t}</span><div class="ef-arr">→</div>{v}</div>'
                  for k, t, v in rows)
    return (f'<div class="ef-emb"><div class="ef-hd"><span>문장</span><span></span><span>벡터 · 칸 하나가 숫자 하나</span></div>{out}'
            f'<div class="ef-leg"><i class="p"></i>양수 <i class="n"></i>음수 · 진할수록 큰 값 · S1과 S2는 무늬가 비슷</div></div>')


def space2():
    """원점에서 나가는 화살표 + 각도 호 + 점 (위쪽 반원)."""
    import math
    ox, oy, L = 270, 350, 250
    pts = [("S1", R, 40), ("S2", "#FF7A93", 24), ("S3", K, 128)]
    s = '<svg viewBox="0 0 560 410" class="ef">'
    for i in range(1, 4):
        rr = L * i / 3
        s += f'<path d="M{ox - rr} {oy} A{rr} {rr} 0 0 1 {ox + rr} {oy}" fill="none" stroke="#EFEFF2" stroke-width="2"/>'
    s += f'<line x1="{ox - L - 10}" y1="{oy}" x2="{ox + L + 10}" y2="{oy}" stroke="{G}" stroke-width="2"/>'
    for k, c, a in pts:
        r = math.radians(a)
        x, y = ox + L * math.cos(r), oy - L * math.sin(r)
        s += f'<line x1="{ox}" y1="{oy}" x2="{x}" y2="{y}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
        s += _dot(x, y, k, c, r=14)
    s += f'<circle cx="{ox}" cy="{oy}" r="6" fill="{K}"/>'

    def arc(a1, a2, rr, color, label, lr):
        r1, r2 = math.radians(a1), math.radians(a2)
        x1, y1 = ox + rr * math.cos(r1), oy - rr * math.sin(r1)
        x2, y2 = ox + rr * math.cos(r2), oy - rr * math.sin(r2)
        mid = math.radians((a1 + a2) / 2)
        lx, ly = ox + lr * math.cos(mid), oy - lr * math.sin(mid)
        return (f'<path d="M{x1} {y1} A{rr} {rr} 0 0 0 {x2} {y2}" fill="none" stroke="{color}" stroke-width="4"/>'
                f'<text x="{lx}" y="{ly}" text-anchor="middle" class="ef-s" fill="{color}">{label}</text>')
    s += arc(24, 40, 150, R, "", 0)
    s += arc(40, 128, 80, M, "", 0)
    s += f'<text x="{ox + 140}" y="{oy + 36}" text-anchor="middle" class="ef-s" fill="{R}">S1 · S2 각도 작음 → 유사도 높음</text>'
    s += f'<text x="{ox - 140}" y="{oy + 36}" text-anchor="middle" class="ef-s" fill="{M}">S1 · S3 각도 큼 → 유사도 낮음</text>'
    return s + "</svg>"
