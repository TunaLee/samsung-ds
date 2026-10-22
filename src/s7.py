"""7교시 · 캡스톤 1 · 기획과 제작 (원본: 노션 교안 7교시)."""
import fig
import s7_fig as sf
from kit import (ba, big, cards, cover, flow, img, note, page, pane, prompt, section, steps, table, three, two, ul)
from s1 import course_map

TITLE = "캡스톤 1 · 기획과 제작"
IMG = "img/s7/"


def opening():
    return [
        cover(["캡스톤 1", "<em>기획</em>과 제작"],
              "제출 플랫폼에 가입하고, 업무 결과물을 기준으로 주제를 정해 구현합니다",
              [("교시", "7교시"), ("트랙", "AI Agent · Multi-modal RAG"), ("제출", "8교시 · 실행 결과 정리")], "7교시"),
        page("학습 목표", cards([
            ("제출 준비", "산출물 제출 플랫폼 가입 · 프로필 실명 입력", "01"),
            ("트랙 선택", "AI Agent 또는 Multi-modal RAG 중 하나", "02"),
            ("목표 정의", "입력 · 결과물 · 완료 조건까지 정하기", "03"),
            ("단계별 구현", "단계마다 요청하고 화면에서 결과 확인", "04"),
        ], 4)),
        page("과정 전체 흐름", course_map("7")
             + note("오늘", "주제를 정하고 핵심 기능부터 구현 → 8교시에 실제 실행 결과를 정리해 제출", "red")),
    ]


def block_platform():
    return [
        section("01", "제출 플랫폼 가입", "8교시에 완성한 결과 페이지를 제출할 곳"),
        page("회원가입", two(
            steps([("접속", "<code>contest-platform-production.up.railway.app/samsungds-B</code>"),
                   ("회원가입 탭", "오른쪽 위 [로그인] → [회원가입]"),
                   ("이메일 · 비밀번호", "본인 knox 이메일 두 번 입력 · 비밀번호 설정")])
            + note("비밀번호", "사내 계정과 다르게 설정", "red"),
            img(IMG + "signup.png", "[화면 1] 회원가입 · knox 이메일로 가입", light=True), "w2"), kick="제출 플랫폼"),
        page("프로필에 실명 입력", two(
            ul(["가입 후 프로필에 <b>본인 실명</b> 입력", "결과물 <b>전시관</b>에 이 이름이 표시됨", "8교시 제출도 이 계정으로"]),
            img(IMG + "profile.png", "[화면 2] 프로필 · 전시관에 표시될 이름", light=True), "w2"), kick="제출 플랫폼"),
    ]


def block_topics():
    return [
        section("02", "캡스톤 주제 A / B", "두 트랙 중 하나를 선택해 진행"),
        page("두 트랙", '<div class="s7-tks">'
             + sf.track("tool", "A 트랙", "AI Agent",
                        "업무 목표를 받아 필요한 Tool을 고르고, 실행 결과에 따라 다음 행동을 결정",
                        "최종 결과물과 근거를 화면에서 확인")
             + sf.track("search", "B 트랙", "Multi-modal RAG",
                        "그림 · 표 · 도식이 많은 PDF를 페이지 그대로 검색해 답변",
                        "근거 페이지와 함께 보여 주는 기술 문서 검토 도우미")
             + "</div>"),
        page("A. AI Agent 트랙", ba(
            "질문에 답하는 챗봇\n\n답변이 대화창에서 끝남",
            "업무 과정의 일부를 직접 수행하는 Agent\n\n자료 찾기 · 파일 읽기 · 데이터 계산 · 외부 시스템 조회\n다음 행동: 추가 조회 · 계산 · 사용자 확인 · 종료",
            "목표가 아닌 것", "목표")
             + note("화면", "최종 결과물과 그 근거를 확인할 수 있어야 함", "red"), kick="A 트랙"),
        page("A 트랙 작업 예시", cards([
            ("파일 정리", "여러 파일을 읽어 필요한 내용을 찾아 정리", "01"),
            ("CSV 집계", "시험 결과 CSV를 분석해 조건별 집계표 작성", "02"),
            ("누락 확인", "폴더에서 누락된 파일이나 항목 확인", "03"),
            ("검토표", "여러 자료를 비교해 검토표 생성", "04"),
            ("함께 조사", "내부 데이터와 외부 정보를 함께 조사", "05"),
            ("반복 자동화", "반복되는 자료 확인 · 정리 작업 자동화", "06"),
        ], 3), kick="A 트랙"),
        page("A 트랙 Tool 예시", two(
            table(["필요한 기능", "Tool"], [
                ["외부 정보 조사", "<b>Web Search</b>"], ["파일 · 폴더 접근", "<b>Filesystem MCP</b>"],
                ["계산 · 가공", "<b>Python Tool</b>"], ["DB 조회", "<b>SQLite / 직접 만든 Tool</b>"],
                ["웹 페이지 조회", "<b>Fetch 계열 MCP</b>"]]),
            ul(["직접 Tool로 만들거나 제공된 MCP 활용", "모든 Tool을 사용할 필요 없음"])
            + note("원칙", "자신의 업무에서 실제로 필요한 작업 하나를 정하고, <b>필요한 Tool만</b> 연결", "red"), "w"), kick="A 트랙"),
        page("B. Multi-modal RAG 트랙", two(
            pane("텍스트만 추출하는 RAG", ul(["그림 안의 글자", "표의 구조", "도식의 연결 관계", "→ 잃기 쉬움"]), "bad"),
            pane("이 트랙", ul(["페이지를 <b>이미지</b>로 바꿔 임베딩", "찾은 페이지 이미지를 근거로 답변", "임베딩 모델: 내 PC에서 실행하는 <b>EmbeddingGemma 2</b>"]), "good"))
             + sf.chain(["PDF 올리기", "페이지마다 이미지로", "내 PC 모델로 임베딩", "벡터 DB에 저장", "가까운 페이지 찾기", "보고서형 답변"], hl=(2,), cls="sm")
             + note("최종 목표", "그림과 표 속 내용까지 근거 페이지와 함께 보여 주는 <b>기술 문서 검토 도우미</b>", "red"), kick="B 트랙"),
    ]


def block_check():
    return [
        section("03", "캡스톤 시작 전 확인", "실제 업무와 가까운 주제 · 입력하는 정보는 계속 확인"),
        page("외부 AI 서비스에 입력하지 않는 것", cards([
            ("사내 기밀", "실제 사내 기밀 정보", "01"), ("미공개 제품 정보", "출시 전 제품 · 사양", "02"),
            ("고객 정보", "고객사 · 거래 정보", "03"), ("개인정보", "이름 · 연락처 등", "04"),
            ("내부 코드 · 문서", "사내 코드 · 내부 문서", "05"),
            ("대신 사용할 것", "공개 문서 · 교육용 가상 데이터 · 실제 CSV는 <b>형식만</b> 본뜬 가상 데이터", "→"),
        ], 3), kick="보안"),
        page("대화가 깊어질수록 섞이는 정보", sf.drift()
             + note("확인 범위", "최초 프롬프트만이 아니라 <b>대화 중 추가로 입력하는 내용</b>도 계속 확인", "red"), kick="보안"),
        page("실습 중 보안 원칙", sf.checks([
            "공개 문서와 가상 데이터 사용",
            "실제 사내 문서 · 코드 · 미공개 정보는 입력하지 않음",
            "실제 이름 · 수치 · 프로젝트명은 필요하면 가상의 값으로",
            "첫 질문뿐 아니라 <b>이어지는 대화</b>에서도 민감한 정보가 없는지 확인",
            "AI가 더 자세한 자료를 요구해도 <b>입력 가능한 정보인지</b> 먼저 판단",
        ]), kick="보안"),
    ]


