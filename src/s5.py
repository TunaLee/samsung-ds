"""5교시 · AI Agent · MCP로 RAG와 외부 도구 연결 (원본: 노션 교안 5교시)."""
import fig
import s5_fig as f5
from kit import (big, cards, cover, flow, img, lab, note, page, pane, prompt, section, steps, table, two, ul)

TITLE = "AI Agent · MCP로 RAG와 외부 도구 연결"
IMG = "img/s5/"
SP = '<div class="sp5"></div>'
SPS = '<div class="sp5 s"></div>'


def opening():
    return [
        cover(["MCP로 <em>RAG</em>와", "외부 도구 연결"],
              "rag-sim의 검색을 Tool · MCP 서버로 내놓고, agent-sim이 도구로 골라 쓰는 흐름을 확인합니다",
              [("교시", "5교시"), ("실습", "rag-sim · agent-sim · Claude Code"), ("연결", "Microsoft Learn MCP · rag_search MCP")], "5교시"),
    ]


def block_api():
    return [
        section("01", "API", "도구가 바깥 서비스에 요청하는 약속 · 주소 · 조건 · 응답"),
        page("API: 약속된 방식으로 소통하는 접점", f5.api_fig()
             + note("API", "Application Programming Interface · 요청할 기능 · 보낼 값 · 결과 형식을 정해 둠", "red")
             + note("웹 API", "주소로 요청 → JSON 같은 데이터 형식으로 결과 · 안의 구현은 몰라도 형식만 맞추면 됨"), kick="API"),
        page("GET 요청: 주소창에 Enter", prompt("https://api.frankfurter.app/latest?from=USD&to=KRW,JPY,CNY", "[브라우저] 주소창") + SP
             + table(["부분", "뜻"], [
                 ["<code>…/latest</code>", "요청할 주소 · 가장 최근에 고시된 환율"],
                 ["<code>?</code>", "뒤에 요청 조건 · 여러 조건은 <code>&amp;</code>로 연결"],
                 ["<code>from=USD</code>", "1달러 기준"],
                 ["<code>to=KRW,JPY,CNY</code>", "원화 · 엔화 · 위안화로 환산"],
                 ["<code>2026-08-01..2026-09-03</code>", "<code>latest</code> 자리에 기간 → 날짜별 값"]])
             + note("GET", "바꾸지 않고 <b>받아 오기만</b> 하는 요청 · 오늘은 이것부터"), kick="API"),
        page("응답 읽기", img(IMG + "frankfurter.png", "브라우저에 돌아온 응답 · rates 안의 KRW가 1달러의 원화 값", light=True)
             + table(["항목", "뜻"], [
                 ["<code>rates.KRW</code>", "1달러를 원화로 환산한 값"],
                 ["<code>date</code>", "환율 고시일"],
                 ["갱신", "유럽중앙은행 고시 환율 · 하루 한 번 · 주말엔 새 값 없음"]])
             + note("응답", "사람이 보는 화면이 아니라 <b>프로그램이 읽고 처리하는 데이터</b>"), kick="API"),
        page("도구 안의 API 호출", f5.chain([
            ("model", "LLM", "「환율 조회 도구를<br>USD로 불러 줘」", False),
            ("window", "앱", "환율 조회<br>함수 실행", False),
            ("globe", "Frankfurter API", "함수 안에서 호출<br>→ 결과", True),
            ("window", "앱", "결과를<br>LLM에 전달", False),
            ("chat", "LLM", "답변 작성", False),
        ]) + note("API 없는 Tool", "4교시의 메모 도구처럼 외부 API를 쓰지 않는 Tool도 있음"), kick="API"),
    ]


