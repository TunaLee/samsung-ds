"""6교시 · Multi-Agent · Decisions와 조사 Agent (원본: 노션 교안 6교시)."""
import fig
import s6_fig as sf
from kit import (big, cards, cover, esc, flow, ill, lab, note, page, pane, prompt, section, steps, table, two, ul)
import vizanim

TITLE = "Multi-Agent · Decisions와 조사 Agent"
DOC = "https://developers.openai.com/api/docs/guides/decisions"

PROMPT = """agent-sim의 Decisions 실습을 구현·개선해 줘.

목표는 UI 개발이 아니라 OpenAI Decisions API를 실제 호출하고, 수강생이 서버에 전송한 Request와 실제 Response를 직접 확인하는 것이다.

먼저 README와 기존 코드를 확인해 줘. Decisions 탭이 있으면 재사용하고, 없으면 기존 탭 구조에 최소한으로 추가해 줘. 도구·MCP·에이전트 등 다른 기능은 유지하고, 불필요한 UI나 구조 변경은 하지 마.

공식 문서:
https://developers.openai.com/api/docs/guides/decisions

1. 기존 확률 처리 진단

predicate 확률이 0 또는 1로만 표시된다면 다음을 확인해 줘.

- 실제 API 응답의 answers[].probability
- 서버의 응답 추출 과정과 브라우저 표시 과정
- round, parseInt, 정수·Boolean 변환 여부
- 기준값 비교 결과를 probability 대신 표시하는지

API가 실제로 0 또는 1을 반환했다면 정상 결과로 인정해 줘.
중간값을 만들기 위한 수치 보정이나 가짜 확률은 금지한다.
확률은 API의 원래 숫자값을 보존하고, 표시할 때 반올림하지 마.
기존 구현이나 통신 기록이 없으면 과거 문제의 원인을 추측해서 확정하지 마.

2. 생산라인 감시

line-sim/API_GUIDE.md를 읽고 실제 경로와 파라미터를 따라 줘.

- [감시 시작]을 누르면 POST /api/reset에 {"play": true}를 보내 처음부터 재생한다.
- 브라우저가 2초마다 /api/events를 조회한다.
- since와 run_id를 사용해 새 이벤트만 가져온다.
- 동일한 seq는 중복 판정하지 않는다.
- 이벤트 조회와 Decisions 처리는 별도로 동작한다.
- 새 이벤트는 순서대로 대기열에 넣는다.
- Decisions 호출은 동시에 1건만 실행한다.
- 자동·수동 호출을 합쳐 호출 시작 간격을 최소 3초로 유지한다.
- 감시는 최대 180초에 자동 종료한다.
- 종료 후 대기열의 새 판정 호출을 시작하지 않는다.
- 이미 시작한 요청은 완료될 수 있으며 결과를 표시한다.
- 종료 시 남은 이벤트는 미호출 상태로 표시한다.

감시는 브라우저가 주도한다. 서버의 자율 반복 감시, 별도 중지 버튼, heartbeat, 브라우저 생존 확인 기능은 만들지 마.
서버에서도 기한을 확인해 대기 중이던 자동 요청이 180초 이후 새 OpenAI 호출을 시작하지 않게 해 줘.

3. Decisions API

서버에서 다음 API를 호출해 줘.

- Method: POST
- Endpoint: https://api.openai.com/v1/decisions
- Model: gpt-6-luna
- API Key: 기존 .env의 OPENAI_API_KEY
- Question type: predicate
- Question name: needs_investigation

questions의 instructions는 다음 문구를 사용해 줘.

“현재 이벤트에 새롭게 조사할 필요가 있는 품질 이상 징후가 있는가? 정상적인 공정 시작·종료 및 관리 범위 내의 측정값은 조사 대상으로 판단하지 않는다. 제공된 이벤트의 정보만 평가하고 미래 이벤트를 추측하지 않는다.”

input에는 해당 이벤트의 원본 정보 전체와 교육용 합성 데이터라는 설명을 포함해 줘.

응답 answers에서 name이 needs_investigation인 항목을 찾고, type이 predicate인지 확인한 후 probability를 추출해 줘.

HTTP 오류, refusal, 응답 형식 오류, 네트워크 오류는 구분해 표시한다. 실패를 0이나 다른 확률로 대체하지 마.
자동 재시도로 추가 호출을 만들지 마.

브라우저가 OpenAI API에 직접 접근하지 않도록 해 줘.
API 키·인증 헤더는 화면이나 로그에 노출하지 마.

4. 실제 Request / Response 확인

이벤트를 선택하면 해당 이벤트와 연결된 실제 통신 기록을 보여줘.

A. 생산라인 이벤트 API
- Request: HTTP Method, 실제 URL, Query Parameters
- Response: HTTP Status, 실제 수신 JSON

B. OpenAI Decisions API
- Request: HTTP Method, Endpoint, 실제 전송 JSON 전체
- Response: HTTP Status, 실제 수신 JSON

Request에서 model, input, questions, type, name, instructions를 확인할 수 있어야 한다.
Response에서 answers와 probability의 원래 값을 확인할 수 있어야 한다.

실제로 보낸 요청 객체와 실제로 받은 응답을 기록해 줘.
가상의 예시 JSON을 만들어 표시하지 마.
usage 정보만 화면에서 제외하고, 생략 사실을 표시해 줘.
각 JSON은 단순한 코드 블록으로 표시하고 복사 버튼을 제공해 줘.

5. 최소 화면

상단:
- [감시 시작]
- 경과 시간과 감시 상태

이벤트 목록:
- seq
- 장비
- 이벤트 내용
- 조사 필요 확률(probability)
- 판정 상태

이벤트 상세:
- 생산라인 API Request / Response
- Decisions API Request / Response

기준값은 0.5다. probability가 0.5 이상이면 ‘조사 대상’으로 표시하되, 확률 자체는 변경하지 마.

별도 대시보드·차트·애니메이션·복잡한 카드 UI는 만들지 마.
조사 Agent, 전문 Agent, 멀티에이전트 호출은 구현하거나 연결하지 마.

6. API 단독 테스트

선택한 이벤트의 input을 편집하는 입력란과 [Decisions 테스트] 버튼을 추가해 줘.

- 버튼을 누르면 편집한 input으로 API를 정확히 1회 호출한다.
- 실제 Request와 Response, probability를 바로 표시한다.
- 원래 이벤트 데이터와 자동 감시의 판정 결과는 변경하지 않는다.
- 테스트 결과에는 어느 seq에서 시작한 테스트인지 표시한다.
- 자동 호출과 같은 단일 실행·최소 3초 시작 간격 제한을 적용한다.
- 감시 종료 후 사용자가 명시적으로 누른 수동 테스트는 별도 1회 호출로 허용한다.

정상 이벤트, 명확한 이상 이벤트, 판단이 애매한 이벤트를 비교할 수 있어야 한다.
choice·score를 위한 UI는 추가하지 마.

7. 실제 검증

기존 키로 실제 API를 호출하여 다음을 검증해 줘.

- 이벤트 조회가 약 2초 간격인가?
- Decisions 호출이 동시에 1건이며 시작 간격이 최소 3초인가?
- 동일 seq를 중복 판정하지 않는가?
- 공식 규격의 JSON을 실제로 전송하는가?
- HTTP 상태와 실제 응답 JSON을 확인·복사할 수 있는가?
- API 원본 probability와 화면 표시 값이 일치하는가?
- 수동 input 수정이 실제 요청에 반영되는가?
- 수동 테스트가 원래 이벤트와 판정을 보존하는가?
- 180초에 자동 종료하고 이후 새 자동 호출을 시작하지 않는가?

실제 API 검증과 모의 응답을 사용한 오류 분기 시험을 구분해서 보고해 줘.
0/1 또는 중간값 중 특정 결과가 나오도록 강제하지 마.

완료 후 변경 파일, 실행 주소, 실제 테스트 결과, 확률 문제의 확인된 원인과 미확인 사항을 간단히 보고해 줘."""
PL = PROMPT.split("\n")