def block_agent():
    return [
        section("04", "Agent 트랙", "업무를 수행하는 AI Agent 만들기"),
        page("내 업무의 일부를 실제로 수행", flow([
            ("사용자 요청", "자연어"), ("LLM 판단", "필요한 행동"), ("Tool 실행", "앱이 실행"),
            ("실행 결과", "실제 데이터"), ("업무 결과물", "표 · 목록")], hl=2)
             + two(ul(["반복해서 확인 · 정리하는 작업", "여러 자료를 함께 봐야 하는 작업", "사람이 매번 손으로 처리하는 작업"]),
                   note("데이터", "실제 사내 데이터 대신 <b>공개 자료</b>나 업무 형식을 본뜬 <b>가상 데이터</b>", "red")), kick="Agent 트랙"),
        page("주제 예시", cards([
            ("누락 항목", "폴더의 여러 시험 결과를 읽고 누락 항목 찾기", "01"),
            ("조건별 집계", "CSV 데이터를 읽어 조건별 결과 집계", "02"),
            ("변경점 비교", "여러 문서를 찾아 변경점 비교", "03"),
            ("후속 조치", "자료를 읽고 회의 후속 조치 목록 만들기", "04"),
            ("함께 조사", "내부 데이터와 외부 정보를 함께 조사", "05"),
            ("인수인계", "여러 파일을 찾아 인수인계용 정리표 만들기", "06"),
        ], 3), kick="Agent 트랙"),
        page("수행할 작업 하나 정하기", two(
            steps([("입력", "Agent가 어떤 입력을 받는가"), ("Tool", "어떤 Tool을 실제로 사용해야 하는가"),
                   ("결과물", "실행이 끝나면 어떤 업무 결과물이 나오는가")]),
            '<div style="font-weight:800;margin-bottom:10px">예: 시험 결과 검토 Agent</div>' + sf.agent_io().replace("s7-ios", "s7-ios s7-iov"))
             + note("이 단계", "아직 코드 없이 Claude Code와 대화하며 <b>업무 범위가 너무 크지 않은지</b> 먼저 확인", "red"), kick="4-1"),
        page("목표는 완료 조건까지", ba(
            "CSV를 분석한다",
            "지정한 Lot의 시험 결과와 교육용 기준을 대조해,\n누락 · 기준 이탈 · 판단 불가 항목과 근거를 담은\n검토표를 만든다",
            "모호한 목표", "입력과 완료 여부를 확인하기 쉬운 목표")
             + note("다른 주제", "성공 조건 · 부족한 정보에 대한 행동 · 종료 조건을 먼저 정하고, 최소 기능부터 구현", "red"), kick="4-1"),
        page("목표를 이루는 다섯 가지", table(["항목", "시험 결과 검토 Agent 예"], [
            ["<b>입력</b>", "Lot ID · 시험 결과 폴더 · 교육용 기준 파일 · Lot 미지정이면 먼저 확인"],
            ["<b>결과물</b>", "항목별 측정값 · 단위 · 적용 기준 · 검토 상태 · 근거 파일과 행 번호 · 자료가 없으면 「자료 부족」"],
            ["<b>Agent의 판단</b>", "필요한 파일 선택 · 누락 발견 시 다른 자료 조회 또는 사용자 질문 · 계산식은 Tool에서 일관되게"],
            ["<b>완료 · 중단</b>", "각 항목에 상태와 근거가 있으면 종료 · 찾을 자료가 없거나 호출 한도면 미해결 항목과 이유"],
            ["<b>실행 범위</b>", "입력 파일은 조회만 · 결과는 별도 출력 폴더 · 설비 제어 · 업무 승인 · 외부 전송 제외"],
        ], "s7-tt"), kick="4-1"),
        page("프롬프트 작성 힌트", two(
            sf.checks(["내가 만들려는 Agent의 업무", "사용할 공개 또는 가상 데이터", "최종적으로 보고 싶은 결과물",
                       "사람이 마지막에 확인해야 하는 항목", "처음에는 <b>핵심 기능 하나만</b>"]),
            note("Claude Code에게", "위 다섯 가지를 설명하며 대화 시작", "red")), kick="4-1"),
        page("Dummy data로 판단할 장면 만들기", three(
            pane("정상", ul(["필요한 자료가 모두 있음", "계산 후 종료"]), "good"),
            pane("누락", ul(["항목 · 파일이 빠짐", "추가 조회 · 질문 · 자료 부족"]), "good"),
            pane("충돌", ul(["단위 · 기준이 맞지 않음", "추가 확인 · 판단 보류"]), "good"))
             + note("이유", "항상 같은 순서로 끝나면 다음 행동을 판단하는지 보기 어려움")
             + note("Dummy data", "실제 업무 자료를 대신하는 교육용 가상 데이터 · 목표를 정한 뒤 <b>소량</b>으로", "red"), kick="4-1-1"),
        page("데이터 생성 요청 직접 작성", two(
            ul(["한 행이 무엇을 뜻하나요?", "어떤 ID로 파일을 연결하나요?", "어떤 사례에서 추가 조회 · 계산 · 질문 · 중단이 필요할까요?", "각 사례의 <b>예상 결과</b>를 먼저 정하기"]),
            '<div style="font-weight:800;margin-bottom:10px">키워드</div>'
            + sf.keywords(["합성 데이터", "스키마", "연결 ID", "정상 / 누락 / 충돌", "고정 seed", "기대 결과", "별도 검증 파일"])
            + note("입력", "내부 문서 · 실제 값 첨부 없이 열 이름 · 형식 · 가상 범위만 설명", "red")), kick="Claude Code · Prompt 직접 작성"),
        page("실습 조건 · 시험 결과 검토 예시", prompt(
            "- data/test_results.csv: row_id, lot_id, test_item, measured_value, unit, measured_at. 행 하나는 한 Lot의 시험 항목 측정 결과.\n"
            "- data/criteria.csv: test_item, unit, min_value, max_value, required. 연결 기준은 test_item과 unit이며 모든 수치는 교육용 가상 기준.\n"
            "- 작은 규모부터 시작: Lot 3개·필수 시험 항목 3개, 정상 3행 + 누락 사례 2행 + 충돌 사례 3행. 예: LOT-DEMO-02의 항목 1개 누락, LOT-DEMO-03의 단위 1개 불일치.\n"
            "- 검증용 expected_results.json에는 사례별 기대 상태·근거 행·기대 행동을 기록. Agent가 조회하는 data/ 폴더 밖 evaluation/에 두고 Tool 접근 대상에서 제외.\n"
            "- generate_dummy.py와 README에 스키마·단위·생성 규칙·고정 seed·재생성 방법 기록. “교육용 합성 데이터” 표시와 UTF-8 저장. 실데이터 복사·익명화 방식으로 대체하지 않음.",
            "실습 조건 확인")
             + note("사용법", "요청문에 넣을 조건 · 문장은 직접 작성"), kick="4-1-1"),
        page("만든 데이터 확인", two(
            steps([("직접 읽기", "샘플 몇 행 · ID 연결 · 단위 · 누락 · 충돌이 의도대로인지"),
                   ("기대 결과는 사람용", "Agent에게 답으로 제공하지 않음"),
                   ("재생성", "구조가 맞으면 같은 생성기로 다시 만들 수 있게")]),
            pane("B 트랙", ul(["제공된 공개 PDF 그대로 사용 가능", "가상 PDF는 <b>선택</b>: 가상 표 · 그림과 확인 질문부터", "렌더링된 페이지가 읽히는지 확인"]), "bad")), kick="4-1-1"),
        page("필요한 Tool 선택", two(
            table(["행동", "Tool"], [
                ["폴더와 파일 조회", "Filesystem MCP"], ["웹 페이지 읽기", "Fetch 계열 MCP"], ["브라우저 작업", "Browser 계열 MCP"],
                ["DB 조회", "SQLite Tool"], ["외부 정보 조사", "Web Search"], ["CSV 계산 · 가공", "직접 만든 Python Tool"]], "s7-tt"),
            ul(["Agent가 <b>직접 수행할 행동</b> 기준", "강사 제공 MCP 목록 참고", "모든 Tool을 연결하지 않음"])
            + note("시작", "업무에 반드시 필요한 Tool <b>1~2개</b>부터", "red")
            + note("기준", "Tool 개수 ≠ 좋은 Agent · 정확한 선택과 사용")), kick="4-2"),
        page("LLM보다 Tool 먼저 확인", two(
            '<div style="font-weight:800;margin-bottom:8px">Filesystem MCP</div>'
            + sf.chain(["폴더 목록 요청", "Filesystem MCP", "실제 파일 목록"], hl=(2,), cls="sm")
            + '<div style="font-weight:800;margin:18px 0 8px">직접 만든 CSV 분석 Tool</div>'
            + sf.chain(["CSV 파일", "계산 Tool", "실제 집계 결과"], hl=(2,), cls="sm"),
            pane("확인할 것", sf.checks(["실제 데이터를 읽었는가", "입력값은 무엇이었는가", "반환 결과는 어떤 구조인가", "잘못된 경로 · 없는 파일이면 어떻게 되는가"]), "good"))
             + note("순서", "Tool 결과를 확인한 뒤에 LLM 연결", "red"), kick="4-3"),
        page("LLM이 Tool을 선택", flow([
            ("사용자 요청", ""), ("LLM", ""), ("Tool 선택", "인자 결정"), ("Tool 실행", ""), ("실행 결과", "실제"), ("LLM 답변", "")], hl=2)
             + note("한 번의 실행", "위 흐름은 도구 한 번으로 답할 수 있는 경우")
             + note("반복 호출", "4교시처럼 결과를 읽고 다음 행동 선택 · 질문 · 지침 · 도구 결과가 입력에 쌓임 → 필요한 근거는 남기고 중복 결과의 전달 범위 정하기", "red"), kick="4-4"),
        page("다음 행동을 고르게 하기", sf.decide()
             + note("이번 트랙", "입력이나 조회 결과에 따라 <b>다음 행동이 달라지는 장면</b>을 하나 이상 확인", "red"), kick="4-4 · 설계 질문"),
        page("화면에 남길 것 · 빠진 요청 테스트", two(
            pane("최종 답변과 함께", sf.checks(["어떤 Tool을 사용했는지", "Tool에 어떤 인자를 전달했는지", "Tool이 어떤 결과를 반환했는지"]), "good"),
            prompt("이번 시험 결과를 정리해 줘.", "정보가 빠진 요청")
            + '<div style="margin-top:16px">' + ul(["어떤 시험 결과인지 모르면 <b>임의로 정하지 않음</b>", "필요한 정보를 다시 묻기", "또는 현재 정보로 할 수 있는 일 알리기"]) + "</div>"), kick="4-4"),
        page("정상 · 누락 · 충돌로 목표 달성 확인", table(["사례", "확인할 것"], [
            ["<b>정상</b>", "필요한 자료를 읽고 계산해 검토표를 완성한 뒤 종료하는가 · 근거 파일 · 행 · 실제 Tool 반환값이 맞는가"],
            ["<b>누락</b>", "없는 값을 지어내지 않고 다른 자료를 찾거나, 사용자에게 묻거나, 자료 부족을 표시하는가"],
            ["<b>충돌</b>", "단위나 기준이 맞지 않는 항목을 그대로 비교하지 않고 추가 확인하거나 판단을 보류하는가"],
        ]), kick="4-4"),
        page("호출 로그로 따라가기", sf.chain(["받은 결과", "선택한 다음 행동", "최종 상태"], hl=(1,))
             + two(pane("구분할 것", ul(["모든 Tool을 정해진 순서로 호출한 흐름 vs <b>Agent가 선택한 부분</b>", "코드가 강제한 분기 vs <b>LLM이 선택한 행동</b>"]), "good"),
                   pane("기대와 다르면", ul(["Claude Code에 전달: 실제 입력 · 호출 인자 · 반환값 · 기대한 행동", "선택지가 달라진 사례와 추가 행동 없이 끝난 사례를 나란히"]), "bad")), kick="4-4"),
        page("채팅이 아닌 업무 결과물", cards([
            ("시험 결과 집계표", "", "01"), ("누락 파일 목록", "", "02"), ("변경점 비교표", "", "03"),
            ("후속 조치 목록", "", "04"), ("검토 체크리스트", "", "05"), ("분석 결과 요약표", "", "06"),
        ], 3) + note("가능하면", "결과를 만든 <b>근거가 어디에서 왔는지</b>도 함께 확인", "red"), kick="4-5"),
        page("최종 개발 요청 직접 작성", two(
            ul(["사용자는 어떤 요청을 할 것인가", "Agent가 판단해야 할 것은 무엇인가", "어떤 Tool을 어떤 상황에서 호출하는가", "Tool 실행 결과를 화면에 어떻게 보여 줄 것인가"]),
            ul(["어떤 업무 결과물을 만들어야 하는가", "정보가 부족하면 어떻게 행동하는가", "Tool 실패를 어떻게 구분해서 보여 줄 것인가", "실행하지 않은 작업을 했다고 말하지 않게 하려면"]))
             + note("먼저 완성", "하나의 요청이 <code>사용자 입력 → Tool 실행 → 실제 결과 → 업무 결과물</code>까지 이어지는 것", "red")
             + note("이제부터", "완성된 프롬프트는 제공하지 않음"), kick="4-5"),
    ]


