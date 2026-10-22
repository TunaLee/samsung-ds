"""과정 소개 · 학습 목표와 실습 준비 (원본: 노션 교안 루트 페이지)."""
import fig
import s0_fig as f0
from kit import cards, cover, flow, note, page, pane, prompt, section, steps, table, two, ul
from s1 import course_map

TITLE = "과정 소개 · 학습 목표와 실습 준비"

ERR = """claude : 'claude' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다. 이름이 정확한지 확인하고 경로가 포함된 경우 경로가 올바른지 검증한 다음 다시 시도하십시오.
위치 줄:1 문자:1
+ claude
+ CategoryInfo : ObjectNotFound: (claude:String) [], CommandNotFoundException
+ FullyQualifiedErrorId : CommandNotFoundException"""

TEST = r'Test-Path "$env:USERPROFILE\.local\bin\claude.exe"'
DIRECT = r'& "$env:USERPROFILE\.local\bin\claude.exe" --version'
SETPATH = r"""$claudePath = "$env:USERPROFILE\.local\bin"

# 현재 PowerShell에 즉시 적용
$env:Path += ";$claudePath"

# 사용자 PATH에 영구 등록 (중복 방지)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

if (($userPath -split ';') -notcontains $claudePath) {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$userPath;$claudePath",
        "User"
    )
}"""
FIND = 'Get-ChildItem -Path $env:APPDATA, $env:LOCALAPPDATA -Filter "claude.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName'
FOUND = r"C:\Users\사용자명\AppData\Local\Packages\Claude_pzs8sdgfd5c\LocalCache\Roaming\Claude\claude-code\2.1.247\claude.exe"
SETPATH_B = r'''# B-1에서 확인한 본인의 폴더 경로로 입력합니다. (claude.exe 제외)
$claudePath = "C:\Users\본인사용자명\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\2.1.247"

# 환경 변수 Path에 해당 경로를 추가합니다.
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$claudePath", "User")'''
TREE = r"""C:\Users\사용자계정명\Downloads\samsung_ds_btrack
├─agents-lab
├─line-sim
├─PDFs
└─rag-lab"""


def opening():
    return [
        cover(["B Track", "<em>AI Agent</em> 아키텍트 과정"],
              "학습 목표 · 교육 방식 · 오늘의 프로젝트 · 실습 준비",
              [("교안", "b2bsparta.com/0827-686a"), ("방식", "바이브코딩"), ("도구", "Claude Code · OpenAI GPT")], "과정 소개"),
        page("학습 목표", cards([
            ("앱 구조 파악과 구현", "Claude Code로 배부 앱의 구조 파악 · 필요한 기능 요청 · 구현과 수정", "01"),
            ("RAG 흐름", "문서 준비와 검색 · 답변 흐름 설명 · 단계별 결과 확인과 개선", "02"),
            ("도구 제공", "AI에 도구 제공 · 도구 선택의 판단 근거 설명", "03"),
            ("판정 모델과 조사 Agent", "이벤트 판정 모델과 도구 기반 조사 Agent 연결 · 역할과 실행 조건 분리", "04"),
        ], 2)),
    ]


def block_way():
    return [
        section("01", "교육 방식", "코드를 직접 쓰는 대신 자연어 지시로 만들고 고치는 바이브코딩"),
        page("바이브코딩", flow([("자연어 지시", "만들 기능 · 고칠 점"), ("Claude Code", "코드 작성 · 수정"),
                               ("앱 실행", "결과 확인"), ("다시 지시", "필요한 수정 요청")], hl=1)
             + note("바이브코딩", "코드를 직접 작성하지 않고 자연어 지시로 프로그램을 만들고 고치는 방식", "red"), kick="교육 방식"),
        page("개발 환경과 앱 실행 환경", f0.roles(), kick="교육 방식",
             sub="Claude Code는 개발 환경에서 앱을 제작 · OpenAI GPT는 실행 환경에서 앱이 호출"),
    ]


