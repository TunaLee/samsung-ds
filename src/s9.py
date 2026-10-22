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
              "터미널 실행 명령 · 대화 중 명령 · 단축키 · MCP와 Plugin 관리 · 자동화 옵션을 용도별로 정리",
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
            ("시작과 대화", "시작 · 종료 · 컨텍스트 · 복구", "01"), ("지침 · 설정 · 권한", "CLAUDE.md · 모델 · 권한 모드 · 사용량", "02"),
            ("입력 · 단축키", "줄 바꿈 · 중단 · 파일 지정 · 편집 키", "03"), ("검토와 Agent", "기본 제공 Skill · 백그라운드 · 반복 작업", "04"),
            ("MCP · Skill · Plugin", "서버 등록 · 범위 · Skill 작성 · Plugin 설치", "05"), ("외부 연결과 관리", "IDE · 원격 · 로그인 · 진단 · 기타", "06"),
            ("자동화 · CLI 옵션", "파이프 · 출력 형식 · 실행 옵션", "07"), ("주의와 순서", "바뀐 명령 · 수업 중 순서", "08"),
        ], 4), kick="부록"),
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
        page("대화 이름과 이력", T([
            [k("/help"), "사용할 수 있는 명령 확인 · 입력창 맨 앞 <code>/</code> → 검색 메뉴", ""],
            [k("/rename 환율앱-오류수정"), "현재 대화에 이름 붙이기", k("/resume 환율앱-오류수정")],
            [k("/resume [이름 또는 ID]"), "이전 대화 선택해 이어가기 · 별칭 <code>/continue</code>", ""],
            [k("/recap"), "현재 세션 한 줄 요약", ""],
            [k("/copy"), "최근 답변 복사", k("/copy 2") + " 두 번째 최근 답변"],
            [k("/export conversation.txt"), "대화를 텍스트 파일로 · 파일명 생략 → 내보내기 메뉴", ""],
            [k("/btw 이 함수는 왜 비동기인가요?"), "본 작업 중 별도 질문 · 주 대화 컨텍스트에 추가 안 함", ""],
        ], ("명령", "하는 일", "예")), kick=kk),
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
    kk = "지침 · 설정 · 권한"
    return [
        section("02", "지침 · 설정 · 권한", "프로젝트 지침 · 폴더 · 설정 파일 · 모델 · 권한 · 사용량"),
        page("프로젝트 지침", T([
            [k("/init"), "프로젝트를 살펴 <code>CLAUDE.md</code> 초기 지침 생성 · 실행 방법 · 테스트 명령 · 코드 구조 · 작업 규칙"],
            [k("/memory"), "<code>CLAUDE.md</code>와 자동 메모리 확인 · 관리"],
            [k("CLAUDE.md"), "프로젝트 지침 파일 · 저장소 루트 지침과 하위 폴더 지침 분리 가능"],
            [k(".claude/rules/"), "주제별 규칙 관리"],
        ]) + note("구분", "새 대화에도 유지할 지침 → 파일 · 일회성 요청 → 대화", "red")
             + note("지침 ≠ 권한", "지침 파일은 실행 권한을 강제하는 설정과 구분")
             + note("공식 참고", "프로젝트 메모리와 지침 · Settings · Hooks"), kick=kk),
        page("폴더와 설정 화면", T([
            [k(r"/add-dir C:\samsung_YYYYMMDD\materials_ch2"), "현재 세션이 접근할 추가 폴더 지정"],
            [k(r"/cd C:\samsung_YYYYMMDD\myapp"), "대화 유지 · 작업 폴더 이동"],
            [k("/config", "/settings"), "설정 화면 · <code>/config --help</code>로 키 확인 → <code>/config theme=dark</code>"],
            [k("/import codex --dry-run", "/import gemini --dry-run"), "다른 개발 도구 설정 가져오기 전 변경안 확인 · 지원 계정 · 환경만"],
            [k("/hooks"), "도구 호출 등 이벤트에 연결된 Hook 설정 확인"],
            [k("/statusline"), "입력창 아래 상태 표시줄 구성"],
        ], cls="s9-wrap") + note("/add-dir · /cd", "<code>/add-dir</code>: 접근 범위 추가 · <code>/cd</code>: 작업 폴더 이동 · 추가 폴더의 설정과 Plugin까지 자동 로드된다고 가정하지 않음"), kick=kk),
        page("설정 파일 위치", f9.settings_files()
             + note("가져오기", "실제 가져오기는 <code>/import</code> 안내를 따라 진행"), kick=kk),
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
        page("권한 규칙 · 사용량", two(T([
            [k("/permissions", "/allowed-tools"), "도구별 <code>allow</code> <code>ask</code> <code>deny</code> 규칙 · 접근 폴더"],
            [k("/auto-mode-setup"), "Auto 모드 환경 규칙 초안 → 검토 → 저장"],
            [k("/fewer-permission-prompts"), "반복 읽기 작업 → 허용 규칙 구성 Skill · 제안 범위 읽고 적용"],
            [k("/sandbox"), "지원 플랫폼의 Sandbox 설정 · Windows에서 일부 항목 다름"],
        ], cls="s9-wrap"), T([
            [k("/status"), "버전 · 모델 · 계정 · 연결 상태"],
            [k("/usage"), "사용량 · 제한 · 통계 · <code>/cost</code> 별칭 · <code>/stats</code> 통계 탭"],
            [k("/rate-limit-options"), "사용 한도 도달 시 선택지"],
            [k("/usage-credits"), "추가 사용량 설정 · 관리자 요청"],
            [k("/upgrade"), "상위 요금제 안내 · 표시와 결제 권한은 계정별"],
        ], cls="s9-wrap"))
             + note("공식 참고", "Permissions · Model configuration · Fast mode · Costs"), kick=kk),
    ]


