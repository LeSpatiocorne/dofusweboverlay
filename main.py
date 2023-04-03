import sys, traceback, wx, wx.html2
from pynput import keyboard

class WebOverlayWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Dofus Web Overlay", size=(800, 600), style=wx.STAY_ON_TOP | wx.CAPTION | wx.RESIZE_BORDER)


        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self.panel)

        self.add_tab("https://dofensive.com/fr", "Dofensive")
        self.add_tab("https://dofus-portals.fr", "Dofus-Portals")
        self.add_tab("https://dofusdb.fr/fr/tools/treasure-hunt", "DofusDB")
        self.add_tab("https://dofusplanet.com/", "DofusPlanet")
        self.add_tab("https://www.dofupscommu.fr", "DofupsCommu")
        self.add_tab("https://www.dofups.fr", "Dofups")
        self.add_tab("https://www.dofusbook.net/fr/", "DofusBook")
        self.add_tab("https://www.dofuspourlesnoobs.com", "Dofus pour les noobs")
        self.add_tab("https://www.metamob.fr", "Metamob")

        self.settings_panel = wx.Panel(self.panel)
        self.settings_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.transparency_label = wx.StaticText(self.settings_panel, label="Transparence :")
        self.transparency_slider = wx.Slider(self.settings_panel, minValue=0, maxValue=100, value=100, style=wx.SL_HORIZONTAL)
        self.transparency_slider.Bind(wx.EVT_SLIDER, self.change_transparency)

        self.settings_sizer.Add(self.transparency_label, 0, wx.ALIGN_CENTER_VERTICAL)
        self.settings_sizer.Add(self.transparency_slider, 0, wx.ALIGN_CENTER_VERTICAL)

        self.settings_panel.SetSizer(self.settings_sizer)

        self.sizer.Add(self.notebook, 1, wx.EXPAND)
        self.sizer.Add(self.settings_panel, 0, wx.EXPAND)

        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Ajoutez ces lignes pour définir les touches de raccourci et démarrer le listener
        self.toggle_key = {keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('W')}
        self.current_keys = set()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.keyboard_listener.start()

    def add_tab(self, url, title):
        browser_panel = wx.Panel(self.notebook)
        browser_sizer = wx.BoxSizer(wx.VERTICAL)
        browser = wx.html2.WebView.New(browser_panel)
        browser.LoadURL(url)
        browser_sizer.Add(browser, 1, wx.EXPAND)
        browser_panel.SetSizer(browser_sizer)
        self.notebook.AddPage(browser_panel, title)

    def change_transparency(self, event):
        value = event.GetEventObject().GetValue()
        self.SetTransparent(int(value * 2.55))

    # Ajoutez ces méthodes pour gérer les événements du clavier et afficher/masquer la fenêtre
    def on_key_press(self, key):
        if key in self.toggle_key:
            self.current_keys.add(key)
            if self.current_keys == self.toggle_key:
                wx.CallAfter(self.toggle_window)  # Utilisez CallAfter pour éviter les problèmes de thread

    def on_key_release(self, key):
        if key in self.current_keys:
            self.current_keys.remove(key)

    def toggle_window(self):
        if self.IsShown():
            self.Hide()
        else:
            self.Show()
            self.Raise()
    def on_close(self, event):
        self.keyboard_listener.stop()
        self.Destroy()

if __name__ == "__main__":
    try:
        app = wx.App()
        window = WebOverlayWindow()
        window.Show()
        app.MainLoop()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
