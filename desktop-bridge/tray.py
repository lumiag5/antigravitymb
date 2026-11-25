# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import struct
import tempfile
import threading
import webbrowser
from pathlib import Path
from typing import Callable, Optional

IS_WINDOWS = sys.platform.startswith("win")

if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    shell32 = ctypes.windll.shell32
    kernel32 = ctypes.windll.kernel32

    LRESULT = ctypes.c_ssize_t
    WNDPROCTYPE = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

    WS_OVERLAPPED = 0x00000000
    WM_DESTROY = 0x0002
    WM_CLOSE = 0x0010
    WM_COMMAND = 0x0111
    WM_USER = 0x0400
    WM_TRAYICON = WM_USER + 20
    WM_LBUTTONUP = 0x0202
    WM_LBUTTONDBLCLK = 0x0203
    WM_RBUTTONUP = 0x0205

    SW_HIDE = 0
    SW_RESTORE = 9

    NIM_ADD = 0x00000000
    NIM_MODIFY = 0x00000001
    NIM_DELETE = 0x00000002

    NIF_MESSAGE = 0x00000001
    NIF_ICON = 0x00000002
    NIF_TIP = 0x00000004
    NIF_INFO = 0x00000010
    NIIF_INFO = 0x00000001

    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    LR_DEFAULTSIZE = 0x00000040
    IDI_APPLICATION = 32512

    TPM_LEFTALIGN = 0x0000
    TPM_BOTTOMALIGN = 0x0020
    TPM_RIGHTBUTTON = 0x0002
    TPM_RETURNCMD = 0x0100
    MF_STRING = 0x00000000
    MF_SEPARATOR = 0x00000800

    class WNDCLASSEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.UINT),
            ("style", wintypes.UINT),
            ("lpfnWndProc", WNDPROCTYPE),
            ("cbClsExtra", ctypes.c_int),
            ("cbWndExtra", ctypes.c_int),
            ("hInstance", wintypes.HINSTANCE),
            ("hIcon", wintypes.HICON),
            ("hCursor", wintypes.HANDLE),
            ("hbrBackground", wintypes.HBRUSH),
            ("lpszMenuName", wintypes.LPCWSTR),
            ("lpszClassName", wintypes.LPCWSTR),
            ("hIconSm", wintypes.HICON),
        ]

    class NOTIFYICONDATAW(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("hWnd", wintypes.HWND),
            ("uID", wintypes.UINT),
            ("uFlags", wintypes.UINT),
            ("uCallbackMessage", wintypes.UINT),
            ("hIcon", wintypes.HICON),
            ("szTip", wintypes.WCHAR * 128),
            ("dwState", wintypes.DWORD),
            ("dwStateMask", wintypes.DWORD),
            ("szInfo", wintypes.WCHAR * 256),
            ("uVersion", wintypes.UINT),
            ("szInfoTitle", wintypes.WCHAR * 64),
            ("dwInfoFlags", wintypes.DWORD),
        ]

    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.DefWindowProcW.restype = LRESULT


def _build_ico_from_png(png_path: Path) -> Optional[Path]:
    """Cria um arquivo .ico temporário encapsulando o PNG oficial (suportado nativamente pelo Windows)."""
    if not png_path.exists():
        return None
    try:
        png_bytes = png_path.read_bytes()
        # ICONDIR (6 bytes) + ICONDIRENTRY (16 bytes) + PNG payload
        icondir = struct.pack("<HHH", 0, 1, 1)
        entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png_bytes), 22)
        ico_path = Path(tempfile.gettempdir()) / "antigravity_mobile_tray.ico"
        ico_path.write_bytes(icondir + entry + png_bytes)
        return ico_path
    except Exception:
        return None


