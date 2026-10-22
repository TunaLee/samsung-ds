"""부록 · Claude Code 명령어 사용법 모음 (원본: 노션 「Claude Code 명령어 사용법 모음」)."""
import s9_fig as f9
from kit import (cards, cover, esc, note, page, pane, prompt, section, table, two, ul)

TITLE = "부록 · Claude Code 명령어 사용법 모음"


def k(*xs):
    """명령 표기: 원문 그대로 code로 감싼다."""
    return " · ".join(f"<code>{esc(x)}</code>" for x in xs)


def T(rows, head=("명령", "하는 일"), cls=""):
    return table(list(head), rows, ("s9-t " + cls).strip())


def opening():
    return [
        cover(["부록", "Claude Code <em>명령어</em> 사용법 모음"],
              "수업에서 쓰는 터미널 · 대화 중 명령 · 단축키 · MCP 관리를 용도별로 정리",
              [("기준", "2026-09-08 공식 문서 · CLI 2.1.263"), ("환경", "Windows PowerShell · 교육 실습 폴더"), ("확인", "claude --help · /help")], "부록"),
        page("입력 위치", f9.where()
             + note("일반 요청", "같은 대화 입력창에 자연어로")
             + note("구분", "Claude Code를 조작하는 명령 · 실습 앱의 OpenAI API 모델과 앱 자체의 MCP 설정은 자동으로 바뀌지 않음", "red"), kick="부록"),
        page("표기 읽는 법", T([
            ["<code>&lt;경로&gt;</code>", "꺾쇠 · 실제 값으로 바꾸기", k("claude attach <ID>")],
            ["<code>[이름]</code>", "대괄호 · 생략 가능", k("/clear [이름]")],
            ["꺾쇠 · 대괄호 자체", "입력하지 않음", ""],
            ["<code>samsung_YYYYMMDD</code>", "교육 당일 날짜로", k(r"C:\samsung_YYYYMMDD\myapp")],
        ], ("표기", "뜻", "예"))
             + note("버전 차이", "계정 · 운영체제 · 설치 버전 · 활성화된 기능에 따라 메뉴와 지원 범위가 다름 → 설치본의 <code>claude --help</code>와 대화창의 <code>/help</code> 함께 확인", "red")
             + note("공식 참고", "CLI reference · Commands · Interactive mode"), kick="부록"),
        page("구성", cards([
            ("시작과 대화", "시작 · 종료 · 컨텍스트 · 되돌리기", "01"), ("지침 · 모델 · 권한", "CLAUDE.md · 계획과 모델 · 권한 모드", "02"),
            ("입력 · 단축키", "줄 바꿈 · 중단 · 파일 지정", "03"), ("MCP · Skill", "서버 등록 · 상태 관리 · Skill 사용", "04"),
            ("로그인 · 진단", "로그인 · 업데이트 · 문제 진단", "05"), ("주의와 순서", "바뀐 명령 · 수업 중 순서", "06"),
            ("실습별 요청 예시", "1 ~ 6교시 · 평소 말하듯 쓴 요청문", "07"),
        ], 4)
             + note("전체 목록", "수업에서 쓰는 명령만 모음 · 자동화 · CLI 옵션 · Plugin 제작 등은 공식 문서 <b>code.claude.com/docs</b> 와 <code>claude --help</code>", "red"), kick="부록"),
    ]


