# -*- coding: utf-8 -*-
"""
nk_credit.py - credit + animated splash screen for Nuke tools
Author  : Nitin Kashyap
Support : Nuke 10 -> 16   (Python 2.7 / 3.7 / 3.9 / 3.10 / 3.11)
          PySide (Qt4), PySide2 (Qt5) and PySide6 (Qt6) are all detected.

INSTALL
    1. Copy this file into ~/.nuke
    2. In ~/.nuke/menu.py:
           import nk_credit
           nk_credit.install()
"""
import datetime
import os
import time

import nuke

# ---------------------------------------------------------------------------
# Qt binding: PySide2 (Nuke 11-15), PySide6 (Nuke 16+), PySide (Nuke 10)
# ---------------------------------------------------------------------------
QtCore = QtGui = QtWidgets = None
QT_BINDING = None
QT_FILE = None


def _load_qt():
    """Import the Qt binding that Nuke itself uses (chosen by Nuke version).
    Never guess: a PySide2 installed on the system path would create a second,
    separate Qt and give 'Must construct a QApplication before a QWidget'."""
    major = nuke.NUKE_VERSION_MAJOR
    if major < 11:
        import PySide
        from PySide import QtCore as core, QtGui as gui
        return "PySide", PySide, core, gui, gui
    if major < 16:
        import PySide2
        from PySide2 import QtCore as core, QtGui as gui, QtWidgets as wid
        return "PySide2", PySide2, core, gui, wid
    import PySide6
    from PySide6 import QtCore as core, QtGui as gui, QtWidgets as wid
    return "PySide6", PySide6, core, gui, wid


try:
    QT_BINDING, _mod, QtCore, QtGui, QtWidgets = _load_qt()
    QT_FILE = getattr(_mod, "__file__", "?")
except ImportError:
    pass
HAS_QT = QT_BINDING is not None


# ------------------------------- SETTINGS -------------------------------
CONFIG = {
    "enabled":          True,                # False = module does nothing (kill switch)
    "author":           "Nitin Kashyap",
    "tool_name":        "Lens Edge Extend",
    "version":          "v2.0",
    "contact":          "",                  # e.g. "you@email.com" (empty = hidden)
    "node_prefix":      "Lens_Edge_Extend",  # matches node name or class
    "marker_knob":      "lensChoice",        # matches the node even if it is renamed
    "show_label":       True,                # "by <author>" under the node
    "label_color":      0xffd166ff,          # 0xRRGGBBAA
    "label_size":       14,
    "splash_seconds":   3.5,
    "splash_on_create": False,               # splash when a node is created (off = safest)
    "auto_credit":      False,               # the gizmo already carries the credit knobs
}

CREDIT_KNOBS = ("credit_div", "credit", "credit_ver", "about_btn")
_SESSION = {"splash_shown": False}
_splash = None   # keeps a reference so the window is not garbage collected


# ------------------------------- HELPERS --------------------------------
def _hsv(h, s=0.9, v=1.0):
    return QtGui.QColor.fromHsvF(h % 1.0, s, v)


def _adv(fm, text):
    """Text width: horizontalAdvance (Qt 5.11+/6) or width (older Qt)."""
    fn = getattr(fm, "horizontalAdvance", None) or fm.width
    return fn(text)


def _center_geometry():
    app = QtWidgets.QApplication
    active = app.activeWindow()
    if active is not None:
        return active.geometry()
    try:
        return app.primaryScreen().geometry()          # Qt5 / Qt6
    except AttributeError:
        return app.desktop().screenGeometry()          # Qt4


def _rainbow_html(text, palette=None):
    palette = palette or ["#ff5f6d", "#ffc371", "#fff36b", "#7bd88f",
                          "#2ec4ff", "#8e7dff", "#ff6bd6"]
    out, i = [], 0
    for ch in text:
        if ch == " ":
            out.append("&nbsp;")
            continue
        out.append("<font color='%s'><b>%s</b></font>" % (palette[i % len(palette)], ch))
        i += 1
    return "".join(out)


# ------------------------------- SPLASH ---------------------------------
_Base = QtWidgets.QWidget if HAS_QT else object


def _disabled():
    return (not CONFIG["enabled"]) or bool(os.environ.get("NK_CREDIT_DISABLE"))