def block_mcp():
    return [
        section("02", "MCP: 도구를 연결하는 표준", "목록 조회 · 호출 · 결과 전달의 공통 규격"),
        page("규격 없는 연결", two(
            pane("규격이 없으면", ul(["메일 · 문서 저장소 · 지도 · 업무 시스템마다 <b>요청 형식 · 인증</b>이 다름",
                                    "같은 문서 검색도 AI 앱이 바뀔 때마다 목록 전달 · 결과 반환 코드를 새로",
                                    "→ 유지보수가 복잡"]), "bad"),
            pane("MCP (Model Context Protocol)", ul(["Anthropic · 2024년 11월 공개",
                                                    "서버와 앱이 <b>목록 조회 · 호출 · 결과 전달</b> 형식을 맞춤",
                                                    "→ 같은 연결 부분을 반복해서 만들 필요가 줄어듦"]), "good"))
             + note("없애 주지 않는 것", "각 서비스의 API와 인증 · 서버 개발자가 서비스 연결 코드를 구현", "red"), kick="MCP"),
        page("MCP 서버와 MCP 클라이언트", '<div class="parts">'
             + fig._tile("plug", "MCP 서버", "약속에 맞춰<br>도구를 <b>제공</b>하는 프로그램")
             + '<div class="plus">⇄</div>'
             + fig._tile("rule", "MCP", "어떤 순서로 무엇을 주고받을지<br>정한 <b>규격(표준)</b>", "core")
             + '<div class="plus">⇄</div>'
             + fig._tile("window", "MCP 클라이언트", "그 도구를 가져다 <b>쓰는</b><br>AI 앱 쪽 기능")
             + "</div>" + note("오늘 순서", "이미 만들어진 서버 연결 → 직접 서버 만들기"), kick="MCP"),
        page("MCP 서버가 하는 두 가지 일", '<div class="parts">'
             + fig._tile("rule", "도구 목록 보내기", "앱이 물으면 도구의<br>이름 · 설명문 · 입력 형식<br><code>tools/list</code>")
             + fig._tile("bolt", "도구 호출 처리하기", "「이 도구를 이 인자로 실행해 줘」<br>→ 실제 실행 · 결과 반환<br><code>tools/call</code>", "core")
             + "</div>" + note("주소", "문서를 읽는 웹페이지 주소 ≠ MCP 요청을 받는 주소 <code>https://learn.microsoft.com/api/mcp</code>"), kick="MCP"),
        page("등록 · 호출 순서", f5.mcp_seq()
             + note("통신 주체", "MCP 서버와 통신하는 것은 <b>앱의 MCP 클라이언트</b> · 서버 구현 코드는 서버에 남음", "red"), kick="MCP"),
        page("Microsoft Learn 서버 연결", two(
            prompt("https://learn.microsoft.com/api/mcp", "[MCP] 탭 · MCP 서버 주소") + SP
            + ul(["agent-sim 실행 → <b>[MCP]</b> 탭 · 처음엔 서버 목록이 비어 있음",
                  "주소 입력 → <b>[추가하고 연결]</b>",
                  "왼쪽 서버 목록: learn.microsoft.com · 연결 상태",
                  "오른쪽 도구 목록: <b>내장 메모 도구 vs 새 MCP 도구</b> 구분"]),
            pane("Microsoft Learn MCP", ul(["Microsoft가 운영하는 <b>공개 문서 검색</b> 서버", "별도 API 키 없음",
                                           "내 학습 이력 · 회사 내부 문서는 읽지 않음"]), "good")
            + note("주의", "목록에 저장돼도 연결은 실패할 수 있음 · 오류 문구와 도구 목록을 함께", "red"), "w"), kick="MCP 실습"),
        page("공통 질문으로 실제 검색 확인", prompt("Microsoft Learn에서 PowerShell의 현재 폴더를 확인하는 명령을 찾아 설명하고 출처를 보여 줘.", "[도구] 탭 · 앱 질문 입력칸") + SP
             + ul(["하단 <b>API 호출 내역</b>: Microsoft 문서 검색 도구의 호출 · 반환값 · 출처 주소",
                   "<b>연결 표시 ≠ 실제 검색 실행</b>",
                   "답변의 출처 주소를 열어 원문 확인"]), kick="MCP 실습"),
        page("연결 확인 순서", steps([
            ("[MCP]", "주소 · 연결 상태"),
            ("[앱에 연결된 도구]", "제공 서버 · 이름 · 설명"),
            ("[도구]", "공통 질문 실행"),
            ("API 호출 내역", "선택된 도구 · 입력 인자 · 반환 출처 대조"),
            ("출처 원문", "답변의 출처 주소 열기"),
        ]) + note("구분", "목록 조회와 실제 도구 실행은 <b>서로 다른 단계</b>", "red"), kick="MCP 실습"),
        page("연결 실패와 연결 해제", two(
            pane("연결이 실패하면", ul(["<code>https://</code> · 끝의 <code>/api/mcp</code> · 공백", "인터넷 접속 · 화면 오류 순서로 확인",
                                       "브라우저로 열어 <b>405</b> → 웹페이지 GET과 MCP 연결 요청이 다르기 때문일 수 있음",
                                       "주소 · 오류 문구 · 발생 단계 기록 → 앱 안에서 다시 연결"]), "bad"),
            pane("연결 해제 비교", ul(["<b>[연결 끊기]</b> → 서버 주소는 왼쪽 목록에 남는지",
                                      "해당 서버의 도구는 오른쪽 목록에서 빠지는지",
                                      "다시 <b>[연결]</b> → 다음 실습",
                                      "내장 메모 도구 · 다른 서버 도구는 따로 구분"]), "good")), kick="MCP 실습"),
        page("MCP 클라이언트 코드 읽기", f5.guide(
            ["MCP 연결 · 목록 · 호출이 코드 어디에 있는지"],
            ["initialize", "tools/list", "tools/call"],
            [("읽을 파일", "lab/mcp_client.py · lab/registry.py"), ("범위", "코드 수정 없이 읽고 설명받기")], "agent-sim 폴더"), kick="Claude Code"),
    ]


