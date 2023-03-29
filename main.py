import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout

class WebOverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dofus Web Overlay")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.tab_widget = QTabWidget(self)

        self.add_tab("https://dofensive.com/fr", "Dofensive")
        self.add_tab("https://dofus-portals.fr", "Dofus-Portals")
        self.add_tab("https://dofusdb.fr/fr/tools/treasure-hunt", "DofusDB")
        self.add_tab("https://dofusplanet.com/", "DofusPlanet")
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

    def add_tab(self, url, title):
        browser = QWebEngineView(self)
        browser.setUrl(QUrl(url))
        self.tab_widget.addTab(browser, title)

    def change_transparency(self, value):
        self.transparency_value_label.setText(str(value))
        self.setWindowOpacity(value / 100)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebOverlayWindow()
    window.show()
    sys.exit(app.exec_())