class Splash(_Base):
    """Splash window. Created once and reused, so nothing is ever deleted
    while Qt may still be using it (no WA_DeleteOnClose, no animation objects)."""
    FADE_IN = 0.35
    FADE_OUT = 0.40

    def __init__(self):
        super(Splash, self).__init__()
        self.setWindowFlags(QtCore.Qt.SplashScreen |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(560, 300)
        self._seconds = 3.5
        self._phase = 0.0
        self._start = time.time()
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._tick)

    # ---- control ----
    def restart(self, seconds):
        self._seconds = max(float(seconds), 0.5)
        self._phase = 0.0
        self._start = time.time()
        self._timer.start(33)
        self.show()
        self.raise_()

    def _finish(self):
        self._timer.stop()
        self.hide()

    def _elapsed(self):
        return time.time() - self._start

    def _alpha(self):
        e = self._elapsed()
        fin = min(1.0, max(0.0, e / self.FADE_IN))
        fout = min(1.0, max(0.0, 1.0 - (e - self._seconds) / self.FADE_OUT))
        return min(fin, fout)

    def _tick(self):
        self._phase += 0.004
        if self._elapsed() >= self._seconds + self.FADE_OUT:
            self._finish()
        else:
            self.update()

    # ---- events ----
    def mousePressEvent(self, event):
        e = self._elapsed()
        if e < self._seconds:                    # jump to the fade-out
            self._start -= (self._seconds - e)

    def keyPressEvent(self, event):
        self.mousePressEvent(event)

    # ---- drawing ----
    def _rainbow_text(self, p, text, y, size):
        font = QtGui.QFont("Arial", size)
        font.setBold(True)
        p.setFont(font)
        fm = QtGui.QFontMetrics(font)
        total = sum(_adv(fm, c) for c in text)
        x = (self.width() - total) / 2.0
        for i, ch in enumerate(text):
            p.setPen(_hsv(self._phase * 3 + i * 0.06))
            p.drawText(QtCore.QPointF(x, y), ch)
            x += _adv(fm, ch)

    def _plain_text(self, p, text, y, size, color, bold=False):
        font = QtGui.QFont("Arial", size)
        font.setBold(bold)
        p.setFont(font)
        p.setPen(QtGui.QColor(color))
        rect = QtCore.QRectF(0, y - size * 2, self.width(), size * 3)
        p.drawText(rect, text, QtGui.QTextOption(QtCore.Qt.AlignCenter))

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            p.setRenderHint(QtGui.QPainter.TextAntialiasing)
            p.setOpacity(self._alpha())

            rect = QtCore.QRectF(self.rect()).adjusted(3, 3, -3, -3)
            grad = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0.0, _hsv(self._phase, 0.65, 0.28))
            grad.setColorAt(1.0, _hsv(self._phase + 0.25, 0.75, 0.38))
            p.setBrush(QtGui.QBrush(grad))
            p.setPen(QtGui.QPen(_hsv(self._phase * 2 + 0.5, 0.8, 1.0), 2))
            p.drawRoundedRect(rect, 22, 22)

            c = CONFIG
            self._rainbow_text(p, c["tool_name"], 105, 30)
            self._plain_text(p, u"created by", 150, 11, "#cfd8ff")
            self._rainbow_text(p, c["author"], 195, 22)
            self._plain_text(p, u"%s   \u25cf   \u00a9 %d" % (c["version"], datetime.date.today().year),
                             232, 11, "#ffd166", True)
            if c["contact"]:
                self._plain_text(p, c["contact"], 254, 10, "#7bd88f")

            frac = min(1.0, self._elapsed() / self._seconds)
            bar = QtCore.QRectF(40, self.height() - 22, self.width() - 80, 5)
            p.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            p.setBrush(QtGui.QColor(255, 255, 255, 40))
            p.drawRoundedRect(bar, 2.5, 2.5)
            fill = QtCore.QRectF(bar.left(), bar.top(), bar.width() * frac, bar.height())
            p.setBrush(_hsv(self._phase * 3))
            p.drawRoundedRect(fill, 2.5, 2.5)
        finally:
            p.end()                                # always release the painter