def block_mcp_lab():
    return [
        section("03", "실습 1 · rag-sim 검색 MCP 서버", "rag-sim 검색을 부르는 Tool → MCP 서버 → agent-sim"),
        page("오늘 만들 전체 구성", f5.arch()
             + note("관리 탭", "rag-sim에 <b>[MCP 관리]</b> 탭 하나 · MCP 서버 On/off와 호출 로그를 같은 화면에서"), kick="실습 1"),
        page("주소와 포트", two(
            ul(["<code>127.0.0.1</code> = 내 컴퓨터 자신 · <code>localhost</code>와 같은 뜻",
                "이 주소로 보낸 요청은 밖으로 나가지 않고 내 PC 안에서 처리",
                "<code>:8765</code> 같은 숫자 = <b>포트</b> · 한 컴퓨터의 여러 서버를 번호로 구분"]),
            table(["포트", "서버"], [
                ["<b>8765</b>", "rag-sim 관리 화면 (유지)"], ["<b>8770</b>", "agent-sim (유지)"],
                ["<b class='hl'>8790</b>", "새 MCP 서버"]]))
             + note("분리 이유", "MCP 서버를 꺼도 관리 화면에서 다시 켤 수 있도록 화면 서버와 포트 분리", "red"), kick="로컬 서버"),
        page("내 PC에서만 접근하는 서버", two(
            pane("127.0.0.1 바인딩", ul(["내 PC에서 접근", "로컬 실행 여부 ≠ 외부 접근 허용 · 서로 다른 설정", "옆자리에서 같은 주소를 넣으면 <b>자기 PC</b>를 가리킴", "사내 문서를 다루는 기능의 통제에 유리"]), "good"),
            pane("외부에서 접근하게 하려면", ul(["방화벽 · 공개 설정을 따로", "그때부터 <b>누가 접근할 수 있는지</b>가 설계 결정"]), "bad")), kick="로컬 서버"),
        lab("1", "MCP 서버를 만들어 agent-sim에 연결", "rag-sim 검색을 부르는 rag_search Tool을 MCP 규격으로 제공하고, agent-sim이 도구로 골라 쓰는지 확인",
            ["rag_search Tool 만들기 (3-1)", "MCP 서버 · 관리 탭에서 On/off (3-2)", "agent-sim의 주소 등록 흐름 읽기 (3-3)", "rag-sim MCP 주소 등록 (3-4)", "반도체 질문 · PowerShell 질문 (3-5)"],
            "8790번 MCP 서버 · agent-sim 도구 목록의 rag_search"),
        page("rag_search Tool · 요청 작성", f5.guide(
            ["rag-sim 기존 검색을 어떻게 불러 쓸지", "어떤 질문에 쓰는 도구인지 설명문에"],
            ["rag_search", "question · top_k", "tools/list"],
            [("만들 것", "rag_mcp 폴더의 rag_search(question, top_k)"), ("호출", "기존 검색 그대로 · 청크 · 문서 · 쪽 반환"),
             ("설명문", "어떤 자료에서 무엇을 찾는 도구인지"), ("확인", "tools/list 형식으로 출력")], "rag-sim 폴더"), kick="3-1 · Tool"),
        page("로컬 MCP 서버 · 요청 작성", f5.guide(
            ["agent-sim의 MCP 요청을 받아 rag_search 실행"],
            ["HTTP MCP", "tools/call", "8790"],
            [("주소", "http://127.0.0.1:8790/mcp"), ("기준", "agent-sim lab/mcp_client.py 형식"),
             ("호출", "rag_search 실행 · 실패면 도구 오류"), ("관리 탭", "[MCP 관리] On/off · 상태 · 호출 로그")], "rag-sim 폴더"), kick="3-2 · MCP 서버"),
        page("MCP 서버 켜기", two(
            prompt("cd C:\\samsung_ds_YYYYMMDD\\rag-sim\n.\\run.bat", "[PowerShell] rag-sim을 다시 실행하는 경우"),
            ul(["rag-sim 다시 시작 → <b>[MCP 관리]</b> 탭",
                "<b>[MCP 서버 On]</b>",
                "실행 상태 · 주소 확인",
                "rag-sim을 실행한 PowerShell 창은 실습 동안 유지"]))
             + note("브라우저로 확인하지 않기", "MCP 주소는 웹페이지용 요청을 받지 않아 오류가 날 수 있음 → Claude Code에 확인 요청", "red"), kick="3-2 · MCP 서버"),
        page("MCP 서버 응답 확인 · 요청 작성", f5.guide(
            ["서버 코드를 바꾸지 않고 연결 · 목록 · 호출 확인"],
            ["initialize", "tools/list", "tools/call"],
            [("대상", "8790/mcp 응답 원문"), ("호출", "AEC-Q100 샘플 수 질문 · 기존 검색 결과와 대조")], "rag-sim 폴더"), kick="3-2 · MCP 서버"),
        page("MCP 서버를 껐다 켜며 대조", table(["상태", "기대 결과"], [
            ["<b>On</b>", "도구 목록의 rag_search · tools/call 반환 청크 = 기존 검색 화면의 같은 질문 결과 · 관리 탭에 MCP 호출 기록"],
            ["<b>Off</b>", "MCP 호출 실패 · 기존 검색 화면은 그대로 동작"],
            ["<b>마무리</b>", "MCP 서버 On"]])
             + note("실행 창 하나", "화면(8765)에서 MCP 서버(8790)를 관리"), kick="3-2 · MCP 서버"),
        page("agent-sim의 주소 등록 흐름 읽기", f5.guide(
            ["주소 입력 후 도구 목록이 바뀌기까지 이어지는 파일"],
            ["/api/mcp/add", "initialize", "tools/list"],
            [("읽을 경로", "app.js → app.py → mcp_client.py"), ("확인", "저장 성공 ≠ 연결 성공"), ("범위", "코드 수정 없이 읽기")], "agent-sim 폴더"), kick="3-3 · 쓰는 쪽"),
        page("rag-sim의 MCP 주소 등록", two(
            prompt("http://127.0.0.1:8790/mcp", "[MCP] 탭 · MCP 서버 주소") + SP
            + ul(["<b>[추가하고 연결]</b> · 2절과 같은 입력 칸", "연결 상태 + 도구 목록에 <b>rag_search</b>"]),
            pane("시작 전", ul(["3-3은 코드 수정 없음 · agent-sim 그대로", "rag-sim 관리 탭에서 MCP 서버 <b>On</b> 확인"]), "good"), "w"), kick="3-4 · 등록"),
        page("두 질문으로 도구 호출 확인", prompt("AEC-Q100의 기계적 충격 시험은 몇 개의 샘플로 수행하나요? 근거 문서와 페이지도 알려 줘.", "[앱 질문 입력칸] 질문 1") + SPS
             + prompt("PowerShell에서 현재 폴더를 확인하는 명령은 무엇인가요?", "[앱 질문 입력칸] 질문 2") + SP
             + ul(["질문마다 rag_search 호출 여부 · agent-sim 호출 기록 vs rag-sim MCP 로그의 도구 이름 · 인자",
                   "기존 검색 화면에서 같은 질문 · top_k 결과와 대조",
                   "안 불렸다면 설명문 vs 질문 비교 → 3-1에서 수정 → MCP Off → On → agent-sim 재연결"]), kick="3-5 · 호출 확인"),
        page("막히면 · MCP 연결", table(["증상", "확인"], [
            ["<b>MCP 연결 실패</b>", "MCP 서버 On · 포트 8790 · 주소가 <code>/mcp</code>로 끝나는지 · 호출 시도와 오류는 같은 탭"],
            ["<b>도구는 불렸는데 검색 오류</b>", "rag-sim 저장소에 문서가 적재되어 있는지 · MCP 로그의 오류 요약"],
            ["<b>연결됐는데 도구 없음</b>", "3-2의 tools/list 확인 다시 · 서버가 알려 주지 못하면 앱 목록에도 없음"],
            ["<b>한글 결과가 깨짐</b>", "서버 응답을 UTF-8로 보내도록 Claude Code에 수정 요청"],
            ["<b>포트가 이미 사용 중</b>", "관리 탭의 실행 오류 · 해당 포트 · 내가 이전에 실행한 서버만 종료 후 On · 다른 프로그램은 임의로 종료하지 않기"]]), kick="3-5 · 호출 확인"),
    ]