def block_keys():
    kk = "입력 · 단축키"
    return [
        section("03", "입력 · 단축키", "보내기 · 줄 바꿈 · 중단 · 파일 지정 · 줄 편집"),
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
        page("화면 · 작업 · 모델 전환", two(T([
            [k("Ctrl+O"), "상세 실행 기록"],
            [k("Ctrl+L"), "화면 다시 그리기"],
            [k("Ctrl+T"), "작업 체크리스트 표시 · 숨김"],
            [k("Ctrl+B"), "실행 중 작업 백그라운드로 → <code>/tasks</code>"],
            [k("Ctrl+X") + " → " + k("Ctrl+K"), "백그라운드 Subagent 중단 · 재확인 안내"],
            [k("Ctrl+G"), "외부 편집기로 긴 입력 작성"],
            [k("Ctrl+X") + " → " + k("Ctrl+E"), "외부 편집기 (같은 기능)"],
            [k("Ctrl+S"), "입력 초안 임시 보관 · 복원"],
        ], ("키", "하는 일"), "s9-wrap"), T([
            [k("Alt+P"), "모델 선택"],
            [k("Alt+T"), "지원 모델의 Thinking 전환"],
            [k("Alt+O"), "Fast 모드 전환"],
            [k("Alt+V"), "Windows 이미지 붙여넣기"],
            [k("/keybindings"), "키 설정 파일"],
            [k("/terminal-setup"), "터미널 입력 설정"],
            ["<code>/config</code> Editor mode", "일반 · Vim 편집 모드 선택"],
        ], ("키 · 명령", "하는 일"), "s9-wrap"))
             + note("키가 안 먹으면", "터미널이 키를 가로채는 경우 · 실제 도움말 확인", "red"), kick=kk),
        page("줄 편집 키", T([
            [k("Ctrl+A", "Ctrl+E"), "줄의 처음 · 끝으로 이동"],
            [k("Ctrl+U", "Ctrl+K"), "커서 앞 · 뒤의 줄 내용 지우기"],
            [k("Ctrl+W"), "앞의 공백까지 지우기"],
            [k("Ctrl+Y"), "지운 내용 붙이기"],
            [k("Alt+B", "Alt+F"), "단어 단위 이동"],
            [k("Alt+D"), "단어 끝까지 지우기"],
            [k("Ctrl+_", "Ctrl+Shift+-"), "입력 편집 되돌리기"],
        ], ("키", "하는 일"))
             + note("공식 참고", "Interactive mode · Keybindings · Terminal configuration"), kick=kk),
    ]