def chunk(a, b):
    return "\n".join(PL[a:b]).strip("\n")


def pchunk(title, a, b, no, sub=""):
    box = prompt(chunk(a, b), f"[Claude Code] 완성형 Prompt · {no}/7", sm=True).replace('class="code prompt sm"', 'class="code prompt sm c2"', 1)
    return page(title, box, kick="실습 2 · 완성형 Prompt", sub=sub, top=True)


def full_prompt():
    parts = ["1 기존 확률 처리 진단", "2 생산라인 감시", "3 Decisions API", "4 실제 Request / Response 확인",
             "5 최소 화면", "6 API 단독 테스트", "7 실제 검증"]
    s = " · ".join(f"<b>{p.split(' ', 1)[0]}</b> {p.split(' ', 1)[1]}" for p in parts)
    return (f'<div class="code prompt full"><div class="bar"><span class="plabel">[Claude Code] 완성형 Prompt 전체 · 복사 후 그대로 붙여 넣기</span></div>'
            f'<div class="fsum">{s}</div><pre><code>{esc(PROMPT)}</code></pre></div>')


def opening():
    return [
        cover(["Multi-Agent", "<em>Decisions</em>와 조사 Agent"],
              "자주 하는 판정과 비용이 큰 조사를 나누고, 판단과 실행을 잇는 기본 흐름을 만듭니다",
              [("교시", "6교시"), ("실습", "line-sim · agent-sim [decisions] 탭"), ("API", "OpenAI Decisions · Responses")], "6교시"),
    ]