def block_design():
    return [
        section("04", "설계 관점", "검색 시점 · 연결 방식 · 입력 크기"),
        page("검색 여부를 정하는 주체", table(["", "rag-sim 화면", "agent-sim + rag_search"], [
            ["<b>구조</b>", "파이프라인형 RAG", "에이전트형 RAG"],
            ["<b>검색 시점</b>", "질문이 오면 <b>항상</b> 검색", "LLM이 <b>필요하다고 판단할 때</b> 검색"],
            ["<b>실제 검색</b>", "rag-sim 코드", "rag-sim 코드 (MCP를 거쳐 호출)"]])
             + '<div class="rec5" style="margin-top:16px">기록 · 반도체 질문: rag_search 호출 <u></u> &nbsp;/&nbsp; PowerShell 질문: rag_search 호출 <u></u></div>'
             + note("해석", "PowerShell 질문에서 rag_search 미호출 → 다른 검색 도구(Microsoft Learn)를 썼는지 · 도구 없이 답했는지 호출 기록으로 구분 · 특정 도구 미호출 ≠ 검색 전체 불필요"), kick="설계 질문"),
        page("업무 조건에 따른 선택", two(
            pane("파이프라인형 · 항상 검색", ul(["반드시 <b>사내 근거를 확인한 뒤</b> 답해야 하는 업무", "→ 더 안전"]), "good"),
            pane("에이전트형 · 판단해서 검색", ul(["문서와 관계없는 요청이 <b>섞여 들어오는</b> 업무", "→ 불필요한 검색 감소",
                                               "대신 필요한 검색을 <b>건너뛸 가능성</b>"]), "bad")), kick="설계 질문"),
        page("함수와 MCP 서버 중 선택", two(
            pane("한 앱에서만 쓴다면", ul(["앱 안의 <b>함수</b>가 단순", "서버를 띄우고 관리할 필요 없음"]), "bad"),
            pane("여러 AI 앱이 같은 기능을 쓴다면", ul(["<b>MCP 서버</b>가 유리", "규격이 같아 한 번 만든 서버를 여러 앱에 연결"]), "good"))
             + note("새 결정 사항", "서버로 내면 <b>누가 이 서버에 접근할 수 있는가</b>", "red"), kick="설계 질문"),
        page("더 해보기 · Claude Code 연결", prompt("claude mcp add --transport http rag-search http://127.0.0.1:8790/mcp", "[PowerShell] 새 창 · MCP 서버 On 유지") + SP
             + ul(["Claude Code 실행 → <code>/mcp</code>로 연결 상태 → 반도체 질문",
                   "서버 코드를 한 줄도 바꾸지 않고 다른 AI 앱에 도구가 붙음 = <b>「규격」의 의미</b>",
                   "agent-sim 클라이언트에 맞춰 만든 서버라 연결이 안 될 수도 있음 → 오류 메시지를 Claude Code에 보여 주고 규격에 맞게 수정 요청"]), kick="더 해보기"),
        page("연결할 도구와 반환할 정보", two(
            ul(["MCP로 연결해도 1교시의 입력 구성은 그대로: 이름 · 설명 · 입력 규격 전달 → 실행 결과를 다음 입력에",
                "서버가 따로 실행돼도 도구 정의 · 결과는 <b>Context Window 안</b>에서 처리",
                "저장소 전체가 아니라 <b>실제 반환한 청크의 원문 · 출처</b>가 도구 결과"]),
            table(["누가 정하나", "무엇을"], [
                ["<b>RAG 설계</b>", "검색 범위 · 반환할 근거의 크기"],
                ["<b>Agent 처리 흐름</b>", "언제 호출해 어떻게 사용할지"]]))
             + note("오류도 설계", "검색이 정상적으로 끝나 근거가 없는 경우 ≠ 서버에 연결되지 않은 경우 · 이후 판단에 필요한 정보가 다름", "red"), kick="Context"),
        page("정리", steps([
            ("검색을 감싼 Tool → MCP", "API는 코드가, Tool은 AI가 부름 · rag-sim 검색을 감싼 Tool을 MCP 규격으로 제공"),
            ("다른 앱의 도구가 된 RAG", "규격이 같아 이 서버는 agent-sim 전용이 아님"),
            ("업무에 옮길 때의 결정", "어떤 문서까지 검색 · 서버를 누구에게 · 읽기만 허용할지 → <b>도구 제작 = 권한 결정</b>"),
        ]), kick="정리"),
    ]