def block_agent():
    kk = "검토와 Agent"
    return [
        section("04", "검토와 Agent", "기본 제공 Skill · Subagent · 백그라운드 · 반복 작업"),
        page("검토 Skill", T([
            [k("/diff"), "현재 작업 폴더의 변경 확인 · 화면 수정 후 바뀐 파일 살펴보기"],
            [k("/code-review", "/review"), "변경 코드의 문제 검토 · <code>/code-review high</code> 수준 지정 · <code>/code-review high 123</code> PR 지정"],
            [k("--fix", "--comment"), "<code>--fix</code>: 수정 적용 · <code>--comment</code>: GitHub 댓글 게시"],
            [k("/code-review ultra"), "클라우드 심층 검토 · <code>/ultrareview</code> 관련 진입점 · 계정 · 클라우드 접근 · 사용량 조건 확인"],
            [k("/simplify"), "수정 코드의 재사용 · 단순화 · 효율 검토와 개선 · <code>/simplify src/</code> 대상 지정"],
            [k("/security-review"), "현재 브랜치 변경의 보안 문제 · 원격 <code>origin</code>과 비교 기준 브랜치 필요"],
        ], cls="s9-wrap")
             + note("기본 제공 Skill", "명령 입력 → Claude가 작업 지침을 받아 수행 · 코드 실행 · 수정 · 외부 서비스 이용 포함 가능 → 요청 범위 함께 적기", "red"), kick=kk),
        page("실행 · 조사 · 자료 Skill", T([
            [k("/run"), "앱 실행 · 변경 결과 확인", ""],
            [k("/verify"), "빌드 · 실행 · 조작 → 요청한 동작 확인", ""],
            [k("/run-skill-generator"), "프로젝트의 실행 · 검증 절차를 Skill로", ""],
            [k("/debug 증상"), "디버그 로그와 현재 상황으로 원인 조사", k("/debug CSV 업로드 후 화면이 멈춥니다.")],
            [k("/batch 요청"), "큰 변경 → worktree 병렬 처리 · 계획 확인 후 여러 작업 · PR 생성까지", k("/batch src의 공통 오류 처리 방식을 통일해 주세요.")],
            [k("/claude-api"), "Claude API 개발 자료", "하위 작업 5종"],
            [k("/dataviz 요청"), "시각화 설계", k("/dataviz 환율의 월별 변화를 보여줄 차트를 설계해 주세요.")],
            [k("/design 요청"), "지원 계정에서 화면 시안", k("/design 환율 대시보드의 화면 시안")],
            [k("/design-login"), "디자인 시스템 접근 인증", ""],
            [k("/design-sync [힌트]"), "저장소의 디자인 시스템 → Claude Design · 외부 업로드 포함", ""],
        ], ("명령", "하는 일", "예"), "s9-wrap"), kick=kk),
        page("/claude-api 하위 작업", T([
            [k("migrate"), "모델 이전"], [k("upgrade"), "SDK 이전"], [k("managed-agents-onboard"), "Managed Agent 시작"],
            [k("prompt-audit"), "프롬프트 점검"], [k("cost-optimize"), "비용 개선"],
        ], ("하위 작업", "용도"))
             + note("/design-sync", "프로젝트 구성요소의 외부 업로드 포함", "red")
             + note("공식 참고", "코드 검토 · 앱 실행 · 검증 Skill · Commands"), kick=kk),
        page("대화 안의 Agent 명령", T([
            [k("/agents"), "Subagent 관리 안내 · 자연어로 생성 · 수정 요청 또는 <code>.claude/agents/</code> 파일 편집"],
            [k("/subtask 요청"), "현재 대화를 이어받는 백그라운드 Subagent에 작업 · 결과는 원래 대화로"],
            [k("/tasks", "/bashes"), "현재 세션의 백그라운드 작업 확인 · 관리"],
            [k("/list-agents", "/peers"), "메시지를 보낼 수 있는 Agent · 다른 세션 · 기능 활성화 여부에 따름"],
            [k("/background [추가 요청]", "/bg"), "현재 세션 전체를 백그라운드로"],
            [k("/fork [요청]"), "현재 대화를 복사한 별도 백그라운드 세션"],
            [k("/stop"), "현재 접속한 백그라운드 세션 중단 · 연결 해제는 <code>/exit</code>"],
        ], cls="s9-wrap")
             + note("/fork · /branch", "<code>/fork</code>: 별도 백그라운드 세션 · <code>/branch</code>: 사용자가 새 분기로 이동")
             + prompt("/subtask 현재 변경과 관련된 테스트 누락을 조사해 주세요.", "Claude Code · 예"), kick=kk),
        page("터미널의 백그라운드 관리", two(
            prompt('claude --bg "실패한 테스트의 원인을 조사해 주세요."', "PowerShell · 백그라운드 시작")
            + note("ID", "반환된 ID를 관리 명령에 사용")
            + note("-p", "<code>--bg</code>와 함께 쓰지 않음", "red")
            + note("rm", "삭제 대상 먼저 확인", "red"),
            T([
                [k("claude agents"), "백그라운드 Agent 관리 화면"],
                [k("claude agents --json --all"), "종료 항목 포함 JSON 조회"],
                [k("claude attach <ID>"), "세션 접속"],
                [k("claude logs <ID>"), "최근 출력"],
                [k("claude stop <ID>", "kill"), "실행 멈춤 · 대화 기록 유지"],
                [k("claude respawn <ID>"), "현재 설치 버전으로 재시작"],
                [k("claude rm <ID>"), "종료 세션 · 삭제 가능한 worktree 제거"],
            ]), "w2"), kick=kk),
        page("반복 · 예약 작업", T([
            [k("/goal 완료 조건"), "완료 조건 지정해 작업 이어가기 · <code>/goal</code> 상태 · <code>/goal clear</code> 해제"],
            [k("/loop 5m 요청"), "세션이 열려 있는 동안 반복 · 별칭 <code>/proactive</code>"],
            [k("/schedule 요청"), "클라우드에서 실행할 Routine 구성 · 별칭 <code>/routines</code> · 지원 계정 · 실행 환경 확인"],
            [k("/deep-research 요청"), "여러 조사 작업 Workflow · <code>/workflows</code> 진행 관리 · <code>/workflow-authoring</code> 작성 자료"],
        ], cls="s9-wrap")
             + prompt("/goal 테스트를 통과하고 실행 확인까지 마치기\n/loop 5m 배포 상태를 확인해 주세요.\n/schedule 매주 월요일 오전에 의존성 업데이트를 조사해 주세요.\n/deep-research 반도체 장비 시장의 최근 변화를 조사해 주세요.", "Claude Code · 예", sm=True)
             + note("/loop", "세션 종료 이후까지 유지되는 예약 작업과 실행 환경이 다름"), kick=kk),
        page("앱 안의 Agent와 구분", two(
            pane("Claude Code Agent 기능", ul(["<code>/agents</code> · <code>/subtask</code> · <code>/fork</code>", "<code>claude --bg</code> · <code>claude agents</code>", "개발 도구의 작업 분담"])),
            pane("교육의 Multi-Agent 실습", ul(["앱 코드 안의 연구책임자 · 연구원 구조 구현", "앱 내부 Agent 실행"]), "good"))
             + note("구분", "두 기능은 각각 별도로 동작", "red")
             + note("공식 참고", "Subagents · Agent view · 백그라운드 세션 · 예약 작업 · Routines"), kick=kk),
    ]