def block_rag():
    return [
        section("05", "Multi-modal RAG 트랙", "그림과 표까지 검색하는 문서 도우미 만들기"),
        page("페이지를 이미지 한 장으로", ba(
            "2 · 3교시 rag-lab\nPDF에서 텍스트를 뽑아 청크로 나눠 검색\n\n그림 · 표 · 그래프 속 핵심 정보를 놓치기 쉬움",
            "PDF의 각 페이지 = 이미지 한 장\n텍스트와 이미지를 같은 공간에 임베딩\n\n글로 쓴 질문으로 그림이 있는 페이지를 찾음",
            "텍스트 청크", "페이지 이미지"), kick="Multi-modal RAG"),
        page("전체 구조", sf.mmrag()
             + note("데이터 이동", "문서 준비 단계의 임베딩은 내 PC 안에서 · 답변 단계에서는 찾은 페이지 이미지가 <b>OpenAI API로 전송</b> · 제공된 공개 문서만 사용", "red"), kick="Multi-modal RAG"),
        page("사용할 문서 선택", two(
            pane("A. 가로형 문서 · 발표 자료 형태", ul(["NASA Goddard — Development of Large-Scale Magnetic Calorimeter Arrays", "9페이지 · 16:9", "대형 센서 어레이 구조 · 매립 Nb 배선 공정 · 읽기 회로", "SEM 사진 · 도식 · 측정 그래프 · 표"]), "good"),
            pane("B. 세로형 문서 · 기술 문서 형태", ul(["Sandia · Honeywell — Maintaining Low Voiding Solder Die Attach for Power Die While Minimizing Die Tilt", "7페이지", "전력 다이 솔더 접합의 보이드 · 기울기 줄이기", "리플로 프로파일 · 초음파 영상 · 관리도 · 그래프 · 표"]), "good"))
             + note("진행", "하나를 먼저 끝까지 · 시간이 남으면 다른 문서도 올려 비교")
             + note("시간", "두 문서 모두 10페이지 미만 · 그래픽카드가 없으면 한 페이지에 10~20초 이상", "red"), kick="Multi-modal RAG"),
        page("1단계 · 로컬 임베딩 모델", big([("768", "임베딩 차원"),
                                         ("Apache 2.0", "라이선스"), ("약 1.5GB", "내려받는 파일")])
             + note("EmbeddingGemma 2", "<code>google/embeddinggemma-2</code> (Hugging Face) · Google 공개 임베딩 모델 · 텍스트 · 이미지 · 오디오를 하나의 벡터 공간에 · 가중치 공개 → 내 PC에서 실행")
             + note("이 단계만", "오디오 인코더는 불러오지 않음 · 설치가 막히기 쉬워 <b>요청문을 그대로</b> 사용", "red"), kick="5-1"),
        page("1단계 요청문", prompt(
            "멀티모달 RAG 실습 프로젝트를 준비해 줘.\n\n"
            "- Python 가상환경을 만들고 필요한 패키지를 설치해 줘.\n"
            "- 임베딩 모델은 다음 프롬프트를 수행해서 C:\\model 또는 C:\\models 폴더에 이미 다운 받았으니 \n"
            "  확인해줘. 해당 폴더에 파일이 없다면 이 폴더에 설치해 줘.\n"
            "---\n"
            "Hugging Face에서 아 모델을 현재 폴더 아래에 다운로드해 줘. \n"
            "심볼릭 링크 없이 실제 파일들이랑 하위 폴더 구조(1_Pooling 등)가 그대로 다 들어오게 받아줘.\n"
            "https://huggingface.co/google/embeddinggemma-2\n"
            "---\n"
            "  임베딩모델의 사용법은 아래 문서를 읽고 그대로 따라 줘.\n"
            "  https://developers.googleblog.com/embeddinggemma-2-the-developer-guide/\n"
            "  sentence-transformers 6.1 이상이 필요하고,\n"
            "  오디오는 쓰지 않으니 오디오 인코더는 불러오지 마.\n"
            "- GPU가 없는 노트북이니 개발 진행 시 참고해줘\n"
            "- PDF 는 docs 폴더에 있어.\n\n"
            "모델을 받은 뒤 test_embed.py 를 만들어 실행하고 다음을 보여 줘.\n"
            "- 모델을 불러오는 데 걸린 시간, 파라미터 수, 임베딩 차원",
            "Claude Code", sm=True), kick="5-1"),
        page("1단계 확인할 것", sf.checks([
            "처음 실행: 모델 파일 내려받기 · 두 번째부터는 내 PC에 저장된 모델을 바로 불러옴",
            "관련 있는 문장이 관계없는 문장보다 페이지 이미지와 <b>유사도가 높은지</b> → 글과 그림이 같은 공간에",
            "페이지 한 장의 <b>임베딩 시간</b> 기록 → 문서 전체 준비 시간 가늠",
            "GPU가 없으면 CPU로 실행 · 한 페이지에 10~20초 이상",
        ]) + note("막히면", "다운로드 · 설치에 시간이 걸림 · 막히면 오류 화면을 강사에게 보여 주고 접속 가능한 환경인지 확인", "red")
             + note("다음 단계", "첫 임베딩 결과까지 확인한 뒤 진행"), kick="5-1"),
        page("임베딩 저장소: 벡터 DB", table(["", "일반 데이터베이스", "벡터 데이터베이스"], [
            ["<b>찾는 기준</b>", "값이 조건과 같거나 범위 안에 있는 행", "질문 벡터와 거리가 가까운 항목"],
            ["<b>질문 예</b>", "문서명이 A이고 페이지가 3인 행", "「전원 핀 배치」와 가장 비슷한 페이지 3개"],
            ["<b>결과</b>", "조건을 만족하는 행 전체", "가까운 순서로 정렬된 상위 k개와 거리"],
        ]) + note("저장 이유", "페이지 한 장 = 숫자 768개 벡터 하나 · 질문마다 다시 임베딩하면 너무 오래 걸림 → 문서 준비 때 한 번 만들어 저장")
             + note("함께 저장", "문서명 · 페이지 번호 · 이미지 경로 같은 <b>메타데이터</b>", "red"), kick="5-2"),
        page("거리 · 색인 · Chroma", cards([
            ("코사인 거리", "두 벡터의 방향이 비슷할수록 거리가 0에 가까움", "1"),
            ("색인 (인덱스)", "벡터가 많아지면 하나씩 비교하지 않고 가까운 후보를 빠르게 찾음", "2"),
            ("Chroma", "별도 서버 설치 없이 프로젝트 폴더 안에 저장되는 벡터 DB", "3"),
        ]) + note("같은 모델 · 같은 차원", "저장할 때와 질문할 때 동일하게 · 모델을 바꾸면 문서를 다시 준비", "red"), kick="5-2"),
        page("2단계부터는 요청을 직접 설계", flow([
            ("문서 준비", "페이지 이미지 임베딩"), ("검색", "같은 멀티모달 공간에서 비교"), ("답변", "페이지 이미지 + 질문")], hl=1)
             + ul(["흐름은 앞선 RAG와 같음 · 검색 단위가 <b>텍스트 청크 → 페이지 이미지</b>", "안내는 각 단계에서 만들 것과 정할 것 · 화면 구성과 표현은 각자"])
             + note("진행 방식", "한 번에 모든 기능을 요청하지 않음 · 단계마다 요청 → 화면 확인 → 다음 요청 · 예상과 다르면 무엇을 어떻게 만들었는지 먼저 설명하게", "red"), kick="5-3"),
        page("Claude Code가 모르는 사실 알려 주기", sf.checks([
            "모델은 5-1의 <code>test_embed.py</code>와 같은 방식으로 불러옴",
            "페이지 이미지는 프롬프트 없이 임베딩 · 질문 텍스트에는 검색 질의용 프롬프트(<code>SearchQuery</code>)",
            "답변 모델은 <code>gpt-5.6-luna</code> · <code>.env</code>의 <code>OPENAI_API_KEY</code> 사용",
        ]) + note("이유", "EmbeddingGemma 2는 최근 공개된 모델 · Claude Code가 사용법을 정확히 모를 수 있음 → 요청에 함께 적기", "red"), kick="5-3"),
        page("2단계 · 문서를 벡터 DB에", table(["정할 것", "생각할 점"], [
            ["<b>화면</b>", "문서를 올리는 화면과 저장된 내용을 보는 화면 나누기 · 웹 앱 형태 (예: Streamlit)"],
            ["<b>페이지 이미지 크기</b>", "낮으면 표의 작은 글자가 뭉개짐 · 높으면 저장 용량과 처리 시간 증가"],
            ["<b>함께 저장할 정보</b>", "근거를 보여 주려면 벡터 외에 무엇이 필요한가 · 문서명 · 페이지 번호 · 이미지 파일 위치"],
            ["<b>거리 방식</b>", "5-2의 코사인 거리로 지정"],
            ["<b>다시 올렸을 때</b>", "같은 문서를 다시 올리면 기존 벡터를 어떻게 처리할까"],
            ["<b>진행 표시</b>", "CPU에서 한 페이지 10~20초 이상 · 기다리는 동안 무엇을 보여 줄까"],
        ], "s7-tt"), kick="5-4 · 요청 전에 정할 것"),
        page("2단계 확인할 것", two(
            pane("이 단계를 마치면", ul(["PDF를 올리면 페이지마다 이미지와 벡터가 저장", "무엇이 저장됐는지 화면에서 확인"]), "good"),
            pane("확인할 것", sf.checks(["페이지 수만큼 벡터가 저장되었는가", "항목 하나의 문서명 · 페이지 · 이미지와 벡터 값을 확인할 수 있는가"]), "good"))
             + note("벡터 값", "그림이 많은 페이지도 결국 숫자 768개로 저장", "red"), kick="5-4"),
        page("3단계 · 질문하면 페이지를 찾아 답변", table(["정할 것", "생각할 점"], [
            ["<b>찾을 페이지 수</b>", "몇 장을 답변 모델에 보낼까 · 너무 적으면 근거가 빠지고, 너무 많으면 시간과 비용 증가"],
            ["<b>근거가 없을 때</b>", "찾은 페이지에 답이 없으면 어떻게 답하게 할까"],
            ["<b>문장과 근거의 연결</b>", "답변의 어느 문장이 어느 페이지에서 나왔는지 표시 방법"],
            ["<b>답변을 보여 주는 방식</b>", "읽는 사람이 무엇을 먼저 보고, 언제 근거를 확인하게 할까"],
        ]) + note("이 단계를 마치면", "질문을 입력하면 관련 페이지를 찾고, 그 페이지 이미지를 근거로 답변", "red"), kick="5-5 · 요청 전에 정할 것"),
        page("결론 → 근거 → 과정", two(sf.report(), ul([
            "<b>결론</b>: 답변을 눈에 띄는 상자에 먼저",
            "<b>근거</b>: 답변의 표시와 짝이 되는 카드 · 썸네일 · 문서명 · 페이지 번호 · 거리",
            "<b>과정</b>: 질문 임베딩 시간 · 검색 순위와 거리 · 응답 시간과 토큰 수"]), "w")
             + note("하나의 예", "다른 형식도 가능 · 업무에서 이 답변을 받아 볼 사람에게 맞는 모양으로"), kick="5-5 · 보고서형 화면"),
        page("그림 · 표 속 답을 묻는 질문", two(
            prompt("LXM 배열 구성도에서 Enhanced array의 픽셀 수와 에너지 분해능은 얼마인가요?", "A. 가로형 문서")
            + prompt("50 mK에서 측정한 Main array 픽셀의 NEP는 잡음 보정 전후로 각각 얼마인가요?", "A. 가로형 문서"),
            prompt("리플로 프로파일에서 압력을 가하는 구간의 압력과 최고 온도는 얼마인가요?", "B. 세로형 문서")
            + prompt("다이 기울기가 가장 작았던 툴링 조합과 그때의 평균 기울기는 얼마인가요?", "B. 세로형 문서"))
             + note("확인", "답변이 가리키는 페이지 이미지에 실제로 그 내용이 있는지", "red"), kick="5-5"),
        page("4단계 · 텍스트만 읽었을 때 놓치는 정보", two(
            pane("비교할 것", ul(["근거가 된 페이지를 PDF 텍스트 추출로만 읽으면 무엇이 남는가", "답의 근거가 된 그림 · 표 내용이 추출 텍스트에도 남아 있는가", "비교 결과를 화면 어디에 보여 줄지 직접 정해 요청"]), "good"),
            pane("해석할 때", ul(["추출 텍스트엔 없고 페이지 이미지엔 있다면 → 이번 추출 방식에서 빠진 정보를 이미지로 확인한 것", "OCR · 표 구조 추출을 쓰는 다른 텍스트 기반 RAG까지 같은 한계라고 <b>일반화하지 않음</b>"]), "bad")), kick="5-6"),
        page("더 해보기", cards([
            ("텍스트 검색 함께", "페이지 텍스트도 임베딩해 저장 · 이미지 검색 결과와 합쳐 순위 결정", "1"),
            ("검색 후 다시 평가", "3교시 Reranking처럼 찾은 페이지 후보를 LLM이 질문과 함께 다시 평가해 순서 변경", "2"),
            ("답변 모델도 내 PC에서", "답변 생성까지 로컬 모델로 → 문서가 PC 밖으로 나가지 않는 RAG", "3"),
        ]), kick="더 해보기"),
    ]