def block_more():
    return [
        section("05", "MCP 서버 예시", "7 · 8교시 캡스톤에서 쓸 만한 서버"),
        page("한국 MCP 모음 · Awesome MCP Korea", table(["분야", "서버", "쓰임"], [
            ["<b>국가통계</b>", "korea-stats-mcp", "KOSIS 국가통계 자연어 검색 · 분석 · 반도체 수출입 · 생산 통계"],
            ["<b>기업 공시</b>", "DART-mcp-server", "상장기업 공시 · 기업 개황 · 재무 정보 · 고객사 · 공급사 공시"],
            ["<b>법령</b>", "korean-law-mcp", "법령 · 판례 · 행정규칙 · 화학물질 · 산업안전 규정"],
            ["<b>공공데이터</b>", "data-go-mcp-servers", "공공데이터포털의 여러 API를 개별 MCP 서버로"]])
             + note("쓰기 전에", "서버마다 연결 방식(URL 또는 명령) · 인증 키 필요 여부가 다름 · 각 저장소 안내 확인"), kick="MCP 둘러보기"),
        page("캡스톤에서 활용할 만한 MCP", table(["분야", "서버", "쓰임"], [
            ["<b>논문 검색</b>", "arXiv MCP (예: cyanheads/arxiv-mcp-server)", "공정 · 소자 · 패키징 논문 검색 · 요약 · 개인 구현 여러 개"],
            ["<b>내 PC의 파일</b>", "Filesystem · 공식 참고 서버", "지정 폴더의 파일 읽기 · 찾기 · 실험 결과 · 보고서"],
            ["<b>웹 문서</b>", "Fetch · 공식 참고 서버", "웹페이지를 LLM이 읽기 좋게 · 제조사 공개 문서"],
            ["<b>코드 저장소</b>", "Git(공식 참고) · GitHub MCP Server", "분석 스크립트 · 자동화 코드 관리"],
            ["<b>제품 기술 문서</b>", "Microsoft Learn (2절)", "PowerShell · Excel 등 공식 문서"]])
             + note("보안", "명령 방식 서버는 내 PC에서 코드 실행 → 저장소 · 코드 먼저 확인 · 회사 자료를 외부로 보내면 사내 규정 확인 · 파일 서버는 폴더를 좁게", "red"), kick="MCP 둘러보기"),
        page("URL 연결과 명령 연결", table(["설정", "앱이 하는 일", "서버 실행 위치"], [
            ['<code>{"url":"https://…/mcp"}</code>', "주소에 HTTP 연결", "서비스 제공자의 서버 또는 지정한 PC"],
            ['<code>{"command":"npx","args":["…"]}</code>', "설치된 Node.js 환경에서 패키지 실행", "내 PC"],
            ['<code>{"command":"python","args":["server.py"]}</code>', "로컬 Python 서버 실행", "내 PC"]])
             + note("명령 방식", "내 PC에서 서버 프로그램 실행 · 표준 입력 · 출력(stdio)으로 통신 · npx · uv는 준비 · 실행 도구 · npm은 JavaScript 패키지 관리 도구 (MCP의 다른 이름 아님)")
             + note("주의", "npx 항목은 형식 설명용 · 실제 패키지명 · 인자 · 환경변수는 각 서버 안내 · 로컬 서버도 HTTP면 localhost URL · <b>URL 여부 ≠ 서버 위치</b>", "red"), kick="참고"),
        page("1~5교시를 이은 구조", '<div class="quote" style="font-size:24px;margin-bottom:22px">LLM만으로 해결하기 어려운 문제를 발견하고, 필요한 외부 기능을<br>MCP와 API로 하나씩 연결하면서 AI Agent를 확장</div><div class="parts">'
             + fig._tile("search", "RAG", "근거를 찾는 방법")
             + '<div class="plus">+</div>'
             + fig._tile("tool", "Tool Calling", "판단과 실행을 잇는 과정", "core")
             + '<div class="plus">+</div>'
             + fig._tile("plug", "MCP", "외부 도구와 연결하는 규격")
             + "</div>" + note("지금까지", "Agent 구성 요소 이해 → 필요한 문서 근거 선택 → 도구 실행 결과를 다음 입력에 반영"), kick="정리"),
        section("다음", "6교시 · Multi-Agent", "생산라인 이벤트의 판정과 조사를 나누는 구조 · 팩토리 시뮬레이터와 Decisions API · 처리 비용과 실행 조건"),
    ]


def slides():
    return opening() + block_api() + block_mcp() + block_mcp_lab() + block_design() + block_more()
