import win32gui
import win32api
import win32con


def get_mouse_cursor_position():
    """마우스가 현재 화면에서 위치하고 있는 좌표를 출력한다."""
    print(win32gui.GetCursorInfo())


def open_kakao_talk():
    """카카오톡을 실행한다."""
    handle = win32api.ShellExecute(
        0,  # no parent
        'open',
        'C:\\Program Files (x86)\\Kakao\\KakaoTalk\\KakaoTalk.exe',
        None,
        None,
        win32con.SW_SHOWNORMAL,
    )
    print('instance handle: {}'.format(handle))
    return handle


def set_window_foreground(title):
    """주어진 제목의 윈도우 애플리케이션을 앞으로 활성화 한다."""

    def window_enumeration_handler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    windows = []
    win32gui.EnumWindows(window_enumeration_handler, windows)

    for handle, name in windows:
        if title in name.lower():
            win32gui.ShowWindow(handle, 5)
            win32gui.SetForegroundWindow(handle)
            return handle


