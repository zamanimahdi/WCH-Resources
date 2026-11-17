"""Small macOS changes for desktop/wch_configurator.py (WCH Configurator desktop shell).

    python3 desktop/patch_macos.py [desktop/wch_configurator.py]

Run it once on the desktop-app branch and commit the result; it is idempotent
(a second run changes nothing). What it changes:
  * IS_MAC flag
  * storage path on macOS: ~/Library/Application Support/WCH-Configurator
  * gui=None on macOS, so pywebview uses its Cocoa (WKWebView) backend
  * clipboard fallback: pbcopy on macOS
  * start path: ignore every argument that starts with "-" (old macOS passes -psn_...)
  * docstring / About text: Windows, Linux and macOS
Windows and Linux behaviour stays the same.
"""
import os
import sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "wch_configurator.py")
s = open(path, encoding="utf-8", newline="").read()
if "IS_MAC = " in s:
    print("already patched:", path)
    sys.exit(0)


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, "anchor found %d times: %r" % (n, old[:80])
    s = s.replace(old, new)


rep('WCH Configurator - Desktop edition (Windows and Linux)',
    'WCH Configurator - Desktop edition (Windows, Linux and macOS)')
rep('    WebKitGTK on Linux),',
    '    WebKitGTK on Linux, WKWebView on macOS),')
rep('IS_WIN = sys.platform.startswith("win")',
    'IS_WIN = sys.platform.startswith("win")\nIS_MAC = sys.platform == "darwin"')
rep('        for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):',
    '        cmds = (["pbcopy"],) if IS_MAC else (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"])\n'
    '        for cmd in cmds:')
rep('Desktop edition for Windows and Linux: zamanimahdi',
    'Desktop edition for Windows, Linux and macOS: zamanimahdi')
rep('    start_path = next((a for a in sys.argv[1:] if not a.startswith("--")), None)',
    '    start_path = next((a for a in sys.argv[1:] if not a.startswith("-")), None)')
rep('''        gui = "edgechromium"
    else:
''', '''        gui = "edgechromium"
    elif IS_MAC:
        storage = os.path.join(os.path.expanduser("~/Library/Application Support"), "WCH-Configurator")
        gui = os.environ.get("WCH_GUI") or None   # pywebview uses Cocoa (WKWebView) on macOS
    else:
''')

open(path, "w", encoding="utf-8", newline="").write(s)
print("patched for macOS:", path)
