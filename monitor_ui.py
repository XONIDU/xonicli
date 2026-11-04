#!/usr/bin/env python3
"""Monitor Web UI: muestra varias paginas web a la vez en una cuadricula.

- Agregar / quitar webs (pide la URL)
- Refresco automatico por panel
- Maximizar un panel
- Configuracion guardada en ~/.config/monitor-web/config.json
"""
import json
import math
import sys
from pathlib import Path
from urllib.parse import urlparse

from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication, QFrame, QGridLayout, QHBoxLayout, QInputDialog, QLabel,
    QMainWindow, QMessageBox, QSpinBox, QToolBar, QToolButton, QVBoxLayout,
    QWidget,
)

APP_NAME = "monitor-web"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "columns": 0,  # 0 = automatico
    "sites": [
        {"title": "SERVIR Alertas",
         "url": "https://www.servir.net/servir_alertas/index-new.php",
         "refresh": 0},
        {"title": "Windy",
         "url": "https://embed.windy.com/embed2.html?lat=20.166&lon=-98.965&zoom=10&overlay=wind",
         "refresh": 0},
    ],
}


def load_config():
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        data.setdefault("columns", 0)
        data.setdefault("sites", [])
        return data
    except (OSError, ValueError):
        return json.loads(json.dumps(DEFAULT_CONFIG))


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_url(text):
    text = text.strip()
    if not text:
        return ""
    if "://" not in text:
        text = "https://" + text
    return text


def default_title(url):
    return urlparse(url).netloc or url