class WindowsTrayManager:
    """Ícone nativo na bandeja do Windows (System Tray) sem dependências externas."""

    CMD_TOGGLE = 1001
    CMD_OPEN_WEB = 1002
    CMD_NEW_PIN = 1003
    CMD_CHECK_UPDATE = 1004
    CMD_EXIT = 1005

    def __init__(self):
        self._hwnd = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._wnd_proc_ref = None
        self._on_new_pin: Optional[Callable[[], None]] = None
        self._on_check_update: Optional[Callable[[], None]] = None
        self._on_exit: Optional[Callable[[], None]] = None
        self._get_url: Optional[Callable[[], str]] = None
        self._get_labels: Optional[Callable[[], dict]] = None
        self._icon_handle = None

    def is_supported(self) -> bool:
        return IS_WINDOWS and bool(kernel32.GetConsoleWindow())

    def is_console_visible(self) -> bool:
        if not IS_WINDOWS:
            return True
        hwnd = kernel32.GetConsoleWindow()
        if not hwnd:
            return True
        return bool(user32.IsWindowVisible(hwnd))

    def hide_console(self, notify: bool = True):
        if not IS_WINDOWS:
            return
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, SW_HIDE)
            if notify:
                labels = self._get_labels() if self._get_labels else {}
                self.show_balloon(
                    labels.get("tray_minimized_title", "Antigravity Mobile"),
                    labels.get("tray_minimized_msg", "Rodando em segundo plano na bandeja. Clique no ícone para abrir.")
                )

    def restore_console(self):
        if not IS_WINDOWS:
            return
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, SW_RESTORE)
            user32.SetForegroundWindow(hwnd)

    def toggle_console(self):
        if self.is_console_visible():
            self.hide_console(notify=False)
        else:
            self.restore_console()

    def show_balloon(self, title: str, message: str):
        if not IS_WINDOWS or not self._hwnd:
            return
        try:
            nid = NOTIFYICONDATAW()
            nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
            nid.hWnd = self._hwnd
            nid.uID = 1
            nid.uFlags = NIF_INFO
            nid.szInfoTitle = title[:63]
            nid.szInfo = message[:255]
            nid.dwInfoFlags = NIIF_INFO
            shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))
        except Exception:
            pass

    def start(
        self,
        icon_png: Path,
        on_new_pin: Optional[Callable[[], None]] = None,
        on_check_update: Optional[Callable[[], None]] = None,
        on_exit: Optional[Callable[[], None]] = None,
        get_url: Optional[Callable[[], str]] = None,
        get_labels: Optional[Callable[[], dict]] = None,
    ):
        if not IS_WINDOWS or self._running:
            return

        self._on_new_pin = on_new_pin
        self._on_check_update = on_check_update
        self._on_exit = on_exit
        self._get_url = get_url
        self._get_labels = get_labels
        self._running = True

        def _tray_loop():
            try:
                hinst = kernel32.GetModuleHandleW(None)
                class_name = f"AntigravityTray_{os.getpid()}"

                def _wnd_proc(hwnd, msg, wparam, lparam):
                    if msg == WM_TRAYICON:
                        if lparam in (WM_LBUTTONUP, WM_LBUTTONDBLCLK):
                            self.toggle_console()
                        elif lparam == WM_RBUTTONUP:
                            self._show_context_menu(hwnd)
                        return 0
                    elif msg == WM_COMMAND:
                        cmd_id = wparam & 0xFFFF
                        self._handle_command(cmd_id)
                        return 0
                    elif msg == WM_DESTROY:
                        user32.PostQuitMessage(0)
                        return 0
                    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

                self._wnd_proc_ref = WNDPROCTYPE(_wnd_proc)
                wc = WNDCLASSEXW()
                wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
                wc.lpfnWndProc = self._wnd_proc_ref
                wc.hInstance = hinst
                wc.lpszClassName = class_name
                user32.RegisterClassExW(ctypes.byref(wc))

                self._hwnd = user32.CreateWindowExW(
                    0, class_name, "Antigravity Mobile Tray", WS_OVERLAPPED,
                    0, 0, 0, 0, None, None, hinst, None
                )
                if not self._hwnd:
                    self._running = False
                    return

                ico_path = _build_ico_from_png(icon_png)
                if ico_path and ico_path.exists():
                    self._icon_handle = user32.LoadImageW(
                        None, str(ico_path), IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE
                    )
                if not self._icon_handle:
                    self._icon_handle = user32.LoadIconW(None, IDI_APPLICATION)

                nid = NOTIFYICONDATAW()
                nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
                nid.hWnd = self._hwnd
                nid.uID = 1
                nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
                nid.uCallbackMessage = WM_TRAYICON
                nid.hIcon = self._icon_handle
                nid.szTip = "Antigravity Mobile - Local Server"
                shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid))

                msg = wintypes.MSG()
                while self._running and user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
            except Exception:
                pass
            finally:
                self._cleanup_icon()

        self._thread = threading.Thread(target=_tray_loop, daemon=True)
        self._thread.start()

    def _show_context_menu(self, hwnd):
        labels = self._get_labels() if self._get_labels else {}
        hmenu = user32.CreatePopupMenu()
        if not hmenu:
            return

        toggle_txt = (
            labels.get("tray_hide_terminal", "Ocultar terminal")
            if self.is_console_visible()
            else labels.get("tray_show_terminal", "Mostrar terminal")
        )
        user32.AppendMenuW(hmenu, MF_STRING, self.CMD_TOGGLE, toggle_txt)
        user32.AppendMenuW(hmenu, MF_STRING, self.CMD_OPEN_WEB, labels.get("tray_open_browser", "Abrir no navegador"))
        user32.AppendMenuW(hmenu, MF_STRING, self.CMD_NEW_PIN, labels.get("tray_new_pin", "Gerar novo PIN"))
        user32.AppendMenuW(hmenu, MF_STRING, self.CMD_CHECK_UPDATE, labels.get("tray_check_update", "Atualizar servidor (GitHub)"))
        user32.AppendMenuW(hmenu, MF_SEPARATOR, 0, None)
        user32.AppendMenuW(hmenu, MF_STRING, self.CMD_EXIT, labels.get("tray_exit", "Encerrar servidor"))

        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        user32.SetForegroundWindow(hwnd)
        cmd = user32.TrackPopupMenu(
            hmenu,
            TPM_LEFTALIGN | TPM_BOTTOMALIGN | TPM_RIGHTBUTTON | TPM_RETURNCMD,
            pt.x, pt.y, 0, hwnd, None
        )
        user32.DestroyMenu(hmenu)
        if cmd:
            self._handle_command(cmd)

    def _handle_command(self, cmd_id: int):
        if cmd_id == self.CMD_TOGGLE:
            self.toggle_console()
        elif cmd_id == self.CMD_OPEN_WEB:
            if self._get_url:
                try:
                    webbrowser.open(self._get_url())
                except Exception:
                    pass
        elif cmd_id == self.CMD_NEW_PIN:
            if self._on_new_pin:
                threading.Thread(target=self._on_new_pin, daemon=True).start()
        elif cmd_id == self.CMD_CHECK_UPDATE:
            self.restore_console()
            if self._on_check_update:
                threading.Thread(target=self._on_check_update, daemon=True).start()
        elif cmd_id == self.CMD_EXIT:
            self.restore_console()
            if self._on_exit:
                self._on_exit()

    def _cleanup_icon(self):
        if not IS_WINDOWS or not self._hwnd:
            return
        try:
            nid = NOTIFYICONDATAW()
            nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
            nid.hWnd = self._hwnd
            nid.uID = 1
            shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(nid))
        except Exception:
            pass
        self._hwnd = None

    def stop(self):
        self._running = False
        if IS_WINDOWS and self._hwnd:
            try:
                user32.PostMessageW(self._hwnd, WM_CLOSE, 0, 0)
            except Exception:
                pass
        self._cleanup_icon()


tray_manager = WindowsTrayManager()