def block_patterns():
    return [
        section("01", "멀티에이전트의 구성 방식과 설계 요소", "Agent 사이의 연결 → 도구와 사람 개입의 통제"),
        page("역할 분리 기준", two(
            pane("Agent 하나", ul(["모든 일을 한 Agent가", "Context · Tool이 계속 늘어남", "잘못된 판단이 다음 단계로 전달"]), "bad"),
            pane("역할별 Agent", ul(["Agent마다 맡는 <b>범위를 좁힘</b>", "필요한 <b>Context와 Tool을 구분</b>", "역할마다 다른 구성"]), "good"))
             + note("먼저 정할 두 가지", "① Agent 사이의 작업을 <b>어떻게 연결</b>할지 → ② 도구와 사람의 개입을 <b>어떻게 통제</b>할지", "red"), kick="설계 요소"),
        page("순차 실행 · Sequential", sf.sequential(), kick="1-1 · 연결 방식"),
        page("병렬 실행과 집계 · Aggregator", sf.aggregator(), kick="1-1 · 연결 방식"),
        page("계층형 · Hierarchical", sf.hierarchical()
             + note("상위 Agent", "작업을 나눠 맡기고 결과를 받아 정리 · 요청에 따라 <b>필요한 하위 Agent만 선택</b> 가능 · 하위마다 역할 · Context · Tool을 다르게", "red"),
             kick="1-1 · 연결 방식"),
        page("도구 공유 · Shared Tools", sf.shared_tools()
             + note("핵심", "모든 Agent에게 모든 Tool이 아니라 <b>각 역할에 필요한 Tool만 허용</b> · 5교시 MCP 서버가 같은 규격의 도구 제공", "red"),
             kick="1-2 · 운영 방식"),
        page("사람 개입 · Human-in-the-loop", sf.hitl()
             + note("같은 구조", "Claude Code가 실행 전에 권한을 묻는 것 · 조회는 바로 · 삭제 · 전송은 승인 뒤", "red"), kick="1-2 · 운영 방식"),
    ]