def block_ext():
    kk = "MCP · Skill · Plugin"
    return [
        section("05", "MCP · Skill · Plugin", "서버 등록 · 범위 · 상태 관리 · Skill 작성 · Plugin 설치"),
        page("MCP 서버 등록", prompt("claude mcp add --transport http --scope project mslearn https://learn.microsoft.com/api/mcp", "PowerShell · 프로젝트용 원격 MCP 서버", sm=True)
             + prompt(r"claude mcp add --transport stdio my-server -- python C:\samsung_YYYYMMDD\my-server\server.py", "PowerShell · 로컬 Python 서버 구문 예", sm=True)
             + note("확인", "실제 연결과 도구 노출 → Claude Code 안에서 <code>/mcp</code>")
             + note("--", "<code>--</code> 뒤는 서버 프로세스의 명령과 인자 · 서버 파일이 실제로 있고 stdio MCP 서버로 구현되어 있어야 함", "red"), kick=kk),
        page("전송 방식과 범위", T([
            [k("--transport http"), "원격 HTTP 서버"],
            [k("stdio"), "로컬 프로세스"],
            [k("sse"), "SSE 전송 서버 · 서버 제공자가 안내한 방식 사용"],
        ], ("전송", "대상")) + '<div class="s9-mb"></div>' + f9.scopes(), kick=kk),
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
        page("MCP 고급 등록", T([
            [k("claude mcp add-json <서버명> '<JSON>'"), "JSON 서버 설정 등록 · PowerShell의 JSON 인자 전달 확인 · 복잡하면 <code>--mcp-config</code> 파일"],
            [k("-e 이름=값"), "stdio 서버의 환경변수"],
            [k('-H "헤더명: 값"'), "HTTP/SSE 헤더"],
            [k("--client-id", "--client-secret", "--callback-port"), "OAuth · 서버의 인증 요구에 맞춤"],
            [k("claude mcp reset-project-choices"), "프로젝트 MCP 서버의 승인 · 거절 선택 초기화"],
            [k("claude mcp add-from-claude-desktop"), "Desktop 설정 가져오기 · Mac · WSL 지원 범위 확인"],
            [k("claude mcp serve"), "Claude Code를 MCP 서버로 실행 · 다른 MCP Host에서 연결"],
        ], cls="s9-wrap")
             + note("인증값", "예시 코드나 공유 <code>.mcp.json</code>에 그대로 남기지 않음", "red"), kick=kk),
        page("Claude Code와 앱 구분", f9.two_targets()
             + note("Prompt 명령", "MCP 서버가 Prompt를 제공하면 <code>/mcp__서버명__프롬프트명</code> 표시 가능 · 모든 Tool이 Slash 명령이 되지는 않음")
             + note("앱 MCP 카탈로그", "서버 추가 = 앱의 설정 파일과 코드 변경 · <code>claude mcp add</code>는 Claude Code에 등록", "red")
             + note("공식 참고", "MCP 연결 · 상세 하위 옵션은 <code>claude mcp &lt;하위명령&gt; --help</code>"), kick=kk),
        page("Skill 사용과 위치", T([
            [k("/skills"), "사용할 수 있는 Skill 확인"],
            [k("/reload-skills"), "변경한 Skill · 명령 디렉터리 다시 읽기"],
            [k("/skill-doctor"), "Skill 사용 빈도와 컨텍스트 비용 점검"],
            [k(".claude/skills/<이름>/SKILL.md"), "프로젝트 Skill 기본 위치 · <code>/이름</code>으로 호출"],
            [k("~/.claude/skills/<이름>/SKILL.md"), "개인 공통 위치"],
            [k(".claude/commands/<이름>.md"), "기존 사용자 명령 형식 · 현행 Skill과 함께 지원 · 새 절차는 <code>SKILL.md</code>"],
            [k("/plugin-name:skill-name"), "Plugin Skill · 이름 공간 포함"],
        ]), kick=kk),
        page("Skill 작성", T([
            [k("name", "description"), "YAML 머리말 · 이름과 용도"],
            ["본문", "단계와 출력 형식"],
            [k("$ARGUMENTS"), "호출 뒤의 입력 받기"],
            [k("disable-model-invocation: true"), "사용자가 직접 호출하도록 제한"],
        ], ("항목", "역할"))
             + prompt("/review-csv data/rates.csv", "Claude Code · review-csv Skill 실행 예")
             + note("예", "<code>review-csv</code> Skill에 CSV 열 이름 · 자료형 · 결측값 점검 절차 정의 → 이 명령은 Skill을 만든 뒤에 생김"), kick=kk),
        page("Plugin 관리", T([
            [k("/plugin"), "Plugin 관리 메뉴 · <code>/plugin list</code> · <code>/plugin install &lt;이름&gt;</code> · <code>/plugin enable &lt;이름&gt;</code> · <code>/plugin disable &lt;이름&gt;</code>"],
            [k("claude plugin list"), "설치 목록"],
            [k("claude plugin details <이름>"), "구성요소와 예상 컨텍스트 비용"],
            [k("claude plugin install <이름>@<마켓플레이스>"), "설치"],
            [k("enable", "disable", "update", "uninstall"), "활성화 · 비활성화 · 업데이트 · 제거 · <code>claude plugins</code>도 같은 명령군"],
            [k("/reload-plugins"), "변경한 Plugin 다시 읽기 · <code>--force</code> 강제"],
        ], cls="s9-wrap")
             + note("다시 읽기", "캐시 변경으로 보류되면 안내 확인 · 설치 · 업데이트 결과가 재시작을 요구하면 세션 다시 열기"), kick=kk),
        page("배포처와 Plugin 제작", T([
            [k("claude plugin marketplace add <저장소 또는 URL 또는 경로>"), "배포처 등록"],
            [k("marketplace list", "marketplace update [이름]", "marketplace remove <이름>"), "배포처 목록 · 갱신 · 제거"],
            [k("claude plugin init <이름>", "new"), "기본 구조 생성"],
            [k("validate <경로>"), "정의 검사"],
            [k("eval <대상>"), "평가 실행"],
            [k("tag [경로]"), "릴리스 태그 생성"],
            [k("prune", "autoremove"), "불필요해진 자동 설치 의존성 정리"],
        ], cls="s9-wrap")
             + note("공식 참고", "Skills · Plugins reference · 옵션은 <code>claude plugin &lt;하위명령&gt; --help</code>"), kick=kk),
    ]


