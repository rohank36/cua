import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL('user32', use_last_error=True)

# --- Win32 constants ---
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE        = 0x0001
MOUSEEVENTF_ABSOLUTE    = 0x8000

SM_CXSCREEN = 0
SM_CYSCREEN = 1

# --- Fix: define ULONG_PTR ourselves ---
if ctypes.sizeof(ctypes.c_void_p) == ctypes.sizeof(ctypes.c_ulonglong):
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

# --- Win32 structures for SendInput ---
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx',          wintypes.LONG),
                ('dy',          wintypes.LONG),
                ('mouseData',   wintypes.DWORD),
                ('dwFlags',     wintypes.DWORD),
                ('time',        wintypes.DWORD),
                ('dwExtraInfo', ULONG_PTR))

class INPUT_UNION(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),)

class INPUT(ctypes.Structure):
    _fields_ = (('type',   wintypes.DWORD),
                ('union',  INPUT_UNION))

SendInput = user32.SendInput
SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
SendInput.restype  = wintypes.UINT

GetSystemMetrics = user32.GetSystemMetrics
GetSystemMetrics.argtypes = (ctypes.c_int,)
GetSystemMetrics.restype  = ctypes.c_int

def _send_mouse(dx, dy, flags):
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi = MOUSEINPUT(dx, dy, 0, flags, 0, 0)
    n_sent = SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    if n_sent != 1:
        raise ctypes.WinError(ctypes.get_last_error())

def move_relative(dx: int, dy: int):
    _send_mouse(dx, dy, MOUSEEVENTF_MOVE)

def move_absolute(x: int, y: int):
    w = GetSystemMetrics(SM_CXSCREEN)
    h = GetSystemMetrics(SM_CYSCREEN)
    nx = int(x * 65535 / (w - 1))
    ny = int(y * 65535 / (h - 1))
    _send_mouse(nx, ny, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE)

# Example usage
if __name__ == "__main__":
    move_relative(100, 0)   # move 100 px right
    move_relative(0, 100)   # move 100 px down
    move_absolute(200, 200) # jump to (200,200)