def block_start():
    kk = "시작과 대화"
    return [
        section("01", "시작과 대화", "시작 · 종료 · 다시 열기 · 컨텍스트 · 복구"),
        page("세션 시작", T([
            [k(r"cd C:\samsung_YYYYMMDD\myapp"), "작업할 폴더로 이동 · 이어서 <code>claude</code> 실행 → 이 폴더 기준", k(r'cd "C:\실습 자료\myapp"') + " 공백 경로"],
            [k("claude"), "대화형 세션 시작", "「이 프로젝트의 실행 방법을 찾아 설명해 주세요.」"],
            [k('claude "요청"'), "첫 요청과 함께 시작 · 응답 뒤에도 대화 이어짐", k('claude "이 프로젝트의 폴더 구조를 설명해 주세요."')],
            [k("claude -p", "--print"), "한 번 처리 · 결과 출력 후 종료", k('claude -p "README를 읽고 실행 절차를 요약해 주세요."')],
            [k("claude --version", "-v"), "버전 확인", ""],
            [k("claude --help", "-h"), "실행 옵션 · 하위 명령 확인", k("claude mcp add --help")],
        ], ("명령", "하는 일", "예"), "s9-wrap")
             + note("-p", "파일 수정 · 도구 실행도 요청 내용과 권한에 따라 일어날 수 있음", "red"), kick=kk),
        page("다시 열기 · 종료", T([
            [k("claude -c", "--continue"), "현재 폴더의 최근 대화 이어가기", ""],
            [k("claude -r", "--resume"), "이전 대화 선택 화면 · 이름이나 세션 ID 지정", k("claude -r 환율앱")],
            [k("claude -n", "--name"), "찾기 쉬운 이름 붙여 시작 · 작업 중에는 <code>/rename</code>", k("claude -n 환율앱")],
            [k("claude -c --fork-session"), "최근 대화 바탕 · 새 세션 ID · 다른 방향 시험", ""],
            [k("/exit", "/quit"), "대화형 CLI 종료", ""],
        ], ("명령", "하는 일", "예"))
             + note("--fork-session", "대화만 분리 · 파일 작업 폴더까지 분리하려면 worktree 따로 사용")
             + note("/exit", "백그라운드 세션 접속 중이면 연결만 해제 · 작업은 계속될 수 있음", "red"), kick=kk),
        page("컨텍스트 관리", T([
            [k("/clear [이름]"), "새 대화 시작 · 이름을 주면 이전 대화에 남김 · 별칭 <code>/new</code> <code>/reset</code>"],
            [k("/compact 지시"), "현재 대화 요약 · 컨텍스트 공간 확보 · 같은 작업 계속"],
            [k("/context"), "컨텍스트 사용량 · 큰 비중 항목 · <code>/context all</code> 상세"],
            [k("/autocompact"), "자동 요약 기준 확인 · <code>/autocompact 500k</code> · <code>/autocompact auto</code>"],
        ]) + prompt("/compact 실행 포트와 해결하지 못한 오류를 유지해 주세요.", "Claude Code · 유지할 내용 지정")
             + note("/clear", "이미 수정한 파일은 그대로 남음")
             + note("/autocompact", "지원 범위 → 모델과 버전에서 확인"), kick=kk),
        page("되돌리기와 분기", T([
            [k("/rewind"), "체크포인트 선택 → 코드 · 대화 · 둘 다 복원, 또는 대화 일부 요약 · 별칭 <code>/checkpoint</code> <code>/undo</code>"],
            [k("Esc") + " 두 번", "입력창이 비어 있을 때 복구 메뉴"],
            [k("/branch 다른-설계"), "현재 대화에서 분기 · 원래 대화는 <code>/resume</code>으로"],
        ]) + note("복구 범위", "Claude의 파일 편집 도구가 추적한 변경만 · 셸 명령 · 외부 프로그램 · 대부분의 Subagent 변경은 모두 복원 못 함 → Git 커밋과 함께", "red")
             + note("/branch", "대화 분기 · 파일 작업 폴더 자동 분리 아님")
             + note("공식 참고", "Checkpointing · Memory · Commands"), kick=kk),
        page("상황별 정리 명령", f9.tidy(), kick=kk),
    ]