def block_misc():
    kk = "외부 연결과 관리"
    return [
        section("06", "외부 연결과 관리", "IDE · 웹 · 모바일 · 로그인 · 진단 · 표시 · 기타"),
        page("IDE · 브라우저 · 앱", T([
            [k("/ide"), "IDE 연결 상태 관리"],
            [k("claude --ide"), "연결 가능한 IDE가 하나일 때 시작과 함께 연결"],
            [k("/chrome"), "브라우저 연동 설정"],
            [k("claude --chrome", "claude --no-chrome"), "해당 세션의 연동 켜기 · 끄기"],
            [k("/desktop", "/app"), "Desktop 앱에서 세션 이어가기 · 지원 OS와 Claude 구독 필요"],
            [k("/mobile", "/ios", "/android"), "모바일 앱 설치 안내"],
            [k("/web-setup"), "GitHub 계정의 웹 개발 환경 연결"],
            [k("/install-github-app"), "저장소의 GitHub App · 선택적 Actions 연결 안내"],
            [k("/install-slack-app"), "Slack 앱 인증 화면"],
            [k("/artifacts"), "계정에서 쓸 수 있는 Artifact 확인 · 첨부"],
        ], cls="s9-wrap"), kick=kk),
        page("원격 제어와 클라우드", T([
            [k("/remote-control", "/rc"), "현재 로컬 세션을 다른 기기에서 조작", k('claude --remote-control "환율앱"') + " 시작 때 설정"],
            [k("claude remote-control"), "원격 접속을 기다리는 서버 모드", k("--name", "--spawn", "--capacity") + " 하위 명령 뒤"],
            [k("claude --cloud"), "클라우드 세션 시작", k('claude --cloud "업로드 오류를 수정해 주세요."')],
            [k("/remote-env"), "기본 클라우드 환경 선택", k("--environment <환경ID>") + " 자체 호스팅 환경"],
            [k("/teleport", "/tp"), "웹 세션의 브랜치와 대화를 로컬 터미널로", k("--teleport")],
            [k("/autofix-pr [지시문]"), "현재 브랜치 PR 감시 클라우드 세션 · CI 실패 · 검토 의견 → 수정 push", "<code>gh</code> · 웹 세션 접근 필요"],
        ], ("명령", "하는 일", "비고"), "s9-wrap")
             + note("원격 제어", "작업은 로컬 컴퓨터에서 실행 → 컴퓨터와 세션이 실행 중이어야 함", "red")
             + note("공식 참고", "Remote Control · Claude Code on the web · IDE integrations · Chrome"), kick=kk),
        page("로그인 · 업데이트 · 진단", T([
            [k("claude auth login", "logout", "status"), "PowerShell에서 로그인 · 로그아웃 · 인증 상태 · 대화 안에서는 <code>/login</code> <code>/logout</code>"],
            [k("claude setup-token"), "구독 기반 장기 인증 토큰 설정"],
            [k("claude doctor"), "설치 상태 읽기 전용 진단"],
            [k("/doctor", "/checkup"), "세션 안에서 설정 · 설치 문제 분석 · 확인 후 수정 제안"],
            [k("claude update", "claude upgrade"), "업데이트 확인 · 설치"],
            [k("claude install stable", "latest", "<버전>"), "네이티브 빌드 설치 대상 지정"],
            [k("/release-notes"), "버전별 변경 내용"],
        ], cls="s9-wrap"), kick=kk),
        page("표시 설정 · 기타 명령", two(T([
            [k("/theme"), "화면 테마"],
            [k("/color [색 또는 default]"), "세션 입력줄 색"],
            [k("/tui [default 또는 fullscreen]"), "화면 렌더러"],
            [k("/focus"), "지원 화면에서 요약 중심 표시"],
            [k("/scroll-speed"), "스크롤 속도"],
            [k("/voice [hold 또는 tap 또는 off]"), "지원 계정의 음성 입력"],
            [k("/feedback", "/bug", "/share"), "의견 · 문제 보고"],
            [k("/heapdump"), "메모리 문제 진단 파일"],
        ], cls="s9-wrap"), T([
            [k("/privacy-settings"), "지원 구독의 개인정보 설정"],
            [k("/insights"), "최근 사용 기록 분석 보고서"],
            [k("/team-onboarding"), "사용 이력 기반 팀 시작 가이드"],
            [k("/powerup"), "기능 학습"],
            [k("/passes"), "대상 계정의 체험 공유"],
            [k("/radio"), "음악 페이지"],
            [k("/stickers"), "스티커 주문 안내"],
            [k("/setup-bedrock", "/setup-vertex"), "클라우드 공급자 인증 · 지역 · 모델"],
        ], cls="s9-wrap"))
             + note("/feedback", "전송할 대화 범위와 수신처 확인 후 제출")
             + note("/heapdump", "전체 heap snapshot에 대화 · 인증정보 포함 가능 → 일반 공유 자료로 사용 금지", "red"), kick=kk),
        page("관리용 CLI 명령", T([
            [k("claude auto-mode config", "defaults"), "Auto 모드 적용값 · 기본값 확인"],
            [k("critique"), "사용자 규칙에 대한 AI 검토"],
            [k("reset"), "사용자 Auto 모드 설정 초기화"],
            [k("claude import codex --dry-run"), "외부 개발 도구 설정 가져오기 예고"],
            [k("claude project purge [경로]"), "프로젝트의 대화 · 작업 · 파일 이력 등 Claude Code 상태 삭제 · 새 대화는 <code>/clear</code>"],
            [k("claude gateway --help"), "기업용 인증 · 텔레메트리 게이트웨이 설정 · 수업 실습에 불필요"],
            [k("claude ultrareview [대상]"), "터미널에서 클라우드 코드 검토 · PR 번호 또는 기준 브랜치 · 먼저 <code>--help</code>로 옵션 확인"],
        ], cls="s9-wrap")
             + note("/setup-bedrock · /setup-vertex", "관련 환경변수와 계정 구성이 필요한 선택 기능")
             + note("공식 참고", "Troubleshooting · Setup · Commands · 관리 명령은 설치본 2.1.263의 <code>--help</code>와 대조"), kick=kk),
    ]