def block_project():
    return [
        section("02", "오늘의 프로젝트", "RAG 앱 · Agent 앱 · 캡스톤"),
        page("오늘 만드는 세 가지", '<div class="parts">'
             + fig._tile("search", "RAG 앱", "학습하지 않은 기술 문서를<br>AI가 참조해 답변")
             + '<div class="plus">→</div>'
             + fig._tile("tool", "Agent 앱", "Tool Calling으로<br>AI에 도구 제공")
             + '<div class="plus">→</div>'
             + fig._tile("pen", "캡스톤", "각자 선정한 주제로 결과물 완성<br>앞 프로젝트의 내용 적용", "core")
             + "</div>", kick="프로젝트"),
        page("과정 구성", f0.modules(), kick="프로젝트", sub="5개 모듈 · 8개 교시"),
        page("시간표", table(["시간", "교시", "핵심 내용"], [
            ["08:30 ~ 09:30", "<b>1교시</b> · Claude Code와 RAG 시작", "실습 준비 · 보안, PDF 한 편으로 RAG 구조 관찰"],
            ["09:40 ~ 10:40", "<b>2교시</b> · naive RAG 완성", "임베딩 활용, 청킹 · BM25 · 하이브리드 검색 선택"],
            ["10:50 ~ 11:50", "<b>3교시</b> · Advanced RAG", "질의 재작성 · 재정렬 · 기준값, Text-to-SQL · GraphRAG 소개"],
            ["11:50 ~ 13:00", "점심시간", ""],
            ["13:00 ~ 13:50", "<b>4교시</b> · Tool Calling", "API 요청 확인, 도구 추가, Agent와 가드레일"],
            ["14:00 ~ 14:50", "<b>5교시</b> · MCP", "검색 API → Tool → MCP 서버 → agents-lab 연결"],
            ["15:00 ~ 16:50", "<b>6교시</b> · 생산라인 감시", "Decisions 판정 → 보고 모으기 → 조사 Agent의 도구 조회"],
            ["16:10 ~ 17:10", "<b>7교시</b> · 캡스톤 1", "주제 선정과 제작, 라운드 기록"],
            ["17:10 ~ 17:30", "<b>8교시</b> · 캡스톤 2", "결과물 완성, 결과 보고서 작성과 제출"],
        ], "s0-tt") + note("Break", "교시 사이 10분"), kick="시간표"),
    ]


def block_setup():
    return [
        section("03", "실습 준비", "실습 자료 받기 · Claude Code 명령어 인식 오류 해결"),
        page("실습 자료 받기", two(
            steps([("저장", "배부한 실습 자료 파일 저장"), ("압축 해제", "다운로드 폴더에 풀기"),
                   ("폴더 확인", "<b>samsung_ds_btrack</b> 아래 네 개 폴더")]),
            prompt(TREE, "폴더 구조", sm=True), "w2"), kick="실습 준비"),
        page("PowerShell에서 claude 인식 오류", prompt(ERR, "오류 메시지 · CommandNotFoundException", sm=True)
             + note("원인", "환경 변수 <b>PATH</b>에 Claude Code 실행 파일 경로가 없어 터미널이 프로그램을 찾지 못함", "red")
             + note("해결", "설치 확인 → PATH 등록 → 버전 확인"), kick="Troubleshooting · Windows"),
        page("먼저 · 설치 위치 확인", two(
            prompt(TEST, "PowerShell · 설치 파일 확인", sm=True)
            + table(["결과", "뜻"], [["<b>True</b>", "설치됨 · PATH 문제 · <b>방법 A</b>로"],
                                   ["<b>False</b>", "다른 위치에 설치 · <b>방법 B</b>로 · 그래도 없으면 1교시 설치 명령"]]),
            prompt(DIRECT, "PowerShell · 직접 실행", sm=True)
            + note("버전이 나오면", "프로그램은 정상 · 터미널이 위치를 모르는 것뿐", "red")), kick="Troubleshooting · Windows"),
        page("방법 A · .local\\bin을 PATH에 등록", prompt(SETPATH, "PowerShell · 그대로 붙여 넣기", sm=True)
             + note("고칠 값 없음", "현재 창에 즉시 적용 + 사용자 PATH에 영구 등록 (이미 있으면 건너뜀) · 관리자 권한 불필요", "red"), kick="Troubleshooting · Windows"),
        page("방법 B-1 · 실행 파일 위치 검색", prompt(FIND, "PowerShell · claude.exe 위치 검색")
             + '<div class="s0-gap"></div>'
             + prompt(FOUND, "출력 예시", sm=True)
             + note("복사할 부분", "마지막 파일명 <code>\\claude.exe</code>를 뺀 <b>폴더 경로만</b>", "red"), kick="Troubleshooting · Windows"),
        page("방법 B-2 · 찾은 폴더를 PATH에 등록", prompt(SETPATH_B, "PowerShell · 경로 등록", sm=True)
             + note("주의", "첫 줄 <code>$claudePath</code> 값을 B-1에서 복사한 <b>실제 폴더 경로</b>로 바꾼 뒤 실행 · 열려 있는 PowerShell 창은 모두 닫고 새로 열기", "red"), kick="Troubleshooting · Windows"),
        page("마지막 · 버전 확인", two(
            steps([("확인", "버전 번호가 나오면 정상"), ("새 창에서도", "PowerShell을 새로 열어 한 번 더")]),
            prompt("claude --version", "PowerShell · 확인"))
             + note("방법 B 주의", "등록한 경로에 <code>2.1.247</code> 같은 버전 숫자 포함 · 업데이트로 폴더명이 바뀌면 B-1 · B-2 다시", "red"), kick="Troubleshooting · Windows"),
    ]


def closing():
    return [
        page("교육 만족도 조사", f0.link("교육 만족도 조사",
                                     "https://teamsparta-survey.vercel.app/s/course/0d0a599c-f836-45ab-8ef0-113b1f9ad433"), kick="마무리"),
        section("다음", "1교시 · Agent 구조와 Context Window", "판단과 실행 · 입력 구성 · 첫 RAG"),
    ]


def slides():
    return opening() + block_way() + block_project() + block_setup() + closing()