def block_split():
    return [
        section("02", "판정과 조사 분리", "Decisions API가 고르고, 조사 Agent가 설명"),
        page("이번 실습의 구조", vizanim.decide_investigate()
             + note("나누는 이유", "판정 13회 · 빠르고 저렴 → 조사 4회 · 도구 호출 · 느리고 비쌈 · 확률은 설명용", "red"),
             kick="판정과 조사"),
        page("predicate의 추정 대상", two(
            pane("이 실습의 조건", ul(["「제공한 이벤트에 <b>추가 조사가 필요한 이상 징후</b>가 있는가」",
                                     "조건을 만족할 가능성을 <b>0~1</b>로 추정"]), "good"),
            pane("확률이 아닌 것", ul(["실제 공정의 <b>불량 발생률</b>을 측정한 값 아님", "같은 입력에서도 추정값은 달라질 수 있음"]), "bad"))
             + note("조사 필요 확률", "조건에 대한 모델의 추정값"), kick="Decisions"),
        page("Decisions API의 세 가지 답", cards([
            ("predicate", "조건이 참일 추정 확률 (0~1)<br>이번 실습 · 새롭게 조사할 이상 징후가 있는가", "판정"),
            ("choice", "미리 정한 선택지 중 하나<br>예 · 문의를 어느 부서로 보낼지", "선택"),
            ("score", "순서가 있는 평가 단계의 확률 가중 평균<br>예 · 심각도를 단계별 기준으로", "점수"),
        ]) + note("짧은 판정값", "텍스트 · 이미지 입력을 평가해 정해진 유형의 답 · 앱이 바로 분기할 수 있음", "red"), kick="2-1 · Decisions"),
        page("요청과 응답의 구조", two(
            prompt('POST https://api.openai.com/v1/decisions\n\n{\n  "model": "gpt-6-luna",\n  "input": "이벤트 원본 정보 + 교육용 합성 데이터 설명",\n'
                   '  "questions": [\n    {\n      "type": "predicate",\n      "name": "needs_investigation",\n      "instructions": "현재 이벤트에 새롭게 조사할 …"\n    }\n  ]\n}',
                   "Request · 구조 개요", sm=True),
            prompt('{\n  "answers": [\n    {\n      "name": "needs_investigation",\n      "type": "predicate",\n      "probability": (API가 돌려준 원래 숫자)\n    }\n  ]\n}',
                   "Response · 구조 개요", sm=True)
            + ul(["answers에서 질문의 <b>name</b>으로 결과 찾기", "<b>probability</b>를 화면에 표시", "앱의 기준값과 비교"]))
             + note("실제 JSON", "실습 화면의 Request / Response 기록에서 확인 · 값은 예시로 만들지 않음"), kick="2-1 · Decisions"),
        page("공식 문서 기준", big([("POST /v1/decisions", "공개 베타 · 모델 gpt-6-luna"), ("약 10배", "Responses API 대비 속도 · 문서 소개"),
                                 ("$0.10", "입력 100만 토큰당 기본 요금 · 출력 토큰 요금 없음")])
             + note("주의", "우리 실습의 측정 결과가 아님 · 처리 지역 · 긴 입력의 가산 조건은 공식 문서 확인", "red")
             + note("출처", f'OpenAI Decisions 공식 가이드 (2026-10-13 확인) · <code>{DOC}</code>'), kick="2-1 · Decisions"),
        page("N회 판정 + M회 조사", sf.cost()
             + note("판정 뒤", "도구 호출과 설명이 필요하면 <b>Responses API</b>를 쓰는 조사 Agent로 · 기준값이 조사 횟수와 놓치는 이벤트에 주는 영향 확인", "red"),
             kick="비용 구조"),
        page("판정 → 조사 흐름", sf.decision_flow(), kick="전체 흐름"),
        ill("scenes_ch2", "gauges", "top20", "기준값 0.5",
            ["추정값 ≥ 기준값 → 이벤트마다 조사 Agent", "낮추면 조사 대상 · 비용 증가 · 높이면 놓칠 수 있음"]),
    ]