def block_auto():
    kk = "자동화 · CLI 옵션"
    return [
        section("07", "자동화 · CLI 옵션", "입력 · 출력 · 반복 실행 · 모델 · 지침 · 도구 · 실행 환경"),
        page("파이프로 입력 · 출력", prompt(r'Get-Content -Raw -Encoding UTF8 .\error.log | claude -p "이 로그의 원인 후보와 확인 순서를 정리해 주세요."', "PowerShell · 파일 내용을 표준입력으로", sm=True)
             + prompt("$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()", "PowerShell · 외부 프로그램 입출력 UTF-8", sm=True)
             + prompt(r'claude -p "README에서 실행 방법을 요약해 주세요." | Set-Content -Encoding UTF8 .\run-summary.txt', "PowerShell · 결과를 파일로 저장", sm=True)
             + note("입력", "지정한 파일 내용이 모델 입력에 포함 · 한글 로그는 인코딩 확인")
             + note("저장", "같은 경로의 파일이 있으면 덮어씀", "red")
             + note("확인", "읽기 · 요약처럼 검토하기 쉬운 요청부터 · <code>-p</code>는 대화형 질문을 기다리는 흐름과 다름 → 실행 권한 · 종료 상태 · 결과 파일 함께 확인")
             + note("공식 참고", "Programmatic execution · CLI reference · 세부 조건은 설치 버전 도움말 우선"), kick=kk),
        page("출력 · 입력 형식", T([
            [k("--output-format text"), "일반 텍스트"],
            [k("json"), "결과 JSON"],
            [k("stream-json"), "이벤트별 JSON"],
            [k("--input-format text"), "일반 입력"],
            [k("stream-json"), "구조화된 스트림 입력 · 지정된 메시지 형식 필요"],
            [k("--json-schema <JSON>"), "결과가 따를 JSON Schema · <code>type</code> <code>properties</code> <code>required</code>로 보고서 필드 지정"],
        ], ("옵션 · 값", "하는 일"), "s9-wrap")
             + prompt('claude -p "실행 방법을 요약해 주세요." --output-format json', "PowerShell · 예")
             + note("주의", "<code>stream-json</code> 입력은 임의의 JSON 파일을 그대로 보내는 옵션 아님 · 복잡한 JSON은 PowerShell 따옴표 전달 확인", "red"), kick=kk),
        page("실행 한도 · 스트림 옵션", two(T([
            [k("--max-turns 3"), "Print 모드의 Agent 턴 수 제한"],
            [k("--max-budget-usd 1"), "API 사용 금액 한도"],
            [k("--no-session-persistence"), "Print 대화를 디스크에 남기지 않음 · 이후 <code>/resume</code> 불가"],
            [k("--fallback-model sonnet,haiku"), "기본 모델 불가 시 대체 모델 순서 · Print 모드용"],
            [k("--permission-prompts none"), "승인할 사람이 없는 Print 실행 · 질문 필요한 동작 거부 · <code>host</code>는 SDK Host 경로"],
        ], cls="s9-wrap"), T([
            [k("--include-partial-messages"), "부분 스트리밍 이벤트"],
            [k("--include-hook-events"), "Hook 이벤트"],
            [k("--forward-subagent-text"), "Subagent 텍스트 포함 · <code>stream-json</code> · 필요 시 <code>-p --verbose</code>"],
            [k("--replay-user-messages"), "스트림 입력 메시지를 출력으로 · 입출력 모두 <code>stream-json</code>"],
            [k("--prompt-suggestions"), "후속 요청 제안 이벤트"],
            [k("--permission-prompt-tool <MCP도구>"), "전용 승인 도구 · 고급"],
        ], cls="s9-wrap"))
             + prompt('claude -p "테스트 오류를 분석해 주세요." --max-turns 3 --max-budget-usd 1', "PowerShell · 예"), kick=kk),
        page("CLI 옵션 · 모델과 지침", T([
            [k("--model <모델>", "--effort <수준>"), "이번 세션의 모델 · 추론 수준"],
            [k("--agent <이름>"), "세션의 Agent 정의 선택"],
            [k("--agents <JSON>"), "이번 실행에 쓸 Agent 정의 전달"],
            [k('--system-prompt "지침"'), "기본 System Prompt 대체"],
            [k('--append-system-prompt "답변에는 파일 경로를 포함하세요."'), "기본 지침 뒤에 덧붙임"],
            [k("--system-prompt-file <파일>", "--append-system-prompt-file <파일>"), "지침을 파일에서 읽기"],
            [k("--append-subagent-system-prompt <지침>", "-file <파일>"), "Print 모드의 Subagent용 추가 지침 · 둘 중 하나만"],
            [k("--system-prompt-snapshot on", "off"), "System Prompt 기록 · 재사용 조절 · 설치본 도움말의 고급 옵션"],
        ], cls="s9-wrap")
             + note("교체 · 추가", "전체 교체 옵션 둘은 함께 사용 불가 · 기본 동작 유지하며 규칙만 추가 → append 계열", "red")
             + note("snapshot", "활성화된 기록이 있으면 바꾼 지침이 바로 반영되지 않을 수 있음"), kick=kk),
        page("CLI 옵션 · 설정 · 세션 · MCP", two(T([
            [k("--settings <파일 또는 JSON>"), "이번 실행에 적용할 설정"],
            [k("--setting-sources user,project,local"), "불러올 설정 범위"],
            [k("--add-dir <폴더...>"), "접근할 추가 폴더"],
            [k("--autocompact <auto 또는 토큰수>"), "자동 요약 기준"],
            [k("--session-id <UUID>"), "세션 ID 명시"],
            [k("--from-pr <PR번호 또는 URL>"), "연결된 PR의 대화 찾기"],
            [k("--permission-mode plan"), "Plan 모드로 시작"],
        ], ("옵션", "하는 일"), "s9-wrap"), T([
            [k(r"--mcp-config .\mcp.json"), "MCP 설정 파일 읽기"],
            [k("--strict-mcp-config"), "지정한 MCP 설정만 사용"],
            [k(r"--plugin-dir .\my-plugin"), "로컬 디렉터리 · ZIP 불러오기 · 여러 개면 반복"],
            [k("--plugin-url <URL>"), "URL의 Plugin ZIP"],
            [k("--disable-slash-commands"), "Skill · 명령 기능 제한"],
            [k("--exclude-dynamic-system-prompt-sections"), "장비별 동적 정보를 첫 사용자 메시지로 · Prompt Cache 재사용 구성"],
        ], ("옵션", "하는 일"), "s9-wrap")), kick=kk),
        page("CLI 옵션 · 도구와 권한", T([
            [k('--allowedTools "Read" "Bash(git status *)"'), "승인 없이 허용할 도구 규칙"],
            [k('--disallowedTools "Edit"'), "금지 규칙 · 하이픈 표기 <code>--allowed-tools</code> <code>--disallowed-tools</code>도 지원"],
            [k('--tools "Read,Grep,Glob"'), "내장 도구 목록 제한 · MCP 도구는 별도 → <code>--disallowedTools \"mcp__*\"</code>"],
            [k("--dangerously-skip-permissions"), "권한 확인을 건너뛰는 모드로 시작"],
            [k("--allow-dangerously-skip-permissions"), "해당 모드를 선택 가능하게 · 처음부터 켜지지는 않음"],
            [k("--safe-mode"), "사용자 지침 · Skill · Plugin · Hook · MCP 영향 배제 · 설정 문제 진단 · 인증 · 기본 도구 · 권한 유지"],
            [k("--bare"), "자동 로딩을 줄인 최소 실행 · OAuth · 키체인 읽지 않음 → 인증 구성 따로 확인"],
            [k("--restricted"), "코드 실행 도구 · 설정 로딩 · 파일 접근 제한"],
        ], cls="s9-wrap")
             + note("skip-permissions", "의미를 모른 채 오류 해결용으로 추가하지 않음", "red")
             + note("세 모드", "<code>--safe-mode</code> · <code>--bare</code> · <code>--restricted</code> 적용 범위가 서로 다름 · safe-mode에도 관리 정책 적용"), kick=kk),
        page("CLI 옵션 · 작업 폴더와 백그라운드", T([
            [k("--worktree [이름]", "-w [이름]"), "Git worktree로 작업 폴더 분리"],
            [k("--tmux"), "worktree를 tmux 세션에서 · <code>--worktree</code> 필요"],
            [k("--teammate-mode <모드>"), "Agent Team 표시 방식 · <code>in-process</code> <code>auto</code> <code>tmux</code> <code>iterm2</code>"],
            [k("--bg", "--background"), "백그라운드 시작 · <code>--exec</code>와 조합 → 셸 작업을 백그라운드로"],
        ], cls="s9-wrap")
             + prompt('claude -w fx-chart "환율 차트의 날짜 축을 개선해 주세요."', "PowerShell · worktree 예")
             + note("tmux · iTerm2", "해당 환경 준비 필요 · 기본 Windows PowerShell 기능 아님", "red")
             + note("--bg --exec", "예시와 지원 여부는 백그라운드 문서에서 확인"), kick=kk),
        page("CLI 옵션 · 원격과 연결", T([
            [k("--cloud <요청>"), "웹 작업 시작"],
            [k("--environment <환경ID>"), "자체 호스팅 실행 환경 지정"],
            [k("--ref <브랜치>"), "해당 환경의 시작 Git ref · <code>--remote</code>는 폐기 예정 별칭 → <code>--cloud</code>"],
            [k("--remote-control [이름]", "--rc"), "로컬 세션의 원격 제어"],
            [k("--remote-control-session-name-prefix <접두어>"), "자동 생성 세션 이름 접두어"],
            [k("--chrome", "--no-chrome", "--ide", "--teleport"), "브라우저 · IDE · 웹 세션 연결 · 외부 연결 절 참고"],
        ], cls="s9-wrap"), kick=kk),
        page("CLI 옵션 · 진단과 고급", two(T([
            [k("--debug", "-d"), "디버그 로그 · 범주는 <code>claude --debug=mcp,startup</code>"],
            [k(r"--debug-file .\claude-debug.log"), "로그 경로 지정"],
            [k("--verbose"), "상세 실행 출력"],
            [k("--ax-screen-reader"), "화면 읽기 도구에 맞춘 출력"],
            [k("--betas <항목...>"), "API Key 사용자의 Beta 헤더 · 고급"],
            [k("--init"), "Print 시작 전 init Setup Hook"],
            [k("--maintenance"), "maintenance Setup Hook"],
            [k("--init-only"), "초기화 관련 Hook만 실행 후 종료"],
        ], ("옵션", "하는 일"), "s9-wrap"), T([
            [k("--channels <항목...>"), "지원되는 MCP Channel 알림 구독"],
            [k("--dangerously-load-development-channels <항목...>"), "개발 중 Channel 허용 · Research Preview · 공급자 · 인증 · 활성화 조건"],
            [k("--file <파일ID:상대경로...>"), "시작 시 파일 리소스 다운로드 · <code>@파일</code>과 입력 형식 다름"],
            [k("--brief"), "Agent가 사용자에게 메시지를 보내는 도구 활성화 · 내부 통신 흐름 구성 때만"],
        ], ("옵션", "하는 일"), "s9-wrap"))
             + note("--init-only", "대화의 <code>/init</code>과 실행 대상이 다름")
             + note("공식 참고", "CLI reference · Agent view · 백그라운드 세션 · Agent teams · Channels"), kick=kk),
    ]


def block_close():
    kk = "주의와 순서"
    return [
        section("08", "주의와 순서", "오래된 안내의 바뀐 명령 · 수업 중 자주 쓰는 순서"),
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


def slides():
    return opening() + block_start() + block_settings() + block_keys() + block_agent() + block_ext() + block_misc() + block_auto() + block_close()
