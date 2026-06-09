#Le pedí a la IA Claude que me de un codigo para un modo oscuro.
#Mi prompt fue: "Quiero un codigo para un modo oscuro en python con wxpython, que se pueda activar y desactivar con un boton, y que cambie el fondo de la ventana y el color de los textos."

import wx
 
# Paletas de colores
LIGHT_THEME = {
    "bg": wx.Colour(245, 245, 245),
    "bg_panel": wx.Colour(255, 255, 255),
    "fg": wx.Colour(30, 30, 30),
    "fg_secondary": wx.Colour(90, 90, 90),
    "btn_bg": wx.Colour(70, 130, 180),
    "btn_fg": wx.Colour(255, 255, 255),
    "btn_hover": wx.Colour(50, 110, 160),
    "border": wx.Colour(210, 210, 210),
}
 
DARK_THEME = {
    "bg": wx.Colour(18, 18, 24),
    "bg_panel": wx.Colour(30, 30, 40),
    "fg": wx.Colour(230, 230, 230),
    "fg_secondary": wx.Colour(160, 160, 180),
    "btn_bg": wx.Colour(100, 80, 200),
    "btn_fg": wx.Colour(255, 255, 255),
    "btn_hover": wx.Colour(80, 60, 180),
    "border": wx.Colour(55, 55, 70),
}
 
 
class ToggleButton(wx.Panel):
    """Botón de toggle personalizado con animación visual."""
 
    def __init__(self, parent, label_on="☀ Modo Claro", label_off="☽ Modo Oscuro"):
        super().__init__(parent, style=wx.NO_BORDER)
        self.label_on = label_on
        self.label_off = label_off
        self.is_dark = False
        self._hover = False
 
        self.SetMinSize((200, 46))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnHover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_SIZE, lambda e: self.Refresh())
 
    def OnHover(self, e):
        self._hover = True
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.Refresh()
 
    def OnLeave(self, e):
        self._hover = False
        self.Refresh()
 
    def OnClick(self, e):
        self.is_dark = not self.is_dark
        self.Refresh()
        # Disparar evento al padre
        evt = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.GetId())
        self.GetEventHandler().ProcessEvent(evt)
 
    def OnPaint(self, e):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
 
        w, h = self.GetSize()
        theme = DARK_THEME if self.is_dark else LIGHT_THEME
        color = theme["btn_hover"] if self._hover else theme["btn_bg"]
 
        # Fondo del botón con esquinas redondeadas
        gc.SetBrush(wx.Brush(color))
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.DrawRoundedRectangle(0, 0, w, h, 23)
 
        # Texto
        label = self.label_on if self.is_dark else self.label_off
        font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD, faceName="Segoe UI")
        gc.SetFont(font, wx.Colour(255, 255, 255))
        tw, th = gc.GetTextExtent(label)
        gc.DrawText(label, (w - tw) / 2, (h - th) / 2)
 
 
class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Modo Oscuro — wxPython",
                         size=(540, 420),
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        self.is_dark = False
        self.Centre()
        self._build_ui()
        self._apply_theme()
 
    def _build_ui(self):
        self.main_panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
 
        # ── Título
        self.title_label = wx.StaticText(
            self.main_panel, label="Demostración de Modo Oscuro")
        font_title = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_BOLD, faceName="Segoe UI")
        self.title_label.SetFont(font_title)
 
        # ── Descripción
        self.desc_label = wx.StaticText(
            self.main_panel,
            label="Presioná el botón para alternar entre\nmodo claro y modo oscuro.")
        font_desc = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")
        self.desc_label.SetFont(font_desc)
 
        # ── Cuadro de texto de ejemplo
        self.text_box = wx.TextCtrl(
            self.main_panel,
            value="Este es un campo de texto de ejemplo.\n"
                  "Podés escribir aquí para ver el efecto del tema.",
            style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.BORDER_SIMPLE,
            size=(-1, 80))
        font_text = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")
        self.text_box.SetFont(font_text)
 
        # ── Botón toggle
        self.toggle_btn = ToggleButton(self.main_panel)
        self.main_panel.Bind(wx.EVT_BUTTON, self.OnToggle, self.toggle_btn)
 
        # ── Label de estado
        self.status_label = wx.StaticText(
            self.main_panel, label="Tema actual: Claro ☀")
        font_status = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                              wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")
        self.status_label.SetFont(font_status)
 
        # ── Layout
        vbox.AddSpacer(30)
        vbox.Add(self.title_label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 40)
        vbox.AddSpacer(10)
        vbox.Add(self.desc_label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 40)
        vbox.AddSpacer(20)
        vbox.Add(self.text_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)
        vbox.AddSpacer(28)
        vbox.Add(self.toggle_btn, 0, wx.ALIGN_CENTER)
        vbox.AddSpacer(16)
        vbox.Add(self.status_label, 0, wx.ALIGN_CENTER)
        vbox.AddStretchSpacer()
 
        self.main_panel.SetSizer(vbox)
 
    def OnToggle(self, e):
        self.is_dark = not self.is_dark
        self._apply_theme()
 
    def _apply_theme(self):
        theme = DARK_THEME if self.is_dark else LIGHT_THEME
 
        # Ventana y panel principal
        self.SetBackgroundColour(theme["bg"])
        self.main_panel.SetBackgroundColour(theme["bg"])
 
        # Etiquetas
        self.title_label.SetForegroundColour(theme["fg"])
        self.title_label.SetBackgroundColour(theme["bg"])
 
        self.desc_label.SetForegroundColour(theme["fg_secondary"])
        self.desc_label.SetBackgroundColour(theme["bg"])
 
        self.status_label.SetForegroundColour(theme["fg_secondary"])
        self.status_label.SetBackgroundColour(theme["bg"])
 
        # Estado
        if self.is_dark:
            self.status_label.SetLabel("Tema actual: Oscuro ☽")
        else:
            self.status_label.SetLabel("Tema actual: Claro ☀")
 
        # TextCtrl
        self.text_box.SetBackgroundColour(theme["bg_panel"])
        self.text_box.SetForegroundColour(theme["fg"])
 
        # Forzar redibujado completo
        self.main_panel.Refresh()
        self.Refresh()
        self.Update()
 
 
class App(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True
 
 
if __name__ == "__main__":
    app = App()
    app.MainLoop()