def block_settings():
    kk = "지침 · 모델 · 권한"
    return [
        section("02", "지침 · 모델 · 권한", "프로젝트 지침 · 계획과 모델 · 권한 모드"),
        page("프로젝트 지침", T([
            [k("/init"), "프로젝트를 살펴 <code>CLAUDE.md</code> 초기 지침 생성 · 실행 방법 · 테스트 명령 · 코드 구조 · 작업 규칙"],
            [k("/memory"), "<code>CLAUDE.md</code>와 자동 메모리 확인 · 관리"],
            [k("CLAUDE.md"), "프로젝트 지침 파일 · 저장소 루트 지침과 하위 폴더 지침 분리 가능"],
            [k(".claude/rules/"), "주제별 규칙 관리"],
        ]) + note("구분", "새 대화에도 유지할 지침 → 파일 · 일회성 요청 → 대화", "red")
             + note("지침 ≠ 권한", "지침 파일은 실행 권한을 강제하는 설정과 구분")
             + note("공식 참고", "프로젝트 메모리와 지침 · Settings · Hooks"), kick=kk),
        page("계획과 모델", T([
            [k("/plan 요청"), "Plan 모드로 계획 · 구현 전에 대상 파일과 검증 방법 확인", k("/plan 환율 데이터 적재 구조의 개선안을 작성해 주세요.")],
            [k("/model"), "모델 선택 화면 · 별칭 지정 가능", k("/model sonnet")],
            [k("claude --model sonnet"), "CLI 시작 때만 지정", ""],
            [k("/effort high"), "추론 수준 · <code>/effort status</code> 확인 · <code>/effort auto</code> 자동값", ""],
            [k("/advisor [모델 또는 off]"), "작업 중 다른 모델의 조언 받기", ""],
            [k("/fast on", "/fast off"), "지원 모델의 Fast 모드 · 계정 사용 조건 확인", ""],
        ], ("명령", "하는 일", "예"), "s9-wrap")
             + note("/effort 수준", "<code>low</code> · <code>medium</code> · <code>high</code> · <code>xhigh</code> · <code>max</code> · <code>ultracode</code> · 지원 여부와 유지 범위는 모델 · 버전별"), kick=kk),
        page("권한 모드", T([
            [k("manual", "default"), "일반 승인 모드"],
            [k("acceptEdits"), "파일 편집 승인 자동 처리"],
            [k("plan"), "조사와 계획 중심"],
            [k("auto"), "지원 환경에서 동작별 승인 판단 자동화"],
            [k("dontAsk"), "승인 질문이 필요한 동작은 거부"],
            [k("bypassPermissions"), "일반 권한 확인 건너뜀"],
        ], ("모드", "동작"))
             + note("Shift+Tab", "권한 모드 순환 · 화면에 표시된 현재 모드 확인 · 사용 가능한 모드는 계정과 환경별")
             + note("bypassPermissions", "파일 수정 · 명령 실행 전 사람이 검토할 기회 감소", "red"), kick=kk),
    ]


def block_keys():
    kk = "입력 · 단축키"
    return [
        section("03", "입력 · 단축키", "보내기 · 줄 바꿈 · 중단 · 파일 지정"),
        page("입력과 중단", two(T([
            [k("Enter"), "요청 보내기"],
            [k("Shift+Enter", "Ctrl+Enter"), "줄 바꿈 · OS 환경별"],
            [k("Ctrl+J") + " · <code>\\</code> 뒤 " + k("Enter"), "줄 바꿈이 안 될 때"],
            [k("Esc"), "응답 중단 · 대화상자 닫기"],
            [k("Esc") + " 두 번", "빈 입력창: 복구 메뉴 · 입력 중: 초안 지우기"],
            [k("Ctrl+C"), "실행 중단 · 대기 중 입력 지우기 · 다시 누르면 종료"],
            [k("Ctrl+D"), "빈 입력창: 종료 안내 → 다시 눌러 종료 · 입력 중: 커서 뒤 문자 삭제"],
        ], ("키", "하는 일"), "s9-wrap"), T([
            [k("↑", "↓"), "입력 이력 탐색"],
            [k("Ctrl+R"), "이전 입력 검색"],
            [k("Tab"), "경로 · 명령 자동완성"],
            [k("@lab/registry.py"), "파일 지정해 질문"],
            [k("!git status"), "셸 명령 직접 실행 · 출력을 대화에 포함"],
            [k("?"), "빈 입력창에서 단축키 도움말"],
        ], ("키 · 입력", "하는 일")) + prompt("@lab/registry.py 에서 도구 목록을 합치는 과정을 설명해 주세요.", "Claude Code · @파일 예", sm=True))
             + note("Ctrl+C", "중단 전에 끝난 파일 변경은 남음", "red")
             + note("!", "<code>!</code> 뒤 구문은 Claude Code가 사용하는 셸에 맞춤"), kick=kk),
    ]