def block_line():
    return [
        section("03", "모의 생산라인 켜기", "판정할 이벤트를 공급하는 서버부터"),
        lab("1", "모의 생산라인 실행", "판정할 이벤트를 공급하는 line-sim 서버를 켜고 데이터와 이벤트 API 확인",
            ["line-sim 폴더의 파일 확인", "run_line.bat 실행 · 서버 창 유지", "브라우저에서 재생 조작", "이벤트 API 열어 JSON 확인"],
            "8800번에서 동작하는 모의 생산라인"),
        page("서버 실행", two(
            steps([("폴더 이동", "<code>samsung-ds-btrack</code> 하단의 <b>line-sim</b> 폴더"),
                   ("파일 확인", "<code>run_line.bat</code> · <code>server.py</code> · <code>timeline.json</code> · <code>maintenance.json</code>"),
                   ("실행", "<code>run_line.bat</code> 실행 · 서버 창은 그대로")]),
            prompt("cd C:\\samsung_ds_YYYYMMDD\\line-sim\n.\\run_line.bat", "[PowerShell] 명령으로 실행하는 경우")
            + prompt("http://127.0.0.1:8800/", "[브라우저] 주소창"), "w")
             + note("준비물", "서버와 고정된 합성 데이터 포함 · Python 외 추가 패키지 · API 키 불필요"), kick="실습 1"),
        page("재생 조작", table(["화면 · 버튼", "동작"], [
            ["<b>처음</b>", "대기 상태 · 이벤트 한 개"],
            ["<b>[재생 시작]</b>", "3분 동안 13개 이벤트 공개"],
            ["<b>[끝까지 보기]</b>", "나머지 즉시 공개"],
            ["<b>[처음부터]</b>", "재생 초기화"],
        ]), kick="실습 1"),
        page("LOT-001 경로", flow([
            ("EQ-A", "박막 증착 · 챔버 CH1 · CH2"), ("EQ-B", "열처리"), ("MET", "막 두께 계측"), ("VIS", "비전 검사"),
        ]) + note("합성 데이터", "교육용으로 만든 이름 · 수치 · 실제 공정의 물리적 인과관계를 재현하지 않음", "red")
             + note("보는 법", "이벤트 · 정비 기록만으로 원인 확정 X → <b>확인할 가설 · 추가 점검 사항</b> 찾기"), kick="3-2 · 데이터"),
        page("이벤트 API 열기", two(
            prompt("http://127.0.0.1:8800/api/events?since=0", "[브라우저] 이벤트 API"),
            ul(["5교시 API처럼 주소 요청 → <b>JSON</b> 응답", "이번에는 <b>내 PC의 서버</b>가 데이터 제공", "서버 창은 실습이 끝날 때까지 켜 두기"]), "w"), kick="3-2 · 데이터"),
    ]


def block_decisions():
    return [
        section("04", "이벤트 감시와 Decisions 판정", "완성형 Prompt로 [decisions] 탭 만들기"),
        lab("2", "[decisions] 탭 만들기", "생산라인 이벤트를 감시하고 Decisions API로 조사 필요 확률을 판정하는 화면",
            ["agent-sim 폴더에서 Claude Code 열기", "완성형 Prompt 전체 복사 · 붙여 넣기", "[decisions] 탭에서 [감시 시작]", "확률 · Request / Response 확인"],
            "이벤트별 조사 필요 확률과 실제 통신 기록"),
        page("시작 전 확인", two(
            ul(["기존 <b>agent-sim</b> 폴더에서 Claude Code 열기", "4 · 5교시 .env의 <b>OPENAI_API_KEY</b> 그대로 사용",
                "모의 서버에는 키를 넣지 않음", "<code>http://127.0.0.1:8800/</code> 모의 서버는 켜 둔 채로"]),
            pane("구현 참고 · OpenAI Decisions 공식 문서", f'<p style="font-size:16px;margin:0;word-break:break-all"><code>{DOC}</code></p>'
                 '<p style="font-size:15px;color:var(--ink-soft);margin:10px 0 0">Prompt 안에 주소 포함 · 함께 전달</p>', "good"), "w"), kick="4-1"),
        page("완성형 Prompt 구성", full_prompt()
             + note("붙여 넣기", "위 상자의 <b>복사</b> → Claude Code에 그대로", "red")
             + note("핵심 조건", "실제 API 호출 · 실제 Request / Response 기록 · 가짜 확률 · 가상 JSON 금지 · 조사 Agent는 아직 연결하지 않음"),
             kick="4-1 · 완성형 Prompt"),
        page("감시와 판정의 분리", sf.lanes()
             + note("종료", "감시는 최대 180초 · 종료 후 새 판정 호출 없음 · 이미 시작한 요청은 완료 · 남은 이벤트는 <b>미호출</b> 표시", "red"),
             kick="4-1 · 동작 구조"),
        page("[decisions] 탭의 최소 화면", two(sf.wire(),
             ul(["probability ≥ 0.5 → <b>조사 대상</b> 표시", "확률 자체는 변경하지 않음", "usage만 제외 · 생략 사실 표시", "대시보드 · 차트 · 애니메이션 없음"]), "w"), kick="4-1 · 화면 구성"),
        page("만들어진 화면 확인", steps([
            ("탭 열기", "Claude Code가 안내한 주소 → <b>[decisions]</b> 탭 · 열리지 않으면 실제 오류와 주소를 알려 수정"),
            ("[감시 시작]", "이벤트가 한 줄씩 늘어나고 줄마다 조사 필요 확률이 채워짐"),
            ("처리 상태", "대기 수 · 완료 수 · 호출 수 · 시작 시각 · 앞 요청이 길면 간격도 길어짐"),
            ("[끝까지 보기]", "모의 서버 화면에서 누르면 나머지 이벤트가 한꺼번에"),
        ]), kick="4-2 · [앱 화면]"),
        page("판정 읽기", two(
            pane("확인할 것", ul(["predicate의 조건과 <b>실제 입력</b> → 「조사 필요」의 뜻", "어느 이벤트의 확률이 높은지",
                                "공정 종료 · 관리 범위 안의 측정값은 몇으로 나왔는지"]), "good"),
            pane("이상 신호", ul(["정상적인 시작 · 종료만으로 조사 대상", "아직 일어나지 않은 이벤트를 추측", "판정 실패 · refusal을 <b>0으로 표시</b>"]), "bad"))
             + note("추정값", "API의 추정값이라 실행할 때마다 조금씩 다를 수 있음"), kick="4-2 · 판정 확인"),
        page("감시의 수명과 중지", two(
            ul(["탭을 닫는 순간의 즉시 중지는 모든 환경에서 보장 불가", "서버: 마지막 생존 확인(heartbeat) 후 <b>10초</b>가 지나면 감시 만료",
                "이미 전송한 API 1건은 완료될 수 있음", "만료 · 중지 뒤에는 새 판정 · 후속 조사 시작 없음"]),
            pane("[직접 확인]", ul(["감시 중 agent-sim 탭 닫기", "서버 로그: 중지 사유 · 시각 · 마지막 API 호출 시각", "다시 열면 <b>중지 상태</b>",
                                   "이어서 실습: [감시 시작] 다시"]), "good"), "w"), kick="4-2 · 실행 수명"),
    ]