class Panel(QFrame):
    removeRequested = pyqtSignal(object)
    maximizeRequested = pyqtSignal(object)
    changed = pyqtSignal()

    def __init__(self, site, profile, parent=None):
        super().__init__(parent)
        self.site = site
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        header = QHBoxLayout()
        header.setContentsMargins(4, 0, 4, 0)
        self.title_label = QLabel()
        self.title_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        header.addWidget(self.title_label, 1)

        self.btn_reload = self._button("R", "Recargar", self.reload)
        self.btn_timer = self._button("T", "Refresco automatico (minutos)", self.ask_interval)
        self.btn_edit = self._button("E", "Editar titulo / URL", self.edit_site)
        self.btn_max = self._button("M", "Maximizar / restaurar", lambda: self.maximizeRequested.emit(self))
        self.btn_close = self._button("X", "Quitar este panel", lambda: self.removeRequested.emit(self))
        for b in (self.btn_reload, self.btn_timer, self.btn_edit, self.btn_max, self.btn_close):
            header.addWidget(b)
        layout.addLayout(header)

        self.view = QWebEngineView()
        self.page = QWebEnginePage(profile, self.view)
        self.view.setPage(self.page)
        self.page.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.page.fullScreenRequested.connect(lambda req: req.accept())
        self.page.titleChanged.connect(self._page_title_changed)
        layout.addWidget(self.view, 1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reload)

        self.apply_site()

    def _button(self, text, tip, slot):
        b = QToolButton()
        b.setText(text)
        b.setToolTip(tip)
        b.setAutoRaise(True)
        b.clicked.connect(lambda _=False: slot())
        return b

    def apply_site(self):
        self.view.setUrl(QUrl(self.site["url"]))
        self._update_title()
        self._update_timer()

    def _update_title(self, page_title=None):
        title = self.site.get("title") or page_title or default_title(self.site["url"])
        refresh = self.site.get("refresh", 0)
        suffix = f"  -  T {refresh} min" if refresh else ""
        self.title_label.setText(f"<b>{title}</b>{suffix}")
        self.title_label.setToolTip(self.site["url"])

    def _page_title_changed(self, title):
        if not self.site.get("title"):
            self._update_title(title)

    def _update_timer(self):
        minutes = int(self.site.get("refresh", 0) or 0)
        if minutes > 0:
            self.timer.start(minutes * 60 * 1000)
        else:
            self.timer.stop()

    def reload(self):
        self.view.reload()

    def ask_interval(self):
        current = int(self.site.get("refresh", 0) or 0)
        value, ok = QInputDialog.getInt(
            self, "Refresco automatico",
            "Recargar cada cuantos minutos (0 = nunca):", current, 0, 1440)
        if ok:
            self.site["refresh"] = value
            self._update_title()
            self._update_timer()
            self.changed.emit()

    def edit_site(self):
        url, ok = QInputDialog.getText(self, "Editar URL", "URL:", text=self.site["url"])
        if not ok:
            return
        url = normalize_url(url)
        if not url:
            return
        title, ok = QInputDialog.getText(
            self, "Editar titulo", "Titulo (vacio = usar el de la pagina):",
            text=self.site.get("title", ""))
        if not ok:
            return
        self.site["url"] = url
        self.site["title"] = title.strip()
        self.apply_site()
        self.changed.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor Web")
        self.resize(1400, 850)

        self.cfg = load_config()
        self.profile = QWebEngineProfile(APP_NAME, self)  # perfil persistente
        self.panels = []
        self.maximized_panel = None

        central = QWidget()
        self.grid = QGridLayout(central)
        self.grid.setContentsMargins(2, 2, 2, 2)
        self.grid.setSpacing(2)
        self.setCentralWidget(central)

        self._build_toolbar()

        for site in self.cfg["sites"]:
            self._create_panel(site)
        self.relayout()

        if not self.panels:
            self.add_site()

    # ---------- interfaz ----------
    def _build_toolbar(self):
        tb = QToolBar("Principal")
        tb.setMovable(False)
        self.addToolBar(tb)

        act_add = QAction("Agregar web", self)
        act_add.setShortcut(QKeySequence("Ctrl+N"))
        act_add.triggered.connect(self.add_site)
        tb.addAction(act_add)

        act_reload = QAction("Recargar todo", self)
        act_reload.setShortcut(QKeySequence("F5"))
        act_reload.triggered.connect(lambda: [p.reload() for p in self.panels])
        tb.addAction(act_reload)

        tb.addSeparator()
        tb.addWidget(QLabel(" Columnas (0 = auto): "))
        self.spin_cols = QSpinBox()
        self.spin_cols.setRange(0, 8)
        self.spin_cols.setValue(int(self.cfg.get("columns", 0)))
        self.spin_cols.valueChanged.connect(self._columns_changed)
        tb.addWidget(self.spin_cols)

        tb.addSeparator()
        act_full = QAction("Pantalla completa", self)
        act_full.setShortcut(QKeySequence("F11"))
        act_full.triggered.connect(self.toggle_fullscreen)
        tb.addAction(act_full)

    def toggle_fullscreen(self):
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    # ---------- paneles ----------
    def _create_panel(self, site):
        panel = Panel(site, self.profile)
        panel.removeRequested.connect(self.remove_panel)
        panel.maximizeRequested.connect(self.toggle_maximize)
        panel.changed.connect(self.save)
        self.panels.append(panel)
        return panel

    def add_site(self):
        url, ok = QInputDialog.getText(
            self, "Agregar web", "URL de la pagina a monitorear:")
        if not ok:
            return
        url = normalize_url(url)
        if not url:
            return
        title, ok = QInputDialog.getText(
            self, "Titulo", "Titulo del panel (opcional):")
        if not ok:
            title = ""
        site = {"title": title.strip(), "url": url, "refresh": 0}
        self.cfg["sites"].append(site)
        self._create_panel(site)
        self.maximized_panel = None
        self.relayout()
        self.save()

    def remove_panel(self, panel):
        if QMessageBox.question(
                self, "Quitar panel",
                f"Quitar «{panel.site.get('title') or panel.site['url']}»?"
        ) != QMessageBox.StandardButton.Yes:
            return
        if self.maximized_panel is panel:
            self.maximized_panel = None
        self.panels.remove(panel)
        self.cfg["sites"].remove(panel.site)
        panel.timer.stop()
        panel.setParent(None)
        panel.deleteLater()
        self.relayout()
        self.save()

    def toggle_maximize(self, panel):
        self.maximized_panel = None if self.maximized_panel is panel else panel
        self.relayout()

    def _columns_changed(self, value):
        self.cfg["columns"] = value
        self.relayout()
        self.save()

    def relayout(self):
        while self.grid.count():
            self.grid.takeAt(0)
        for i in range(max(self.grid.columnCount(), 10)):
            self.grid.setColumnStretch(i, 0)
            self.grid.setRowStretch(i, 0)

        if self.maximized_panel in self.panels:
            visible = [self.maximized_panel]
        else:
            visible = self.panels
        for p in self.panels:
            p.setVisible(p in visible)
        if not visible:
            return

        cols = int(self.cfg.get("columns", 0) or 0)
        if self.maximized_panel in self.panels or cols <= 0:
            cols = 1 if len(visible) == 1 else math.ceil(math.sqrt(len(visible)))
        cols = max(1, min(cols, len(visible)))
        rows = math.ceil(len(visible) / cols)

        for idx, p in enumerate(visible):
            self.grid.addWidget(p, idx // cols, idx % cols)
        for c in range(cols):
            self.grid.setColumnStretch(c, 1)
        for r in range(rows):
            self.grid.setRowStretch(r, 1)

    def save(self):
        save_config(self.cfg)

    def closeEvent(self, event):
        self.save()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Monitor Web")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
