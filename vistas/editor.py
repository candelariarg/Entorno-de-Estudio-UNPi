import wx
import wx.richtext as rt
from database import DatabaseManager
 
COLOR_NAVY  = wx.Colour(17, 46, 107)
COLOR_BLUE  = wx.Colour(0, 85, 150)
COLOR_BG    = wx.Colour(245, 245, 245)
COLOR_WHITE = wx.Colour(255, 255, 255)
 
 
class EditorEstudio(wx.Frame):
    def __init__(self, parent, tema):
        super().__init__(parent, title=f"Estudiando: {tema}", size=(950, 650))
        self.tema = tema
        self.db = DatabaseManager("datos/apuntes.db")
 
        # Registrar handlers de richtext (necesario una sola vez)
        self._registrar_handlers()
 
        main_panel = wx.Panel(self)
        main_panel.SetBackgroundColour(COLOR_BG)
        sizer = wx.BoxSizer(wx.VERTICAL)
 
        # ── Encabezado ───────────────────────────────────────
        lbl = wx.StaticText(main_panel, label=f"Tema: {tema}")
        lbl.SetForegroundColour(COLOR_BLUE)
        font = lbl.GetFont()
        font.SetPointSize(14)
        font.MakeBold()
        lbl.SetFont(font)
 
        instruccion = wx.StaticText(
            main_panel,
            label="Escribí todo lo que sabés sobre este tema sin mirar ningún apunte:"
        )
        instruccion.SetForegroundColour(wx.Colour(100, 100, 100))
 
        # ── Barra de herramientas de formato ─────────────────
        toolbar_panel = wx.Panel(main_panel)
        toolbar_panel.SetBackgroundColour(wx.Colour(230, 235, 245))
        toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        def make_btn(label, tooltip, handler, is_toggle=False):
            if is_toggle:
                btn = wx.ToggleButton(toolbar_panel, label=label, size=(36, 30))
            else:
                btn = wx.Button(toolbar_panel, label=label, size=(36, 30))
            btn.SetToolTip(tooltip)
            btn.Bind(wx.EVT_TOGGLEBUTTON if is_toggle else wx.EVT_BUTTON, handler)
            return btn
 
        self.btn_bold      = make_btn("N",  "Negrita (Ctrl+B)",    self.on_bold,       is_toggle=True)
        self.btn_italic    = make_btn("K",  "Cursiva (Ctrl+I)",    self.on_italic,     is_toggle=True)
        self.btn_underline = make_btn("S",  "Subrayado (Ctrl+U)",  self.on_underline,  is_toggle=True)
 
        # Hacemos las letras representativas con estilos visuales
        font_n = self.btn_bold.GetFont(); font_n.MakeBold(); self.btn_bold.SetFont(font_n)
        font_k = self.btn_italic.GetFont(); font_k.MakeItalic(); self.btn_italic.SetFont(font_k)
        font_s = self.btn_underline.GetFont()
        self.btn_underline.SetFont(font_s)
 
        sep1 = wx.StaticLine(toolbar_panel, style=wx.LI_VERTICAL, size=(1, 24))
 
        self.btn_left   = make_btn("≡←", "Alinear izquierda",  self.on_align_left,   is_toggle=True)
        self.btn_center = make_btn("≡≡", "Centrar",            self.on_align_center, is_toggle=True)
        self.btn_right  = make_btn("≡→", "Alinear derecha",    self.on_align_right,  is_toggle=True)
 
        sep2 = wx.StaticLine(toolbar_panel, style=wx.LI_VERTICAL, size=(1, 24))
 
        btn_indent_more = make_btn("→|", "Aumentar sangría",   self.on_indent_more)
        btn_indent_less = make_btn("|←", "Reducir sangría",    self.on_indent_less)
 
        sep3 = wx.StaticLine(toolbar_panel, style=wx.LI_VERTICAL, size=(1, 24))
 
        btn_font   = make_btn("Aa",  "Elegir fuente",     self.on_font)
        btn_color  = make_btn("🎨",  "Color de texto",    self.on_color)
 
        sep4 = wx.StaticLine(toolbar_panel, style=wx.LI_VERTICAL, size=(1, 24))
 
        btn_undo = make_btn("↩", "Deshacer (Ctrl+Z)", self.on_undo)
        btn_redo = make_btn("↪", "Rehacer (Ctrl+Y)",  self.on_redo)
 
        for w in [self.btn_bold, self.btn_italic, self.btn_underline, sep1,
                  self.btn_left, self.btn_center, self.btn_right, sep2,
                  btn_indent_more, btn_indent_less, sep3,
                  btn_font, btn_color, sep4,
                  btn_undo, btn_redo]:
            flag = wx.ALIGN_CENTER_VERTICAL | wx.LEFT
            toolbar_sizer.Add(w, 0, flag, 5)
 
        toolbar_panel.SetSizer(toolbar_sizer)
 
        # ── RichTextCtrl (área de escritura) ─────────────────
        self.rtc = rt.RichTextCtrl(
            main_panel,
            style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.TE_MULTILINE
        )
        self.rtc.SetMinSize((-1, 380))
 
        # Fuente base agradable para escribir apuntes
        default_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")
        self.rtc.SetFont(default_font)
        self.rtc.SetBackgroundColour(COLOR_WHITE)
 
        # Actualizar estado de botones al mover el cursor
        self.rtc.Bind(wx.EVT_KEY_UP,        self._actualizar_toolbar)
        self.rtc.Bind(wx.EVT_LEFT_UP,       self._actualizar_toolbar)
        self.rtc.Bind(rt.EVT_RICHTEXT_CHARACTER, self._actualizar_toolbar)
 
        # ── Botones inferiores ────────────────────────────────
        btn_guardar = wx.Button(main_panel, label="💾 Guardar Apunte")
        btn_guardar.SetBackgroundColour(COLOR_BLUE)
        btn_guardar.SetForegroundColour(COLOR_WHITE)
        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar)
 
        btn_limpiar = wx.Button(main_panel, label="🗑 Limpiar")
        btn_limpiar.Bind(wx.EVT_BUTTON, self.limpiar)
 
        btn_cerrar = wx.Button(main_panel, label="Cerrar")
        btn_cerrar.Bind(wx.EVT_BUTTON, lambda e: self.Close())
 
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_limpiar,  0, wx.RIGHT, 10)
        btn_sizer.AddStretchSpacer()
        btn_sizer.Add(btn_cerrar,   0, wx.RIGHT, 10)
        btn_sizer.Add(btn_guardar,  0)
 
        # ── Ensamblaje ────────────────────────────────────────
        sizer.Add(lbl,           0, wx.ALL, 15)
        sizer.Add(instruccion,   0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(toolbar_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        sizer.Add(self.rtc,      1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)
        sizer.Add(btn_sizer,     0, wx.EXPAND | wx.ALL, 15)
        main_panel.SetSizer(sizer)
        self.Center()
 
    # ── Registro de handlers richtext ─────────────────────────
    def _registrar_handlers(self):
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is None:
            rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
            rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())
            wx.FileSystem.AddHandler(wx.MemoryFSHandler())
 
    # ── Formato de texto ──────────────────────────────────────
    def on_bold(self, event):
        self.rtc.ApplyBoldToSelection()
        self.rtc.SetFocus()
 
    def on_italic(self, event):
        self.rtc.ApplyItalicToSelection()
        self.rtc.SetFocus()
 
    def on_underline(self, event):
        self.rtc.ApplyUnderlineToSelection()
        self.rtc.SetFocus()
 
    def on_align_left(self, event):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)
        self._deselect_align_btns(except_btn=self.btn_left)
        self.rtc.SetFocus()
 
    def on_align_center(self, event):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)
        self._deselect_align_btns(except_btn=self.btn_center)
        self.rtc.SetFocus()
 
    def on_align_right(self, event):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)
        self._deselect_align_btns(except_btn=self.btn_right)
        self.rtc.SetFocus()
 
    def _deselect_align_btns(self, except_btn):
        for btn in (self.btn_left, self.btn_center, self.btn_right):
            if btn is not except_btn:
                btn.SetValue(False)
 
    def on_indent_more(self, event):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = (self.rtc.GetSelectionRange() if self.rtc.HasSelection()
                 else rt.RichTextRange(ip, ip))
            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
        self.rtc.SetFocus()
 
    def on_indent_less(self, event):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr) and attr.GetLeftIndent() >= 100:
            r = (self.rtc.GetSelectionRange() if self.rtc.HasSelection()
                 else rt.RichTextRange(ip, ip))
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
        self.rtc.SetFocus()
 
    def on_font(self, event):
        r = self.rtc.GetSelectionRange() if self.rtc.HasSelection() else None
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())
        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            font = dlg.GetFontData().GetChosenFont()
            if font and r:
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()
        self.rtc.SetFocus()
 
    def on_color(self, event):
        colourData = wx.ColourData()
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())
        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            if colour:
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()
                    attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.rtc.SetStyle(r, attr)
                else:
                    self.rtc.BeginTextColour(colour)
        dlg.Destroy()
        self.rtc.SetFocus()
 
    def on_undo(self, event):
        if self.rtc.CanUndo():
            self.rtc.Undo()
        self.rtc.SetFocus()
 
    def on_redo(self, event):
        if self.rtc.CanRedo():
            self.rtc.Redo()
        self.rtc.SetFocus()
 
    # ── Sincronizar estado visual de botones ──────────────────
    def _actualizar_toolbar(self, event):
        self.btn_bold.SetValue(self.rtc.IsSelectionBold())
        self.btn_italic.SetValue(self.rtc.IsSelectionItalics())
        self.btn_underline.SetValue(self.rtc.IsSelectionUnderlined())
        self.btn_left.SetValue(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))
        self.btn_center.SetValue(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))
        self.btn_right.SetValue(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))
        event.Skip()
 
    # ── Guardar y limpiar ─────────────────────────────────────
    def guardar(self, event):
        contenido = self.rtc.GetValue()
        if not contenido.strip():
            wx.MessageBox("Escribí algo antes de guardar.", "Atención",
                          wx.OK | wx.ICON_WARNING)
            return
        materias = {m["nombre"]: m["id"] for m in self.db.obtener_materias()}
        if self.tema not in materias:
            mat_id = self.db.agregar_materia(self.tema)
        else:
            mat_id = materias[self.tema]
        self.db.agregar_apunte(mat_id, self.tema, contenido)
        wx.MessageBox("¡Apunte guardado correctamente!", "Listo",
                      wx.OK | wx.ICON_INFORMATION)
        self.Close()
 
    def limpiar(self, event):
        if wx.MessageBox("¿Seguro que querés borrar todo el texto?", "Confirmar",
                         wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.rtc.Clear()