def block_agent():
    return [
        section("05", "기준값을 넘으면 조사 Agent 호출", "판정 입력을 그대로 넘기고 도구로 조회"),
        lab("3", "조사 Agent 연결", "기준값을 넘은 이벤트를 조사 Agent에 넘기고, Agent가 도구로 Lot 이력과 정비 기록을 조회하게 하기",
            ["가이드라인 · 키워드 읽기", "실습 조건 확인", "요청문 직접 작성 · 같은 창", "새로고침 후 [감시 시작]"],
            "이벤트 행 아래 조사 결과와 도구 호출 기록"),
        page("Prompt 작성 가이드라인", two(
            pane("기준값과 조사 Agent 연결", ul([
                "어떤 조건에서 조사하고, Agent에게 <b>어떤 Context와 도구</b>를 줄지",
                "판정 입력을 조사로 이어 주는 흐름",
                "조사 결과의 <b>근거 · 표시 방식</b>",
                "같은 이벤트의 <b>반복 호출을 막을 조건</b>",
                "탭 종료 · 감시 중지 후 조사도 새로 시작하지 않도록 <b>실행 수명</b> 연결"]), "good"),
            '<div class="lh" style="font-weight:800;color:var(--mut);font-size:14px">키워드</div><div class="kws">'
            + "".join(f"<span>{k}</span>" for k in ["기준값 0.5", "판정 입력 그대로", "조회 도구", "근거 ID", "도구 기록", "중복 방지", "감시 run_id", "중지/만료"])
            + "</div>" + note("작성 위치", "[Claude Code · Prompt 직접 작성] 같은 창", "red"), "w"), kick="5-1 · 요청 작성"),
        page("실습 조건 확인", table(["항목", "조건"], [
            ["<b>호출 조건</b>", "조사 필요 확률이 기준값 이상인 이벤트 · 기준값 입력칸 · 기본값 0.5"],
            ["<b>전달 Context</b>", "해당 이벤트 + Decisions API에 보냈던 입력 전체를 그대로"],
            ["<b>조사 실행</b>", "기존 Responses API 호출 코드 · 모델 재사용 · 감시 소유자 · run_id · 중지/만료 상태 공유"],
            ["<b>도구 범위</b>", "모의 서버의 조회 API만 · Lot 이력 · 이벤트 · 정비 기록"],
            ["<b>결과</b>", "원인 가설 · 근거(이벤트 seq, 정비 기록 ID) · 추가 확인 사항 · 짧은 한국어"],
            ["<b>화면 · 중복</b>", "이벤트 행 아래 펼쳐 표시 · 호출 도구와 인자도 · 같은 이벤트 중복 조사 금지"],
        ]) + note("실행 수명 확인 시점", "조사 시작 · 각 모델 / 도구 호출 · 재시도 직전 · 종료한 실행의 늦은 판정 결과로 조사 시작 X", "red"),
             kick="5-1 · 실습 조건"),
        page("조사 결과 확인", two(
            steps([("새로고침", "브라우저 새로고침 → <b>[감시 시작]</b> 다시"),
                   ("결과", "기준값 이상인 이벤트 → 그 행 아래 조사 결과"),
                   ("펼침", "Agent가 <b>어떤 도구를 어떤 인자로</b> 불렀는지")]),
            pane("보고가 하나도 없다면", ul(["표시된 확률과 판정 조건 확인", "연결 동작을 볼 때는 기준값을 낮춰 다시 시작",
                                          "이 조정만으로 업무에 맞는 기준값을 찾았다고 판단하지 않음"]), "bad"), "w"), kick="5-1 · [앱 화면]"),
    ]


