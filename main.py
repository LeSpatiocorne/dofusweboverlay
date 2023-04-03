import sys, keyboard, traceback
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout, QShortcut

print("Starting...")

class WebOverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dofus Web Overlay")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.tab_widget = QTabWidget(self)

        self.settings = QWebEngineSettings.globalSettings()
        self.settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)

        self.add_tab("https://dofensive.com/fr", "Dofensive")
        self.add_tab("https://dofus-portals.fr", "Dofus-Portals")
        self.add_tab("https://dofusdb.fr/fr/tools/treasure-hunt", "DofusDB")
        self.add_tab("https://dofusplanet.com/", "DofusPlanet")
        self.add_tab("https://www.dofupscommu.fr", "DofupsCommu")
        self.add_tab("https://www.dofups.fr", "Dofups")
        self.add_tab("https://www.dofusbook.net/fr/", "DofusBook")
        self.add_tab("https://www.dofuspourlesnoobs.com", "Dofus pour les noobs")
        self.add_tab("https://www.metamob.fr", "Metamob")

        self.settings_widget = QWidget(self)
        self.settings_layout = QHBoxLayout(self.settings_widget)

        self.transparency_slider = QSlider(self)
        self.transparency_slider.setOrientation(1)
        self.transparency_slider.valueChanged.connect(self.change_transparency)

        self.transparency_label = QLabel("Transparence :", self)
        self.transparency_value_label = QLabel("100", self)

        self.settings_layout.addWidget(self.transparency_label)
        self.settings_layout.addWidget(self.transparency_slider)
        self.settings_layout.addWidget(self.transparency_value_label)

        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.settings_widget)

        self.setCentralWidget(self.main_widget)

        self.shortcut_reset_transparency = QShortcut(QKeySequence("Ctrl+Alt+R"), self)
        self.shortcut_reset_transparency.activated.connect(self.reset_transparency)

        self.shortcut_toggle_window = QShortcut(QKeySequence("Ctrl+Alt+W"), self)
        self.shortcut_toggle_window.activated.connect(self.toggle_window)

        keyboard.add_hotkey("shift+ctrl+alt+a", self.reset_transparency)
        keyboard.add_hotkey("shift+ctrl+alt+w", self.toggle_window)

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.handle_clipboard_change)

    print("loaded main process")

    def handle_clipboard_change(self):
        mime_data = self.clipboard.mimeData()
        if mime_data.hasText():
            print("Nouveau contenu dans le presse-papiers:", mime_data.text())

    def add_tab(self, url, title):
        browser = QWebEngineView(self)
        browser.setUrl(QUrl(url))
        self.tab_widget.addTab(browser, title)

    def change_transparency(self, value):
        self.transparency_value_label.setText(str(value))
        self.setWindowOpacity(value / 100)

    def reset_transparency(self):
        self.transparency_slider.setValue(100)

    def toggle_window(self):
        if self.windowOpacity() == 0:
            self.setWindowOpacity(100)
        elif self.windowOpacity() > 0:
            self.setWindowOpacity(0)

    print("loaded definitions")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = WebOverlayWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