def show_splash(seconds=None):
    """Open the splash screen centered on the active window."""
    global _splash
    if _disabled() or not nuke.GUI or not HAS_QT:
        print("%s %s by %s" % (CONFIG["tool_name"], CONFIG["version"], CONFIG["author"]))
        return
    if QtWidgets.QApplication.instance() is None:
        print("nk_credit: no QApplication (Qt: %s). Splash skipped." % QT_BINDING)
        return
    try:
        if _splash is None:
            _splash = Splash()
        geo = _center_geometry()
        _splash.move(geo.center().x() - _splash.width() // 2,
                     geo.center().y() - _splash.height() // 2)
        _splash.restart(seconds if seconds is not None else CONFIG["splash_seconds"])
    except Exception as e:
        print("nk_credit: splash failed (%s)" % e)


# ------------------------------- CREDIT ---------------------------------
def _matches(n):
    c = CONFIG
    try:
        if n.name().startswith(c["node_prefix"]) or n.Class().startswith(c["node_prefix"]):
            return True
        return bool(c["marker_knob"]) and n.knob(c["marker_knob"]) is not None
    except Exception:
        return False


def _clean(n):
    """Remove old credit knobs and any Text_Knob that holds pasted code."""
    for name, k in list(n.knobs().items()):
        if name in CREDIT_KNOBS:
            n.removeKnob(k)
            continue
        if k.Class() == "Text_Knob":
            try:
                txt = k.value()
            except Exception:
                txt = ""
            if "import nuke" in txt or "nuke.thisNode" in txt:
                n.removeKnob(k)


ABOUT_STUB = (
    "import nuke\n"
    "try:\n"
    "    import nk_credit\n"
    "    nk_credit.show_splash()\n"
    "except ImportError:\n"
    "    nuke.message('%s %s\\n\\nCreated by %s')\n"
)


def _credit_line():
    c = CONFIG
    return ("%s &nbsp;<font color='#8a8a8a'>by</font>&nbsp; %s "
            "&nbsp;<font color='#ffd166'>%s &bull; %d</font>"
            % (_rainbow_html(c["tool_name"]), _rainbow_html(c["author"]),
               c["version"], datetime.date.today().year))


def add_credit(n):
    """Add the credit to a node, or refresh it if the gizmo already has it."""
    c = CONFIG
    stub = ABOUT_STUB % (c["tool_name"], c["version"], c["author"])

    if n.knob("credit") is not None and n.knob("about_btn") is not None:
        n["credit"].setValue(_credit_line())          # gizmo already carries the knobs
        n["about_btn"].setValue(stub)
    else:
        _clean(n)
        n.addKnob(nuke.Text_Knob("credit_div", ""))
        n.addKnob(nuke.Text_Knob("credit", "", _credit_line()))
        about = nuke.PyScript_Knob("about_btn", "About / Splash")
        about.setValue(stub)
        n.addKnob(about)

    if c["show_label"]:
        n["label"].setValue("by %s" % c["author"])
        n["note_font_color"].setValue(c["label_color"])
        n["note_font_size"].setValue(c["label_size"])


def remove_credit(nodes=None):
    """Remove the credit knobs and label from the given (or selected) nodes."""
    nodes = nodes or [x for x in nuke.selectedNodes() if _matches(x)]
    for n in nodes:
        for name in CREDIT_KNOBS:
            k = n.knob(name)
            if k:
                n.removeKnob(k)
        n["label"].setValue("")
    print("Credit removed from %d node(s)" % len(nodes))


# ------------------------------- CALLBACK -------------------------------
def _on_create():
    n = nuke.thisNode()
    if not _matches(n):
        return
    try:
        if CONFIG["auto_credit"]:
            add_credit(n)
        if (CONFIG["splash_on_create"] and not _SESSION["splash_shown"]
                and nuke.GUI and HAS_QT):
            _SESSION["splash_shown"] = True
            QtCore.QTimer.singleShot(200, show_splash)
    except Exception as e:                       # a credit problem must never break node creation
        print("nk_credit: %s" % e)


def install():
    """Register the auto-credit callback (call once from menu.py)."""
    if _disabled():
        print("nk_credit: disabled")
        return
    try:
        nuke.removeOnUserCreate(_on_create)
    except Exception:
        pass
    if CONFIG["auto_credit"] or CONFIG["splash_on_create"]:
        nuke.addOnUserCreate(_on_create)
    print("nk_credit installed: %s %s by %s | Nuke %s | Qt: %s" % (
        CONFIG["tool_name"], CONFIG["version"], CONFIG["author"],
        nuke.NUKE_VERSION_STRING, QT_BINDING))
    print("nk_credit: Qt module file: %s" % QT_FILE)


# ------------------------------- MANUAL RUN -----------------------------
def run():
    """Apply credit to the selected matching nodes and show the splash."""
    targets = [x for x in nuke.selectedNodes() if _matches(x)]
    if not targets:
        nuke.message("Select a %s node first." % CONFIG["node_prefix"])
        return
    undo = nuke.Undo()
    undo.begin("Add credit")
    try:
        for n in targets:
            add_credit(n)
            print("Credit added to %s" % n.name())
    finally:
        undo.end()
    show_splash()


if __name__ == "__main__":
    run()