def block_check():
    return [
        section("06", "연결된 동작 확인", "이벤트 → 판정 → 기준값 초과 → 도구 조회 → 조사 결과"),
        page("확인 장면", steps([
            ("판정", "Decisions가 이벤트마다 판정한 확률이 표에"),
            ("연결", "기준값을 넘은 이벤트와 그 판정 입력이 조사 Agent의 입력에"),
            ("도구 호출", "Lot 이력 · 정비 기록 조회 같은 도구 호출"),
            ("조사 결과", "조회 결과를 읽은 뒤 원인 가설 · 추가 확인 사항"),
        ]), kick="6 · 확인"),
        ill("scenes_extra", "fact_hypothesis", "left40", "기록 발견 ≠ 원인 확정",
            ["정비 기록을 찾았다 ≠ 원인을 확정했다", "근거로 쓴 이벤트 · 기록 확인", "더 확인해야 할 사항 읽기"]),
    ]


def closing():
    return [
        page("막히면 확인", table(["증상", "확인"], [
            ["<b>서버가 켜지지 않음</b>", "Python과 이전 서버 창 · 포트 사용 중이면 이전 line-sim 창 닫기"],
            ["<b>이벤트가 안 보임</b>", "브라우저에서 8800번 모의 서버가 열리는지"],
            ["<b>Decisions 권한 · 모델 오류</b>", "오류 상태 확인 → 강사에게 · API 키 자체를 채팅에 붙이지 않기"],
            ["<b>429 또는 잔액 오류</b>", "감시 멈추고 오류 안내에 따라 재시도 · 잔액 · 프로젝트 한도는 강사와"],
            ["<b>조사가 시작되지 않음</b>", "판정 조건과 확률 열 · 기준값 이상이 없으면 연결 확인용으로 기준값 낮추기"],
            ["<b>조사에서 도구를 안 씀</b>", "도구 호출 기록 → 도구 등록과 지침을 Claude Code에 확인시키기"],
            ["<b>연결 확인 만료로 멈춤</b>", "백그라운드 · 절전 · 통신 끊김으로 heartbeat 지연 · 다시 열어 중지 사유 확인 → [감시 시작] · 자동으로 되살리지 않음"],
        ], "s6trb"), kick="7 · 문제 해결"),
        page("정리", steps([
            ("연결 방식", "순차 · 병렬과 집계 · 계층형 → 일의 의존 관계로 선택"),
            ("운영 방식", "역할별로 필요한 Tool만 · 되돌릴 수 없는 행동은 사람 승인"),
            ("판정과 조사 분리", "Decisions predicate로 N회 판정 · 기준값 이상만 M회 조사"),
            ("앱과 Agent의 경계", "호출 조건 · 실행 수명은 앱 · 조회할 도구와 내용은 Agent"),
        ])),
        section("다음", "7교시 · 캡스톤 1", "기획과 제작"),
    ]


def slides():
    return opening() + block_patterns() + block_split() + block_line() + block_decisions() + block_agent() + block_check() + closing()