def _qs(rows):
    return '<div class="s7-qs">' + "".join(f'<div class="s7-q"><b>{e}</b><span>{k}</span></div>' for e, k in rows) + "</div>"


def block_graph():
    return [
        section("참고", "GraphRAG 실습", "기본 RAG를 직접 구현한 뒤 관계 탐색으로 확장"),
        page("GraphRAG 트랙", sf.chain([("1", "PDF 읽기"), ("2", "Chunk 만들기"), ("3", "검색하기"), ("4", "검색 결과로 답변"),
                                         ("5", "관계가 필요한 질문 실험"), ("6", "Graph 만들기"), ("7", "Graph 탐색 · 업무 결과물")], hl=(5, 6), cls="sm")
             + two(ul(["업무 관련 기술 문서를 근거로 <b>검색 · 비교 · 검토</b>하는 앱", "강사 제공 공개 문서 중 하나 선택", "처음부터 전체를 만들지 않음 · 기본 RAG부터", "여러 정보를 잇는 질문으로 일반 RAG의 한계 확인 → 관계 탐색 추가"]),
                   pane("최종 업무 결과물", ul(["조건 비교표", "검토 체크리스트", "방법별 비교서", "관계와 근거가 표시된 기술 검토 결과"]), "good"), "w")
             + note("단계마다", "화면에 나타난 결과를 직접 확인하고, 다음에 추가할 것을 생각하며 개발", "red"), kick="참고 · GraphRAG"),
        page("사용할 문서 선택", table(["문서", "연결해서 살펴볼 대상", "결과물 예"], [
            ["<b>A. 패키지 수분 민감도</b><br>TI SLZA002 · Moisture Sensitivity Level", "패키지 · 수분 노출 · 리플로 · 손상 · 관리 조건", "수분 민감 패키지의 보관 · 취급 검토 도우미"],
            ["<b>B. 소프트 에러 대응</b><br>ST AN4750 · Handling of soft errors in STM32 applications", "오류 유형 · 메모리 · 검출 방식 · 완화 방법 · 제약", "메모리 소프트 에러의 검출 · 완화 방법 비교서"],
            ["<b>C. ESD 포장</b><br>TI SZZA027A · ESD Protective Semiconductor Packing Materials and Configurations", "부품 · 포장 형태 · 재료 · 보호 특성 · 시험 방법", "반도체 포장 방식별 ESD 보호 검토 체크리스트"],
        ], "s7-tt"), kick="참고 · GraphRAG"),
        page("관계 검색 질문의 출발점", '<div style="display:flex;flex-direction:column;gap:12px">'
             + prompt("수분 노출과 패키지 손상에 관련된 조건을 어떤 근거로 연결할 수 있나요?", "A. 패키지 수분 민감도")
             + prompt("RAM의 소프트 에러를 검출하고 완화하는 방법과 각 방법의 제약은 무엇인가요?", "B. 소프트 에러 대응")
             + prompt("트레이와 테이프·릴의 ESD 보호 특성을 확인할 때 어떤 시험과 재료 정보를 함께 봐야 하나요?", "C. ESD 포장")
             + "</div>", kick="참고 · GraphRAG"),
        page("1단계 · 문서를 올리면 검색까지", two(
            sf.vchain([("PDF 업로드 + 청킹 전략 선택", "수강생이 고르는 것은 청킹 전략 하나"), ("파싱 → 청킹 → 임베딩 → 저장", "자동"), ("질문 → 검색 → 답변", "")], hl=(0,)),
            ul(["2 · 3교시에서 단계별로 열어 본 과정을 <b>한 번에</b>", "문서를 올리면 준비가 자동으로 끝나고 바로 질문", "나머지는 앱이 알아서 진행"]), "w"), kick="참고 · GraphRAG 5-1"),
        page("1단계 요청문 (1/2)", prompt(
            "선택한 PDF 로 질문에 답하는 RAG 실습 프로젝트를 만들어 줘.\n\n"
            "화면 구성\n- PDF 파일을 올리는 자리\n- 청킹 전략 선택(고정 길이 · 구조 경계 · 문단) 과 청크 크기 입력\n- [문서 준비] 버튼 하나\n- 질문 입력창과 답변 영역\n\n"
            "[문서 준비] 를 누르면 파싱 · 청킹 · 임베딩 · 저장을 한 번에 진행해 줘.\n단계마다 사용자가 버튼을 누르지 않게 해 줘.\n"
            "진행 상황과 끝난 뒤 결과만 화면에 보여 줘.\n- 페이지 수와 페이지별로 추출된 글자 수\n- 만들어진 청크 수, 가장 긴 청크와 가장 짧은 청크\n- 텍스트가 거의 추출되지 않은 페이지가 있으면 표시",
            "Claude Code · 앞부분", sm=True) + note("이어서", "다음 장의 뒷부분까지 한 요청문으로 입력"), kick="참고 · GraphRAG 5-1"),
        page("1단계 요청문 (2/2)", prompt(
            "임베딩은 OpenAI text-embedding-3-small 을 쓰고,\n지금 사용 중인 임베딩 모델 이름과 차원을 화면에 항상 표시해 줘.\n\n"
            "질문을 입력하면 관련 청크를 검색해 상위 5개를 보여 주고,\n그 청크만 근거로 gpt-5.6-luna 가 답하게 해 줘.\n"
            "각 청크는 청크 ID · 페이지 · 본문을 확인할 수 있게 하고,\n답변에는 사용한 페이지를 표시해 줘.\n검색된 근거로 답할 수 없으면 모른다고 답하게 해 줘.\n\n"
            ".env 의 OPENAI_API_KEY 를 사용해 줘.",
            "Claude Code · 뒷부분", sm=True), kick="참고 · GraphRAG 5-1"),
        page("준비가 끝나면 화면에서 확인", two(
            pane("준비 결과", ul(["페이지별 추출 글자 수가 0에 가까우면 원본 PDF의 그 페이지 열기 · 도판이나 표만 있는 페이지일 수 있음",
                                "청크 서너 개 펼쳐 읽기 · 문장 끊김 · 다른 주제 섞임",
                                "청킹 전략을 바꿔 청크 수와 내용 비교 · 문서 생김새에 따라 맞는 전략이 다름",
                                "임베딩 모델 이름 확인 · 질문과 문서가 같은 모델이어야 점수 해석 가능"]), "good"),
            pane("질문", ul(["답이 분명히 있는 질문: 상위 청크의 관련성 · 필요한 내용의 순위 · 표시된 페이지를 원문과 대조",
                            "답이 없는 질문: 그럴듯한 답을 만드는지 · <b>모른다고 답해야 정상</b>"]), "good"))
             + note("이상하면", "답변 쪽을 고치기 전에 앞 단계부터 · 청크에 그 내용이 있는지 → 추출된 텍스트에 있는지", "red")
             + note("기본 RAG", "3교시 검색 개선(Metadata Filter · Query Rewriting · Reranking)은 지금 붙여도 됨 · 트랙의 목표는 그다음"), kick="참고 · GraphRAG 5-1"),
        page("2단계 · 한 번의 검색으로 어려운 질문", sf.chain(["RAM", "Soft Error", "검출 방법", "완화 방법", "제약"], cls="sm")
             + two(ul(["단순한 정의 검색에서 벗어나기", "<b>여러 대상과 조건을 연결해야</b> 답할 수 있는 질문", "아직 Graph를 만들지 않고 지금 RAG의 결과 관찰"]),
                   pane("관찰할 것", ul(["필요한 정보가 한 Chunk에 모두 있는가 · 여러 페이지에 흩어져 있는가", "Vector Search가 필요한 Chunk를 모두 찾았는가", "일부만 검색되어 답변이 빠지지 않았는가", "순위가 낮아 근거가 LLM에 전달되지 않은 것은 없는가"]), "good"), "w2"),
             kick="참고 · GraphRAG 5-2"),
        page("질문 예시 · A. 패키지 수분 민감도", _qs([
            ("Under what conditions does die paddle delamination in a flange-mounted package lead to actual reliability issues, and how do the placement of down-bond wires and temperature cycling affect that risk?",
             "Flange-mounted package에서 die paddle delamination이 발생했을 때, 어떤 조건에서 실제 신뢰성 문제로 이어지며 down-bond wire의 위치와 temperature cycle이 그 위험에 어떤 영향을 주나요?"),
            ("Which failure mechanisms are targeted by the mitigation methods TI proposed to reduce die paddle delamination or alleviate its impact, and what are the functional differences among reinforcing stitch bonds, improving mold adhesion, and adjusting MSL?",
             "Die paddle delamination을 줄이거나 그 영향을 완화하기 위해 TI가 제시한 방법들은 각각 어떤 failure mechanism을 대상으로 하며, stitch bond 강화·mold adhesion 개선·MSL 조정은 어떤 차이가 있나요?"),
            ("Why is electrical testing alone insufficient for evaluating the MSL of flange-mounted packages, and what is the rationale for conducting CSAM, temperature cycling, decapsulation, and stitch-bond inspection together?",
             "Flange-mounted package의 MSL 평가에서 electrical test만으로는 왜 충분하지 않으며, CSAM·temperature cycle·decap·stitch-bond inspection을 함께 수행해야 하는 이유는 무엇인가요?"),
        ]), kick="참고 · TI SLZA002"),
        page("질문 예시 · B. 소프트 에러 대응", _qs([
            ("What distinct roles do parity, scrubbing, and backup copies play in detecting and recovering from soft errors in STM32 SRAM, and how do they work together to prevent accumulated bit errors?",
             "STM32의 SRAM에서 발생하는 soft error를 탐지하고 복구하기 위해 parity, scrubbing, backup copy가 각각 어떤 역할을 하며, 이들이 함께 사용될 때 누적 bit error를 어떻게 방지하나요?"),
            ("Why is it difficult to address transient soft errors and latch-up soft errors using the same approach, and what specific hardware/software detection and compensation mechanisms correspond to each?",
             "Transient soft error와 latch-up soft error는 왜 동일한 방식으로 대응하기 어렵고, 각각 어떤 hardware/software detection 및 compensation 방식과 연결되나요?"),
            ("Which types of memory errors are targeted by ECC, parity, and the Walkpath test in STM32, and how do they differ in terms of detection-only capability versus error correction?",
             "STM32에서 ECC, parity, Walkpath test는 각각 어떤 종류의 메모리 오류를 대상으로 하며, detection-only와 correction 관점에서 어떤 차이가 있나요?"),
        ]), kick="참고 · ST AN4750"),
        page("질문 예시 · C. ESD 포장", _qs([
            ("When packaging moisture-sensitive devices using stick magazines, trays, or tape-and-reel formats, what supplementary ESD shielding elements are introduced in each method, and how do they differ from one another?",
             "수분 민감 소자를 Stick Magazine, Tray, Tape-and-Reel 방식으로 포장할 때, 각 방식에서 추가되는 ESD 차폐 요소는 무엇이며 서로 어떻게 다른가요?"),
            ("In tape-and-reel packaging, how do the material properties of the carrier tape, cover tape, and reel combine with the leader/trailer design to shield devices from external electrostatic fields, and what test results did TI use to validate this effectiveness?",
             "Tape-and-Reel 포장에서 carrier tape, cover tape, reel의 재료 특성과 leader/trailer 구조가 어떻게 결합되어 외부 정전기장으로부터 소자를 보호하며, TI는 그 효과를 어떤 시험 결과로 확인했나요?"),
            ("How do the ESD protection requirements of JESD625-A and EIA-541 translate into TI's packaging material selection and testing standards, and why did TI conclude that actual shielding effectiveness is more critical than simple surface resistance values?",
             "JESD625-A와 EIA-541의 ESD 보호 요구사항은 TI의 포장재 선택과 시험 기준에 어떻게 연결되며, 왜 TI는 단순한 표면저항 값보다 실제 shielding effectiveness가 더 중요하다고 결론 내렸나요?"),
        ]), kick="참고 · TI SZZA027A"),
        page("검색 결과만으로 보이지 않는 연결", '<div class="quote">검색 결과에 여러 개의 사실이 나와도<br><span class="hl">어떤 정보와 어떤 정보가 연결되는지</span>는<br>검색 결과만으로 알기 어려움</div>'
             + note("여기서부터", "GraphRAG 추가", "red"), kick="참고 · 생각해 볼 것"),
        page("3단계 · 문서 안의 관계를 Graph로", sf.triples()
             + note("함께 저장", "관계마다 <b>문서명 · 페이지 · Chunk ID · 근거가 된 원문 문장</b>", "red")
             + note("이유", "필요한 사실이 여러 페이지에 흩어져 있고, 어떻게 이어지는지는 유사도 검색 결과만으로 드러나지 않음"), kick="참고 · GraphRAG 5-3"),
        page("실습 환경과 진행 방향", two(
            ul(["보통은 전용 추출 모델 · Graph DB 인프라 활용", "이번 실습: 한정된 시간 · <b>OpenAI API만</b> 사용", "→ LLM의 문맥 추론으로 텍스트에서 직접 관계 도출", "완성된 프롬프트 복사 대신 직접 작성 · 테스트 · 개선"]),
            steps([("스키마 정하기", "노드 · 관계 유형"), ("프롬프트 조립", "4개 블록"), ("단일 청크 테스트", "LLM 창에서"),
                   ("검증 · 수정", "반복"), ("추출 자동화", "Claude Code")])), kick="참고 · GraphRAG 5-3"),
        page("① 스키마 먼저 정하기", two(
            pane("메모장에 두 줄", ul(["<b>노드 유형</b>: 반복해서 등장하는 대상 · 부품 · 현상 · 방법 · 조건 · 시험처럼 성격으로 묶기",
                                     "<b>관계 유형</b>: 대상을 잇는 동사 · 방향 있음 · <code>A detected_by B</code>와 <code>B detects A</code>는 같은 사실 → 하나만",
                                     "각각 네다섯 개면 충분 · 늘수록 추출이 흔들리고 검증할 양만 증가"]), "good"),
            table(["문서", "노드 / 관계 (시작 예)"], [
                ["<b>A</b>", "패키지 · 손상 유형 · 시험 · 조건 · 관리 방법<br><code>causes · detected_by · mitigated_by · has_condition</code>"],
                ["<b>B</b>", "메모리 영역 · 오류 유형 · 검출 방식 · 완화 방법 · 제약<br><code>has_error · detected_by · mitigated_by · has_limitation</code>"],
                ["<b>C</b>", "포장 형태 · 재료 · 보호 특성 · 시험 방법 · 표준<br><code>made_of · provides · verified_by · complies_with</code>"]], "s7-tt"), "w2")
             + note("그대로 쓰지 않기", "문서를 직접 읽으며 고치기", "red"), kick="참고 · GraphRAG 5-3"),
        page("② 프롬프트 4개 블록", cards([
            ("스키마 강제 · Constraints", "가장 중요 · 규칙을 강하게 걸어야 엉뚱한 데이터를 만들지 않음", "1"),
            ("추출 · 근거 규칙", "할루시네이션 방지 · 본문에 없는 관계를 추론해 만들지 않게", "2"),
            ("입력 데이터 명시", "문서명 · 페이지 · Chunk ID · 텍스트 원문이 들어갈 빈칸", "3"),
            ("출력 형식", "앞뒤 설명 문장 없이 JSON만 · 마크다운 코드 블록도 쓰지 않게", "4"),
        ], 2) + note("핵심", "「너는 ~한 전문가다」 같은 역할 부여보다 <b>명확한 제약 사항과 스키마 규칙</b>", "red"), kick="참고 · GraphRAG 5-3"),
        page("블록 1 · 2 예시 문장", prompt(
            "노드 유형은 반드시 [부품, 현상, 방법, 조건] 중 하나만 사용해야 한다. 관계 유형은 [causes, detected_by, mitigated_by] 중 하나만 사용하며, 이 목록에 없는 대상이나 관계가 도출되면 해당 데이터는 과감히 버린다.",
            "블록 1 · 스키마 강제")
             + prompt("관계 하나마다 그 근거가 되는 원문 문장을 그대로 옮겨 담는다. 부정(하지 않는다)과 조건(다만 ~인 경우)을 빼먹지 말고, 부정이면 관계를 만들지 말고 무시한다.",
                      "블록 2 · 추출 및 근거 규칙")
             + note("블록 3 · 4", "입력 빈칸과 JSON 출력 형식은 직접 작성"), kick="참고 · GraphRAG 5-3"),
        page("③ 단일 청크로 테스트", two(
            steps([("청크 하나 복사", "앞 단계에서 잘라 둔 텍스트 중 단 하나"), ("LLM 창 열기", "ChatGPT 웹 화면 또는 Claude 등"),
                   ("붙여 넣고 실행", "추출 프롬프트 아래에 청크 1개")]),
            pane("하나씩 넣는 이유", ul(["한 번에 넣으면 입력이 길어져 뒷부분 추출이 성글어짐", "결과가 이상할 때 어느 청크, 프롬프트의 어느 줄 때문인지 바로 찾아 수정"]), "good"))
             + note("주의", "코드를 짜고 문서 전체를 한 번에 API로 돌리는 것은 위험", "red"), kick="참고 · GraphRAG 5-3"),
        page("④ 결과 검증 · 프롬프트 수정", table(["증상", "수정"], [
            ["<b>관계가 거의 안 나옴</b>", "스키마가 문서 표현과 맞지 않음 · 청크를 직접 읽고 실제 쓰인 동사로 관계 유형 변경"],
            ["<b>문서에 없는 말이 섞임</b>", "근거 문장을 원문 그대로 옮기게 하고, 옮길 문장이 없으면 관계를 버리라고 블록 2에 명시"],
            ["<b>JSON 형식이 깨짐</b>", "출력 형식 앞에 「부연 설명 없이 JSON만 출력할 것」 · 예시 JSON 포맷을 더 꼼꼼하게"],
            ["<b>같은 대상이 다른 이름으로</b>", "스키마 영역에 「목록에 있는 대표 이름(대소문자 통일)으로 통일한다」 추가"],
        ]) + note("반복", "프롬프트 수정 → 다시 테스트", "red"), kick="참고 · GraphRAG 5-3"),
        page("⑤ 추출 자동화 · Claude Code 요청 조건", table(["조건", "요청할 내용"], [
            ["<b>핵심 동작</b>", "<code>prompt_extract.txt</code>의 프롬프트로 저장된 청크를 OpenAI API에 보내 관계 추출"],
            ["<b>속도 최적화</b>", "<code>asyncio</code> 등으로 비동기 병렬 호출"],
            ["<b>예외 처리</b>", "JSON 파싱 실패 청크는 1회만 재시도 · 그래도 실패하면 <code>failed_chunks.json</code>에 기록"],
            ["<b>데이터 병합</b>", "대소문자 · 앞뒤 공백을 맞춰 합치기 · 같은 관계의 근거 문장은 모두 보존 · <code>graph.json</code>"],
            ["<b>화면 출력</b>", "터미널에 총 노드 수 · 관계 수 · 총 API 호출 횟수"],
            ["<b>검증용 표</b>", "그래프 그림 대신 <code>[출발 노드 / 관계 / 도착 노드 / 페이지 / 근거 문장]</code> 표"],
        ], "s7-tt") + note("시작 조건", "청크에서 원하는 관계와 근거를 정확히 뽑는다는 확신 → 프롬프트를 파일로 저장 · 청크 수백 개는 순차 처리하면 너무 오래 걸림", "red"),
             kick="참고 · GraphRAG 5-3"),
        page("4단계 · Graph 검색 흐름", sf.chain([("사용자 질문", ""), ("시작 Node 찾기", "질문에서"), ("1~2 hop 관계 탐색", "RAM → Soft Error → Detection Method"),
                                                ("원문 근거 수집", "탐색된 관계"), ("LLM에 전달", ""), ("업무 결과물 + 출처", "")], hl=(2,))
             + note("차이", "관련 Chunk를 찾는 데서 끝나지 않고, 핵심 대상에서 출발해 관계망을 따라가며(Hop) 답변의 단서 수집", "red"), kick="참고 · GraphRAG 5-4"),
        page("① 최종 개발 프롬프트 설계", three(
            pane("검색 전략", ul(["질문에서 시작 Node를 어떻게 찾을까", "보조로 Vector Search를 쓸까", "몇 hop까지 따라갈까"]), "good"),
            pane("근거 처리", ul(["관계의 문서명 · 페이지 표시", "원문을 쉽게 확인하는 방법", "연결된 정보가 없을 때 대처"]), "good"),
            pane("결과물 형태", ul(["A: 보관 · 취급 검토표", "B: 검출 · 완화 · 제약 비교서", "C: 포장 · 재료 · 시험 · 보호 특성 체크리스트"]), "good"))
             + note("작성 방식", "앞의 내용을 복사해 합치지 말고, 위 질문의 답을 고민하며 직접 작성", "red"), kick="참고 · GraphRAG 5-4"),
        page("② 화면 출력 흐름", flow([("시작 Node", "예: RAM"), ("탐색 경로", "RAM → Soft Error → Detection Method"),
                                    ("사용한 근거", "페이지 · Chunk ID · 원문"), ("최종 업무 결과물", "비교서 · 체크리스트")], hl=1)
             + note("요청", "최종 답변만 내놓지 않게 · 실제로 Graph를 탐색했는지 추적할 수 있도록 답변 전에 순서대로 출력", "red"), kick="참고 · GraphRAG 5-4"),
        page("③ GraphRAG 검증 테스트", table(["질문 유형", "확인할 것"], [
            ["<b>단일 근거</b>", "하나의 문서 · 페이지로 답할 수 있는 질문 · 기본 RAG로도 쉽게 해결되는지"],
            ["<b>다중 관계 탐색</b> (핵심)", "여러 노드와 관계를 넘어가야 완성 · 실행 로그에서 실제로 1~2 hop 따라갔는지"],
            ["<b>문서에 없는 질문</b>", "관계나 답을 지어내지 않고 「연결된 근거가 없습니다」라고 반응하는지"],
        ]) + note("가장 중요한 것", "그럴듯한 결과보다 <b>어떤 관계와 원문을 따라 도달했는지</b> 투명하게 확인", "red"), kick="참고 · GraphRAG 5-4"),
        page("성능 테스트 질문 예시", three(
            '<div class="s7-pqh">A. 패키지 수분 민감도<small>TI SLZA002</small></div><div class="s7-pq">'
            + "".join(f"<div><code>{q}</code><span>{p}</span></div>" for q, p in [
                ("what causes delamination?", "6·7쪽"), ("delamination mitigation techniques", "9·13쪽"),
                ("MSL testing procedure", "8쪽"), ("mold compound and die paddle", "6·7쪽"),
                ("down bond wire failure", "7·10쪽"), ("how to improve stitch bond strength?", "9쪽")]) + "</div>",
            '<div class="s7-pqh">B. 소프트 에러 대응<small>ST AN4750</small></div><div class="s7-pq">'
            + "".join(f"<div><code>{q}</code><span>{p}</span></div>" for q, p in [
                ("what causes soft errors in SRAM?", "8쪽"), ("parity vs ECC for SRAM protection", "14·18쪽"),
                ("scrubbing and backup copy for parity error recovery", "16·17쪽"), ("structural, functional, temporal and informational redundancy", "11쪽"),
                ("diagnostic coverage and safe failure fraction", "7쪽"), ("Class B IEC 60335 methods supported by STM32 hardware", "13·14쪽")]) + "</div>",
            '<div class="s7-pqh">C. ESD 포장<small>TI SZZA027A</small></div><div class="s7-pq">'
            + "".join(f"<div><code>{q}</code><span>{p}</span></div>" for q, p in [
                ("stick magazine, tray, and tape-and-reel ESD configurations", "5~9쪽"), ("Faraday shield formed by the intermediate container", "6·7쪽"),
                ("surface resistivity requirements for carrier tape and reel", "10~13쪽"), ("triboelectric charging and antistatic cover tape tests", "11·12쪽"),
                ("20 kV charged plate test on loaded tape and reel", "9·10쪽"), ("JESD625-A and EIA-541 requirements for ESD protective packing", "3·4쪽")]) + "</div>"),
            kick="참고 · GraphRAG 5-4"),
        page("성능 테스트 질문 · 확인할 내용", table(["문서", "질문별로 확인할 내용"], [
            ["<b>A</b>", "박리의 원인 인자 · 완화 기법 전반 · bake → soak → reflow → CSAM 절차 · 몰드 컴파운드와 다이 패들의 계면 · 다운본드 와이어 파단 · BSB / SSB / RSSB"],
            ["<b>B</b>", "알파 · 중성자 플럭스, EMI, 130 nm 이하 미세화 · 검출만 되는 방식과 정정까지 되는 방식 · 백그라운드 스크러빙과 복원 절차 · 중복성 4분류 · DC · SFF 정의와 계산식 · 규격 항목과 하드웨어 기능 대응"],
            ["<b>C</b>", "세 방식의 구성 차이 · 중간 용기의 차폐 형성 방식 · 10⁴~10¹¹ Ω/□ 규격과 실측값 · 필링 · 언롤링 시험, 180 V 한계 · ±20 kV 6방향 노출, 차폐 효율 95% · 인용 규격과 적용 범위"],
        ], "s7-tt"), kick="참고 · GraphRAG 5-4"),
        page("GraphRAG 실행 예", img(IMG + "graphrag_run.png", "what causes delamination? · 시작 노드 5 · 탐색된 노드 40 · 관계 57", light=True), kick="참고 · GraphRAG"),
    ]


def closing():
    return [
        page("정리", steps([
            ("제출 준비", "플랫폼 가입 · 프로필 실명 · 8교시에 결과 페이지 제출"),
            ("목표는 완료 조건까지", "입력 · 결과물 · 판단 · 완료와 중단 · 실행 범위"),
            ("작게 시작해 단계마다 확인", "핵심 기능 하나 · Tool 1~2개 · 단계별 요청 후 화면 확인"),
            ("근거가 보이는 결과물", "Tool 호출과 반환값 · 근거 페이지 · 탐색 경로를 화면에"),
            ("보안", "공개 문서와 가상 데이터 · 이어지는 대화에서도 입력 내용 확인"),
        ])),
        section("다음", "8교시 · 캡스톤 2", "완성과 제출 · 실제 실행 결과를 정리해 제출"),
    ]


def slides():
    return opening() + block_platform() + block_topics() + block_check() + block_agent() + block_rag() + block_graph() + closing()