def block_ext():
    kk = "MCP · Skill"
    return [
        section("04", "MCP · Skill", "서버 등록 · 상태 관리 · Skill 사용"),
        page("MCP 서버 등록", prompt("claude mcp add --transport http --scope project mslearn https://learn.microsoft.com/api/mcp", "PowerShell · 프로젝트용 원격 MCP 서버", sm=True)
             + prompt(r"claude mcp add --transport stdio my-server -- python C:\samsung_YYYYMMDD\my-server\server.py", "PowerShell · 로컬 Python 서버 구문 예", sm=True)
             + note("확인", "실제 연결과 도구 노출 → Claude Code 안에서 <code>/mcp</code>")
             + note("--", "<code>--</code> 뒤는 서버 프로세스의 명령과 인자 · 서버 파일이 실제로 있고 stdio MCP 서버로 구현되어 있어야 함", "red"), kick=kk),
        page("MCP 상태 관리", T([
            [k("claude mcp list"), "등록 목록 · 연결 상태"],
            [k("claude mcp get mslearn"), "특정 서버 설정 · 프로젝트 서버는 최초 승인 전까지 대기 가능"],
            [k("claude mcp login <서버명>", "logout"), "OAuth 인증 · 저장된 인증 해제 · 인증 요구 서버"],
            [k("/mcp"), "연결 · 도구 · 인증 상태 관리"],
            [k("/mcp reconnect mslearn"), "재연결"],
            [k("/mcp disable mslearn", "enable"), "비활성화 · 다시 활성화 · 지원 버전에서 <code>all</code>"],
            [k("claude mcp remove mslearn"), "등록 제거 · 같은 이름이 여러 범위면 <code>--scope project</code>처럼 명시"],
        ], cls="s9-wrap")
             + note("일시 중지", "제거 대신 <code>/mcp disable</code>"), kick=kk),
        page("Skill 사용과 위치", T([
            [k("/skills"), "사용할 수 있는 Skill 확인"],
            [k("/reload-skills"), "변경한 Skill · 명령 디렉터리 다시 읽기"],
            [k("/skill-doctor"), "Skill 사용 빈도와 컨텍스트 비용 점검"],
            [k(".claude/skills/<이름>/SKILL.md"), "프로젝트 Skill 기본 위치 · <code>/이름</code>으로 호출"],
            [k("~/.claude/skills/<이름>/SKILL.md"), "개인 공통 위치"],
            [k(".claude/commands/<이름>.md"), "기존 사용자 명령 형식 · 현행 Skill과 함께 지원 · 새 절차는 <code>SKILL.md</code>"],
            [k("/plugin-name:skill-name"), "Plugin Skill · 이름 공간 포함"],
        ]), kick=kk),
    ]


def block_misc():
    kk = "로그인 · 진단"
    return [
        section("05", "로그인 · 진단", "로그인 · 업데이트 · 문제 진단"),
        page("로그인 · 업데이트 · 진단", T([
            [k("claude auth login", "logout", "status"), "PowerShell에서 로그인 · 로그아웃 · 인증 상태 · 대화 안에서는 <code>/login</code> <code>/logout</code>"],
            [k("claude setup-token"), "구독 기반 장기 인증 토큰 설정"],
            [k("claude doctor"), "설치 상태 읽기 전용 진단"],
            [k("/doctor", "/checkup"), "세션 안에서 설정 · 설치 문제 분석 · 확인 후 수정 제안"],
            [k("claude update", "claude upgrade"), "업데이트 확인 · 설치"],
            [k("claude install stable", "latest", "<버전>"), "네이티브 빌드 설치 대상 지정"],
            [k("/release-notes"), "버전별 변경 내용"],
        ], cls="s9-wrap"), kick=kk),
    ]


