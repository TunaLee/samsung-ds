"""부록 · 명령어 모음 도해 (s9-)."""
from fig import _tile


def _row(parts, arrow=False):
    sep = '<div class="s9-arr">→</div>' if arrow else ""
    return f'<div class="s9-row">{sep.join(parts)}</div>'


def where():
    """입력 위치: PowerShell → 대화 입력창."""
    return _row([
        _tile("window", "PowerShell", "<code>claude</code>로 시작하는 명령<br>실행 옵션 · 하위 명령"),
        _tile("chat", "대화 입력창", "<code>/</code>로 시작하는 명령<br>자연어 작업 요청", "core"),
    ], arrow=True)


def tidy():
    """/clear · /compact · /rewind 선택."""
    return _row([
        _tile("doc", "/clear", "다른 작업으로 전환<br>예: 화면 수정 후 다른 API 작업"),
        _tile("rule", "/compact", "같은 작업 계속 · 대화가 길어짐<br>예: 같은 오류를 계속 추적"),
        _tile("check", "/rewind", "직전 수정부터 문제 발생<br>복원 대상 먼저 확인"),
    ])


def settings_files():
    """설정 파일 세 범위."""
    return ('<div class="s9-row s9-sm">'
            + _tile("folder", "프로젝트 공유", "<code>.claude/settings.json</code>")
            + _tile("key", "개인 · 프로젝트별", "<code>.claude/settings.local.json</code>")
            + _tile("model", "사용자 공통", "<code>~/.claude/settings.json</code><br>Windows의 <code>~</code> = 사용자 홈 폴더")
            + '</div>')


def scopes():
    """MCP 등록 범위."""
    return ('<div class="s9-row s9-sm">'
            + _tile("key", "--scope local", "이 프로젝트 · 개인용<br><b>기본 범위</b>", "core")
            + _tile("folder", "--scope project", "프로젝트의 <code>.mcp.json</code><br>공유 설정")
            + _tile("globe", "--scope user", "여러 프로젝트<br>개인 공통")
            + '</div>')


def two_targets():
    """MCP: Claude Code에 연결 vs 제작 중인 앱에 연결."""
    return _row([
        _tile("model", "Claude Code에 연결", "<code>claude mcp add</code> → <code>/mcp</code>로 확인", "core"),
        _tile("window", "제작 중인 앱에 연결", "앱 코드 · 설정 변경 요청<br>앱 화면에서 연결 결과 확인"),
    ])