def block_close():
    kk = "주의와 순서"
    return [
        section("06", "주의와 순서", "오래된 안내의 바뀐 명령 · 수업 중 자주 쓰는 순서"),
        page("바뀐 명령", T([
            [k("/vim"), "삭제 → <code>/config</code>의 Editor mode에서 Vim · Normal"],
            [k("/pr-comments"), "삭제 → 「현재 PR의 검토 댓글을 읽고 남은 작업을 정리해 주세요.」처럼 요청"],
            [k("/ultraplan"), "삭제 → <code>/plan</code>"],
            [k("/agents"), "과거 대화형 관리 화면 → 자연어 요청 또는 Agent 파일 편집"],
            [k("/fork"), "현행 기본: 별도 백그라운드 세션 복사 · 결과를 받는 하위 작업은 <code>/subtask</code> · Agent view 설정별 예외"],
            [k("/review"), "현행 <code>/code-review</code>의 별칭"],
            [k("/cost", "/stats"), "<code>/usage</code>로 통합된 별칭"],
            [k("/extra-usage"), "→ <code>/usage-credits</code>"],
            [k("--enable-auto-mode"), "제거 → 지원 환경에서 <code>--permission-mode auto</code>"],
        ], ("과거 안내", "현행"), "s9-wrap"), kick=kk),
        page("Unknown command가 나오면", T([
            ["입력 위치", "PowerShell인지 대화 입력창인지"],
            ["철자", "명령 이름 다시 확인"],
            ["버전", "<code>claude --version</code> · <code>/release-notes</code>"],
            ["사용 가능 명령", "<code>/help</code>"],
            ["계정 · 플랫폼", "지원 조건 확인"],
            ["Skill · Plugin 명령", "설치 여부 · <code>/reload-skills</code> · <code>/reload-plugins</code>"],
        ], ("확인", "방법"))
             + note("공식 참고", "Commands의 변경 · 삭제 안내 · CLI reference"), kick=kk),
        page("수업 중 자주 쓰는 순서", T([
            ["시작", "실습 폴더로 <code>cd</code> → <code>claude</code> → <code>/status</code>로 계정 · 모델 확인 → 처음이면 <code>/init</code> 후 지침 검토"],
            ["기능 개발", "입력 · 출력 · 완료 조건을 자연어로 → 큰 변경이면 <code>/plan</code> → 구현 후 <code>/diff</code>와 앱 실행으로 확인"],
            ["오류 대응", "오류 원문과 재현 순서 → 필요하면 <code>@파일</code> → 길어지면 <code>/context</code> · <code>/compact</code> → 잘못된 수정은 <code>/rewind</code> 복원 범위 확인"],
            ["다음 작업", "<code>/rename</code> → 새 주제는 <code>/clear</code> → 종료 <code>/exit</code> → 돌아오면 <code>claude -c</code> · <code>claude -r</code>"],
            ["MCP 실습", "Claude Code: <code>claude mcp add</code> · <code>/mcp</code> · 제작 중인 앱: 앱 코드 · 설정 변경 요청 → 앱 화면에서 확인"],
        ], ("상황", "순서"), "s9-wrap"), kick=kk),
    ]



def _ex(*items):
    """요청 예시 여러 개를 세로로. items: (라벨, 요청문)."""
    return '<div class="s9-ex">' + "".join(prompt(t, l, sm=True) for l, t in items) + "</div>"


def block_examples():
    kk = "실습별 요청 예시"
    return [
        section("07", "실습별 요청 예시", "정답 문장 없음 · 평소 말하듯 쓰면 됨"),
        page("이렇게만 들어가면 충분", two(
            ul(["<b>어디서</b> · 지금 폴더가 어느 앱인지", "<b>무엇을</b> · 만들거나 고칠 것", "<b>어떻게 보일지</b> · 화면에서 확인할 것",
                "<b>건드리지 말 것</b> · 그대로 둘 기능"]),
            _ex(("막혔을 때", "화면에 안 바뀐 것 같아. 뭘 바꿨는지 먼저 설명해 줘."),
                ("너무 많이 바뀌었을 때", "방금 바꾼 건 되돌려 줘. 한 번에 다 하지 말고 하나씩 해 보자."),
                ("오류가 났을 때", "실행했더니 아래 오류가 나와. 이유를 알려 주고 고쳐 줘.\n(오류 메시지 그대로 붙여 넣기)")), "w2"), kick=kk),
        page("1교시 · rag-sim 시작", _ex(
            ("/init 다음", "이 앱이 뭐 하는 앱인지 쉽게 설명해 줘. 내가 뭘 넣으면 어떤 순서로 처리돼서 화면에 뭐가 나오는지 알려 주고, 코드는 아직 고치지 마."),
            ("실행 준비", "이 앱 실행하려면 뭐가 필요해? 없는 게 있으면 설치해 주고, 실제로 켜지는지까지 확인해 줘.")), kick=kk),
        page("2교시 · 문장 강조 · 의미 기반 청킹", _ex(
            ("핵심 문장 강조", "검색 결과 청크가 길어서 답이 어디 있는지 찾기 힘들어. 청크를 문장으로 쪼개서 질문이랑 제일 비슷한 문장 하나만 노란색으로 칠해 주고 점수도 옆에 보여 줘. "
                              "문장 임베딩은 검색할 때만 계산하고 저장소는 다시 만들지 마. 원래 검색이랑 답변 기능은 그대로 둬."),
            ("의미 기반 청킹", "청킹 탭에 '의미 기반' 옵션 하나 추가해 줘. 문장 단위로 나눈 다음, 옆 문장끼리 얼마나 비슷한지 계산해서 갑자기 확 달라지는 곳에서 잘라 줘. "
                              "기준값이랑 최소 · 최대 길이는 화면에서 바꿀 수 있게 하고, 미리보기에서 자른 곳마다 유사도 숫자도 보여 줘. 원래 청킹 방식은 그대로 둬.")), kick=kk),
        page("2교시 · BM25 · 하이브리드", _ex(
            ("BM25", "검색 화면에 단어로 찾는 BM25 검색도 붙여 줘. 지금 검색 결과랑 BM25 결과를 왼쪽 오른쪽에 나란히 보여 주고, 답변 만들기를 누르면 각각 따로 답변을 만들어 줘."),
            ("하이브리드", "의미 검색이랑 BM25를 합친 검색도 만들어 줘. 둘은 점수 단위가 달라서 그냥 더하면 안 되니까 순위로 합쳐 줘. 세 가지 결과를 세 칸으로 나란히 보여 줘."),
            ("더 해보기 · Parent-Child", "작은 조각으로 찾고, 답변 만들 땐 그 조각이 속한 큰 단락 전체를 넘기는 방식도 해 보고 싶어. 원래 검색은 그대로 두고 옵션으로 추가해 줘.")), kick=kk),
        page("3교시 · 질의 재작성", _ex(
            ("Query Rewriting", "검색하기 전에 질문을 문서에 맞게 바꿔 주는 기능을 넣어 줘. 문서가 영어니까 한국어 질문은 영어 검색 문장으로 바꾸되 원래 단어도 같이 넣고, 질문에 없던 조건이나 숫자는 절대 붙이지 마. "
                                "검색에는 바꾼 문장을, 답변에는 원래 질문을 써 줘. 켜고 끌 수 있게 하고, 원래 질문이랑 실제로 검색한 문장을 화면에 같이 보여 줘. 바꾸다 실패하면 실패했다고 알려 주고 원래 질문으로 검색해 줘.")), kick=kk),
        page("3교시 · 재정렬", _ex(
            ("1단계 · 점수 계산", "검색 후보를 다시 줄 세우는 기능을 만들고 싶어. 지금 검색 설정 그대로 후보를 한 번만 모으고, 후보 하나씩 gpt-5.4-mini에게 '이게 질문의 근거가 되면 Y, 아니면 N으로 시작해'라고 물어 줘. "
                              "추론은 끄고 답은 최대한 짧게, 첫 토큰의 logprobs로 P(Y) ÷ (P(Y) + P(N)) 점수를 내 줘. Y도 N도 안 나오거나 호출이 실패하면 '재정렬 실패'로 표시해 줘."),
            ("2단계 · 화면과 비교", "이제 재정렬 켜기 · 끄기, 후보 수 10 · 20 · 30개, 기준값(처음엔 0.5)을 화면에 넣어 줘. 기준값 못 넘는 후보는 빼고, 하나도 안 남으면 답변 대신 '문서에서 관련 근거를 찾지 못했습니다'를 보여 줘. "
                                "같은 후보로 원래 순서 상위 5개와 재정렬 상위 5개 답변을 나란히 비교하게 해 주고, 후보마다 점수랑 순위가 어떻게 바뀌었는지도 보여 줘.")), kick=kk),
        page("4교시 · agent-sim", _ex(
            ("실행 준비", "여기는 agent-sim 폴더야. 실행하는 데 필요한 걸 확인해서 준비해 주고 켜지는지 봐 줘."),
            ("코드 읽기", "코드는 건드리지 말고 설명만 해 줘. memo_tool_2라는 도구 이름이 note_save 함수랑 어디서 연결되는지, AI에게는 어떤 정보만 보내는지, AI가 도구를 쓰겠다고 하면 어디서 실제로 실행되는지 개발자가 아니어도 알아듣게 알려 줘."),
            ("메모 수정 도구", "메모를 고치는 도구 memo_tool_4를 추가해 줘. 키워드로 메모를 찾아서 내용을 새로 바꾸는 거야. 도구 목록에 보이게 하고 설명문도 화면에서 고칠 수 있게 해 줘. 입력이 이상하면 어떻게 넣어야 하는지 알려 주는 오류를 돌려줘.")), kick=kk),
        page("5교시 · 검색 API · rag_search", _ex(
            ("검색 API", "rag-sim 검색을 다른 프로그램에서도 쓸 수 있게 해 줘. 127.0.0.1:8780/api/search?query=질문&top_k=5 로 부르면 청크 ID, 문서명, 페이지, 본문, 점수를 JSON으로 돌려주면 돼. 검색은 지금 있는 코드를 그대로 써. "
                         "'API · MCP 관리' 탭을 하나 만들어서 이 서버를 켜고 끌 수 있게 하고(처음엔 꺼진 상태), 언제 무엇을 검색했고 성공했는지 기록도 남겨 줘. 기존 화면은 그대로 둬."),
            ("rag_search", "방금 만든 검색 API를 부르는 rag_search 함수를 rag_mcp 폴더에 만들어 줘. question을 받아 query로 넘기고 결과를 그대로 돌려주면 돼. 서버가 꺼져 있으면 실패라고 알려 주고. "
                           "아직 서버는 만들지 말고, 도구 이름 · 설명 · 입력 형식이 어떻게 보이는지만 보여 줘.")), kick=kk),
        page("5교시 · MCP 서버", _ex(
            ("MCP 서버", "rag_search를 MCP 서버로 내놓아 줘. 주소는 127.0.0.1:8790/mcp 이고, agent-sim의 mcp_client.py가 보내는 형식에 맞춰 줘. 관리 탭에 MCP 서버 켜기 · 끄기를 따로 두고 호출 기록도 남겨 줘. "
                         "검색 API가 꺼져 있으면 가짜 결과 말고 오류를 돌려주고, MCP를 꺼도 검색 API랑 기존 화면은 그대로 동작하게 해 줘."),
            ("동작 확인", "코드는 고치지 말고 8790 서버에 실제로 연결해서 도구 목록을 받아 보고, rag_search로 'AEC-Q100의 기계적 충격 시험은 몇 개의 샘플로 수행하나요?'를 검색해 봐. 응답 원문이랑 MCP · API 기록을 같이 보여 줘.")), kick=kk),
        page("6교시 · 조사 Agent", _ex(
            ("조사 Agent 연결", "Decisions 판정 확률이 기준값(0.5)을 넘는 이벤트만 조사 Agent에게 넘겨 줘. 판정할 때 보낸 입력을 그대로 주고, Agent는 Lot 이력이랑 정비 기록 조회 도구만 쓰게 해 줘. "
                                "결과는 그 이벤트 줄 아래에 원인 가설과 근거로 보여 주고, 어떤 도구를 어떤 값으로 불렀는지 펼쳐 볼 수 있게 해 줘. 같은 이벤트는 두 번 조사하지 말고, 감시를 멈추거나 탭을 닫으면 조사도 새로 시작하지 마.")), kick=kk),
    ]

def slides():
    return opening() + block_start() + block_settings() + block_keys() + block_ext() + block_misc() + block_close() + block_examples()
